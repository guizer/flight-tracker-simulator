from sqlalchemy import Column, FLOAT, TIMESTAMP, String

from app.database import Base


class FlightPosition(Base):
    __tablename__ = "flight_positions"

    flight_id = Column(String, primary_key=True, index=True)
    time = Column(TIMESTAMP, nullable=False)
    latitude = Column(FLOAT, nullable=False)
    longitude = Column(FLOAT, nullable=False)
    altitude = Column(FLOAT, nullable=False)
    speed = Column(FLOAT, nullable=False)
    heading = Column(FLOAT, nullable=False)

