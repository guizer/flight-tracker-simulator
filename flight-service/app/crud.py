from sqlalchemy.orm import Session

from app import models


def find_flights_by_flight_id(session: Session, flight_id: str, skip: int, limit: int):
    return session.query(models.Flight).filter(models.Flight.flight_id == flight_id).offset(skip).limit(limit).all()


def find_flights(session: Session, skip: int, limit: int):
    return session.query(models.Flight).offset(skip).limit(limit).all()
