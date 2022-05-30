from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app import models
from app.models import FlightStatus


def find_all_status(session: Session) -> List[FlightStatus]:
    return session.query(models.FlightStatus).order_by(models.FlightStatus.time).all()


def find_all_status_more_recent_than(session: Session, min_time: datetime) -> List[FlightStatus]:
    return session.query(models.FlightStatus) \
        .filter(models.FlightStatus.time > min_time) \
        .order_by(models.FlightStatus.time) \
        .all()


def find_status_by_id(session: Session, flight_id: str) -> Optional[FlightStatus]:
    return session.query(models.FlightStatus).filter(models.FlightStatus.flight_id == flight_id).first()
