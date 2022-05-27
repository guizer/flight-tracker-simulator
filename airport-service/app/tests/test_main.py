import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from app import models, error_messages
from app.database import Base
from app.dtos import AirportDto
from app.main import app, get_session

engine = create_engine("sqlite:///{}/test.db".format(os.path.join(os.path.dirname(os.path.abspath(__file__)))),
                       connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

CDG_AIRPORT = AirportDto(
    id=1,
    icao="LFPG",
    iata="CDG",
    name="Paris Charles de Gaulle Airport",
    country="France",
    latitude=49.012516,
    longitude=2.555752,
    altitude=392,
)

TORONTO_PEARSON_AIRPORT = AirportDto(
    id=2,
    icao="CYYZ",
    iata="YYZ",
    name="Toronto Pearson International Airport",
    country="Canada",
    latitude=43.680634,
    longitude=-79.627007,
    altitude=569,
)


@pytest.fixture
def init_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    airports = [
        models.Airport(**CDG_AIRPORT.dict()),
        models.Airport(**TORONTO_PEARSON_AIRPORT.dict()),
    ]
    session = TestingSession()
    session.add_all(airports)
    session.commit()
    session.close()
    app.dependency_overrides[get_session] = lambda: TestingSession()


@pytest.fixture
def test_client(init_database):
    client = TestClient(app)
    return client


def test_get_airports_is_200(test_client):
    response = test_client.get("/airports")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [CDG_AIRPORT, TORONTO_PEARSON_AIRPORT]


def test_get_airports_by_country_is_200(test_client):
    response = test_client.get("/airports", params={"country": CDG_AIRPORT.country})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [CDG_AIRPORT]


def test_get_airport_is_404_when_airport_not_exist(test_client):
    response = test_client.get("/airports/3")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": error_messages.AIRPORT_NOT_FOUND}


def test_get_airport_is_200_when_airport_exist(test_client):
    response = test_client.get("/airports/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == CDG_AIRPORT
