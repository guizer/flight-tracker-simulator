from typing import Optional

from pydantic import BaseModel


class AirportDto(BaseModel):
    id: int
    icao: str
    name: str
    country: str
    latitude: float
    longitude: float
    altitude: float
    iata: Optional[str] = None

    class Config:
        orm_mode = True
