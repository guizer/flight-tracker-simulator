import logging
from typing import List

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models, crud, settings
from app.database import engine, SessionLocal
from app.dtos import FlightDto

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


@app.get("/flights", response_model=List[FlightDto])
def get_flights(flight_id: str = None, skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    if flight_id is not None:
        return crud.find_flights_by_flight_id(session, flight_id, skip, limit)
    return crud.find_flights(session, skip, limit)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002, debug=True)
