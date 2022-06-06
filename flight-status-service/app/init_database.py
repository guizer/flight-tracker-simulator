import logging

from sqlalchemy.exc import ProgrammingError

from app import models
from app.database import engine

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        models.Base.metadata.drop_all(bind=engine)
    except ProgrammingError as err:
        logger.error(err)
    models.Base.metadata.create_all(bind=engine, checkfirst=True)
