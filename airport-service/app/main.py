import logging
from typing import List

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import error_messages, models, crud, settings
from app.database import engine, SessionLocal
from app.dtos import AirportDto

logging.basicConfig(format=settings.LOGGING_FORMAT, level=logging.INFO)

models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/airports", response_model=List[AirportDto])
def get_airports(country: str = None, session: Session = Depends(get_session)):
    if country is None:
        return crud.find_all_airports(session)
    return crud.find_airports_by_country(session, country)


@app.get("/airports/{airport_id}", response_model=AirportDto)
def get_airport(airport_id: int, session: Session = Depends(get_session)):
    airport = crud.find_airport_by_id(session, airport_id)
    if airport is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_messages.AIRPORT_NOT_FOUND)
    return airport


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
