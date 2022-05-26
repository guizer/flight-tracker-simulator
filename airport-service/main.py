import csv
import gzip

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import repository
import settings
from database import engine, SessionLocal


def init_database():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine, checkfirst=False)
    with gzip.open(settings.INPUT_FLIGHT_FILE, "rt") as file:
        db = SessionLocal()
        reader = csv.reader(file, skipinitialspace=True)
        headers = next(reader)
        for row in reader:
            airport_dict = {headers[i]: row[i] for i in range(len(headers))}
            db_airport = models.Airport(**airport_dict)
            db.add(db_airport)
        db.commit()
        db.close()


init_database()
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/airports")
def get_airports(country: str = None, db: Session = Depends(get_db)):
    if country is None:
        return repository.get_airports(db)
    return repository.get_airports_by_country(db, country)


@app.get("/airports/{airport_id}")
def get_airport(airport_id: int, db: Session = Depends(get_db)):
    airport = repository.get_airport(db, airport_id)
    if airport is None:
        raise HTTPException(status_code=404, detail="Airport not found")
    return airport


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
