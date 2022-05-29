from datetime import datetime

from sqlalchemy.orm import Session

from app import models


def find_all_status(session: Session):
    return session.query(models.FlightStatus).order_by(models.FlightStatus.time).all()


def find_all_status_more_recent_than(session: Session, min_time: datetime):
    return session.query(models.FlightStatus) \
        .filter(models.FlightStatus.time > min_time) \
        .order_by(models.FlightStatus.time) \
        .all()


def find_status(session: Session, flight_id: str):
    return session.query(models.FlightStatus).filter(models.FlightStatus.flight_id == flight_id).first()
