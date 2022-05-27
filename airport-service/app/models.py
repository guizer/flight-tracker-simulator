from sqlalchemy import Column, FLOAT, Integer, String

from app.database import Base


class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    icao = Column(String, nullable=False)
    iata = Column(String)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    latitude = Column(FLOAT, nullable=False)
    longitude = Column(FLOAT, nullable=False)
    altitude = Column(FLOAT, nullable=False)
