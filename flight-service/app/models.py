from sqlalchemy import Column, Integer, String, TIMESTAMP

from app.database import Base


class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_id = Column(Integer, unique=True, index=True)
    callsign = Column(String, nullable=False)
    aircraft = Column(String, nullable=False)
    airline = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    scheduled_time_of_departure = Column(TIMESTAMP, nullable=False)
    scheduled_time_of_arrival = Column(TIMESTAMP, nullable=False)
    actual_time_of_departure = Column(TIMESTAMP, nullable=False)
    actual_time_of_arrival = Column(TIMESTAMP, nullable=False)
