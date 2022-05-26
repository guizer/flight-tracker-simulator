from sqlalchemy.orm import Session

import models


def get_airport(db: Session, airport_id: int):
    return db.query(models.Airport).filter(models.Airport.id == airport_id).first()


def get_airports(db: Session):
    return db.query(models.Airport).all()


def get_airports_by_country(db: Session, country: str):
    return db.query(models.Airport).filter(models.Airport.country == country).all()
