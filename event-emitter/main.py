import logging
import time
from enum import Enum

import pandas as pd

import settings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger()


class EventType(Enum):
    DEPARTURE = "DEPARTURE"
    ARRIVAL = "ARRIVAL"
    POSITION = "POSITION"


def send_event(event):
    # TODO: send the event to a message broker
    pass


def load_events():
    logger.info("Retrieving flights from file %s", settings.INPUT_FLIGHT_FILE)
    flights = pd.read_csv(settings.INPUT_FLIGHT_FILE).sort_values(["actual_time_of_departure"]).dropna()
    logger.info("%d flights to process", len(flights))

    departure_events = flights.copy()
    departure_events["time"] = departure_events["actual_time_of_departure"]
    departure_events["type"] = EventType.DEPARTURE.value
    departure_events["parameters"] = departure_events["flight_id"].map(lambda flight_id: {flight_id: flight_id})
    departure_events = departure_events[["time", "type", "parameters"]]

    arrival_events = flights.copy()
    arrival_events["time"] = arrival_events["actual_time_of_arrival"]
    arrival_events["type"] = EventType.ARRIVAL.value
    arrival_events["parameters"] = arrival_events["flight_id"].map(lambda flight_id: {flight_id: flight_id})
    arrival_events = arrival_events[["time", "type", "parameters"]]

    logger.info("Retrieving position events from file %s", settings.INPUT_EVENTS_FILE)
    position_events = pd.read_csv(settings.INPUT_EVENTS_FILE)
    position_events.merge(flights[["flight_id"]], on="flight_id", how="inner")
    position_events["type"] = EventType.POSITION.value
    position_events["parameters"] = position_events[["flight_id", "latitude", "longitude", "altitude",
                                                     "speed", "heading"]] \
        .to_dict('records')
    position_events = position_events[["time", "type", "parameters"]]
    logger.info("%d position events to process", len(position_events))

    loaded_events = pd.concat([departure_events, arrival_events, position_events], axis=0).sort_values(
        ["time"]).to_dict('records')
    logger.info("%d events to process", len(loaded_events))
    return loaded_events


if __name__ == "__main__":
    logger.info("Starting simulation")
    events = load_events()
    if events:
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
                    send_event(current_event)
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
