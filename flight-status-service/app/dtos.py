from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class FlightStatusDto(BaseModel):
    flight_id: str = Field(type=str, alias='flightId')
    time: datetime
    latitude: Optional[float]
    longitude: Optional[float]
    altitude: Optional[float]
    speed: Optional[float]
    heading: Optional[float]
    alive: bool

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class FlightEventType(Enum):
    ARRIVAL = "ARRIVAL"
    POSITION = "POSITION"
