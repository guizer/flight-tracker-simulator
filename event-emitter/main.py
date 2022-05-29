import json
import logging
import time

import pandas as pd
import pika

import settings
from event_type import EventType

logging.basicConfig(format=settings.LOGGING_FORMAT, level=logging.INFO)

logger = logging.getLogger()

CONNECTION_PARAMETERS = pika.ConnectionParameters(host=settings.RABBITMQ_URL, connection_attempts=5, retry_delay=5)


def load_events():
    logger.info("Retrieving flights from file %s", settings.INPUT_FLIGHT_FILE)
    flights = pd.read_csv(settings.INPUT_FLIGHT_FILE).sort_values(["actual_time_of_departure"]).dropna()
    logger.info("%d flights to process", len(flights))

    departure_events = flights.copy()
    departure_events["time"] = departure_events["actual_time_of_departure"]
    departure_events["type"] = EventType.DEPARTURE.value
    departure_events = departure_events[["time", "type", "flight_id"]]

    arrival_events = flights.copy()
    arrival_events["time"] = arrival_events["actual_time_of_arrival"]
    arrival_events["type"] = EventType.ARRIVAL.value
    arrival_events = arrival_events[["time", "type", "flight_id"]]

    logger.info("Retrieving position events from file %s", settings.INPUT_EVENTS_FILE)
    position_events = pd.read_csv(settings.INPUT_EVENTS_FILE)
    position_events.merge(flights[["flight_id"]], on="flight_id", how="inner")
    position_events["type"] = EventType.POSITION.value
    position_events = position_events[["time",  "type", "flight_id", "latitude", "longitude", "altitude",
                                                     "speed", "heading"]]
    logger.info("%d position events to process", len(position_events))

    loaded_events = pd.concat([departure_events, arrival_events, position_events], axis=0).sort_values(
        ["time"]).to_dict('records')
    logger.info("%d events to process", len(loaded_events))
    return loaded_events


if __name__ == "__main__":
    events = load_events()
    if events:
        with pika.BlockingConnection(CONNECTION_PARAMETERS) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=settings.FLIGHT_EVENTS_QUEUE_NAME, auto_delete=True)
            logger.info("Starting simulation")
            sent_events_counter = 0
            initial_time = time.time()
            time_interval_lower_bound = time.time()
            initial_event_time = events[0]["time"]
            while events:
                time_interval_upper_bound = time.time()
                if time_interval_upper_bound - time_interval_lower_bound >= 1. / settings.REFRESH_FREQUENCY_IN_HZ:
                    current_event = events[0]
                    while current_event and (current_event["time"] - initial_event_time) <= (
                            time_interval_upper_bound - initial_time) * settings.SPEED_FACTOR:
                        logger.info("Sending event %d: %s", sent_events_counter, current_event)
                        channel.basic_publish(exchange="", routing_key=settings.FLIGHT_EVENTS_QUEUE_NAME,
                                              body=json.dumps(current_event).encode(settings.ENCODING))
                        sent_events_counter += 1
                        if events:
                            events.pop(0)
                        if events:
                            current_event = events[0]
                        else:
                            current_event = None
                    time_interval_lower_bound = time.time()
            logger.info("%d events have been successfully processed.", sent_events_counter)
    else:
        logger.info("No event to process.")
    logger.info("Simulation terminated.")
