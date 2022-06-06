import csv
import gzip
import logging
from sqlite3 import ProgrammingError

from app import models, settings
from app.database import engine, SessionLocal

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
        airports = [models.Airport(**{headers[i]: row[i] for i in range(len(headers))}) for row in reader]
        session.add_all(airports)
        session.commit()
        session.close()


if __name__ == "__main__":
    init_database()
