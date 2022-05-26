from sqlalchemy import Column, FLOAT, Integer, String

from database import Base


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    icao = Column(String, nullable=False)
    iata = Column(String)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    latitude = Column(FLOAT, default=True)
    longitude = Column(FLOAT, default=True)
    altitude = Column(FLOAT, default=True)
