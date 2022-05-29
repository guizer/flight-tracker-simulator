from datetime import datetime

from sqlalchemy.orm import Session

from app import models


def find_all_positions(session: Session):
    return session.query(models.FlightPosition).order_by(models.FlightPosition.time).all()


def find_all_positions_more_recent_than(session: Session, min_time: datetime):
    return session.query(models.FlightPosition) \
        .filter(models.FlightPosition.time > min_time) \
        .order_by(models.FlightPosition.time) \
        .all()


def find_position(session: Session, flight_id: str):
    return session.query(models.FlightPosition).filter(models.FlightPosition.flight_id == flight_id).first()
