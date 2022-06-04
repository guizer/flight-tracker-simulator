import os

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///{}/flight_status.db".format(
    os.path.join(os.path.dirname(os.path.abspath(__file__)))))

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "localhost")

FLIGHT_EVENTS_QUEUE_NAME = "flight-events"

LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

STREAM_DELAY_IN_SECS = int(os.getenv("STREAM_DELAY_IN_SECS", 3))
