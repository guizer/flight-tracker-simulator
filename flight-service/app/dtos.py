from datetime import datetime

from pydantic import BaseModel


class FlightCreationDto(BaseModel):
    flight_id: str
    callsign: str
    aircraft: str
    airline: str
    origin: str
    destination: str
    scheduled_time_of_departure: datetime
    scheduled_time_of_arrival: datetime
    actual_time_of_departure: datetime
    actual_time_of_arrival: datetime

    class Config:
        orm_mode = True


class FlightDto(FlightCreationDto):
    id: int

    class Config:
        orm_mode = True
