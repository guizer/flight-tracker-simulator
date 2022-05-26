import os

INPUT_FLIGHT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "airports.csv.gz")

SQLALCHEMY_DATABASE_URL = "sqlite:///./airports.db"
