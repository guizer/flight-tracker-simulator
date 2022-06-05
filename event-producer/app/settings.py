import os
from datetime import datetime

INPUT_EVENTS_FILE = os.getenv("INPUT_EVENTS_FILE", "../../data/flight_details.csv.gz")

REFRESH_FREQUENCY_IN_HZ = float(os.getenv("REFRESH_FREQUENCY_IN_HZ", 1))

SPEED_FACTOR = float(os.getenv("SPEED_FACTOR", 100))

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "localhost")

FLIGHT_EVENTS_QUEUE_NAME = "flight-events"

ENCODING = "utf-8"

LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

START_TIMESTAMP = int(
    datetime.strptime(os.getenv("START_DATE", "1970-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S").strftime("%s"))

END_TIMESTAMP = int(datetime.strptime(os.getenv("END_DATE", "9999-12-31 23:59:59"), "%Y-%m-%d %H:%M:%S").strftime("%s"))
