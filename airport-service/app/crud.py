from sqlalchemy.orm import Session

from app import models


def find_airport_by_id(session: Session, airport_id: int):
    return session.query(models.Airport).filter(models.Airport.id == airport_id).first()


def find_all_airports(session: Session):
    return session.query(models.Airport).all()


def find_airports_by_country(session: Session, country: str):
    return session.query(models.Airport).filter(models.Airport.country == country).all()
