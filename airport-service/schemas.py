from pydantic import BaseModel


class Airport(BaseModel):
    id = int
    icao = str
    iata = str
    name = str
    country = str
    latitude = float
    longitude = float
    altitude = float

    class Config:
        orm_mode = True
