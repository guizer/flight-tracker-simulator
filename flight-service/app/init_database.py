import csv
import gzip

from app import models, settings
from app.database import engine, SessionLocal
from app.dtos import FlightCreationDto


def init_database():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine, checkfirst=False)
    with gzip.open(settings.INPUT_FLIGHT_FILE, "rt") as file:
        session = SessionLocal()
        reader = csv.reader(file, skipinitialspace=True)
        headers = next(reader)
        flights = [models.Flight(**FlightCreationDto(**{headers[i]: row[i] for i in range(len(headers))}).dict())
                   for row in reader]
        session.add_all(flights)
        session.commit()
        session.close()


if __name__ == "__main__":
    init_database()
