from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class FlightPositionDto(BaseModel):
    flight_id: str
    time: datetime
    latitude: float
    longitude: float
    altitude: float
    speed: float
    heading: float

    class Config:
        orm_mode = True


class FlightEventType(Enum):
    DEPARTURE = "DEPARTURE"
    ARRIVAL = "ARRIVAL"
    POSITION = "POSITION"
