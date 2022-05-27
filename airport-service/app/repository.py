from sqlalchemy.orm import Session

from app import models


def find_airport_by_id(db: Session, airport_id: int):
    return db.query(models.Airport).filter(models.Airport.id == airport_id).first()


def find_all_airports(db: Session):
    return db.query(models.Airport).all()


def find_airports_by_country(db: Session, country: str):
    return db.query(models.Airport).filter(models.Airport.country == country).all()
