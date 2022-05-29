import os

INPUT_EVENTS_FILE = os.getenv("INPUT_EVENTS_FILE", "../data/flight_details.csv.gz")

INPUT_FLIGHT_FILE = os.getenv("INPUT_FLIGHT_FILE", "../data/flights.csv.gz")

REFRESH_FREQUENCY_IN_HZ = float(os.getenv("REFRESH_FREQUENCY_IN_HZ", 1))

SPEED_FACTOR = float(os.getenv("SPEED_FACTOR", 10))

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "localhost")

FLIGHT_EVENTS_QUEUE_NAME = "flight-events"

ENCODING = "utf-8"

LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
