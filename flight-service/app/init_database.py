import csv
import gzip
import logging

from sqlalchemy.exc import ProgrammingError

from app import models, settings
from app.database import engine, SessionLocal
from app.dtos import FlightCreationDto

logger = logging.getLogger(__name__)


def init_database():
    try:
        models.Base.metadata.drop_all(bind=engine)
    except ProgrammingError as err:
        logger.error(err)
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
