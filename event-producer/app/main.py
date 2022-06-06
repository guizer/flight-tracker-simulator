import json
import logging
import math
import time
from typing import List

import pandas as pd
import pika

from app import settings
from app.event_type import EventType

logging.basicConfig(format=settings.LOGGING_FORMAT, level=logging.INFO)

logger = logging.getLogger()

CONNECTION_PARAMETERS = pika.ConnectionParameters(host=settings.RABBITMQ_URL, connection_attempts=5, retry_delay=5)


def load_events():
    logger.info("Retrieving position events from file %s", settings.INPUT_EVENTS_FILE)
    position_events = pd.read_csv(settings.INPUT_EVENTS_FILE)
    position_events["type"] = EventType.POSITION.value
    position_events = position_events[["time", "type", "flight_id", "latitude", "longitude", "altitude",
                                       "speed", "heading"]]
    position_events["time"] = position_events['time'].astype(int)
    logger.info("%d position events to process", len(position_events))

    arrival_events = position_events[["flight_id", "time"]] \
        .sort_values(["time"], ascending=False) \
        .drop_duplicates(["flight_id"])
    arrival_events["type"] = EventType.ARRIVAL.value

    position_events = position_events.merge(arrival_events[["flight_id", "time"]].rename(columns={"time": "arrival_time"}), on=["flight_id"], how="inner")
    position_events = position_events[position_events["time"] < position_events["arrival_time"]].drop(["arrival_time"], axis=1)

    all_events = pd.concat([position_events, arrival_events], axis=0)
    all_events = all_events[
        (all_events["time"] >= settings.START_TIMESTAMP) & (all_events["time"] <= settings.END_TIMESTAMP)]

    all_events = all_events.sort_values(["time"]) \
        .to_dict('records')
    logger.info("%d events to process", len(all_events))
    return all_events


def process_events(events: List[dict]):
    logger.info("Start processing events.")
    if events:
        with pika.BlockingConnection(CONNECTION_PARAMETERS) as connection:
            channel = connection.channel()
            channel.queue_declare(queue=settings.FLIGHT_EVENTS_QUEUE_NAME, auto_delete=True, durable=True)
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
                        body = current_event
                        if current_event["type"] == EventType.ARRIVAL.value:
                            body = {key: value for key, value in current_event.items() if
                                    type(value) is not float or not math.isnan(value)}
                        logger.info("Sending event %d: %s", sent_events_counter, body)
                        body = json.dumps(body).encode(settings.ENCODING)
                        channel.basic_publish(exchange="",
                                              routing_key=settings.FLIGHT_EVENTS_QUEUE_NAME,
                                              body=body,
                                              properties=pika.BasicProperties(
                                                  delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                                              ))
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


if __name__ == "__main__":
    process_events(load_events())
