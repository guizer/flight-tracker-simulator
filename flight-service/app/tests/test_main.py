import os

import pytest
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from app import models
from app.database import Base
from app.dtos import FlightDto
from app.main import app, get_session

engine = create_engine("sqlite:///{}/test.db".format(os.path.join(os.path.dirname(os.path.abspath(__file__)))),
                       connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

FIRST_FLIGHT = FlightDto(
    flight_id="AI143/2022-06-03",
    callsign="AIC143",
    aircraft="B788",
    airline="AIC",
    origin="VIDP",
    destination="LFPG",
    scheduled_time_of_departure="2022-06-03T09:30:00",
    scheduled_time_of_arrival="2022-06-03T18:40:00",
    actual_time_of_departure="2022-06-03T09:36:06",
    actual_time_of_arrival="2022-06-03T18:23:49",
    id=1
)

SECOND_FLIGHT = FlightDto(
    flight_id="QR37/2022-06-03",
    callsign="QTR25A",
    aircraft="B77W",
    airline="QTR",
    origin="OTHH",
    destination="LFPG",
    scheduled_time_of_departure="2022-06-03T11:55:00",
    scheduled_time_of_arrival="2022-06-03T18:55:00",
    actual_time_of_departure="2022-06-03T12:10:42",
    actual_time_of_arrival="2022-06-03T18:40:55",
    id=2
)

THIRD_FLIGHT = FlightDto(
    flight_id="5X219/2022-06-03",
    callsign="UPS219",
    aircraft="B763",
    airline="UPS",
    origin="KPHL",
    destination="LFPG",
    scheduled_time_of_departure="2022-06-03T12:06:00",
    scheduled_time_of_arrival="2022-06-03T19:02:00",
    actual_time_of_departure="2022-06-03T12:13:06",
    actual_time_of_arrival="2022-06-03T18:59:24",
    id=3
)


@pytest.fixture
def init_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    flights = [
        models.Flight(**FIRST_FLIGHT.dict()),
        models.Flight(**SECOND_FLIGHT.dict()),
        models.Flight(**THIRD_FLIGHT.dict()),
    ]
    session = TestingSession()
    session.add_all(flights)
    session.commit()
    session.close()
    app.dependency_overrides[get_session] = lambda: TestingSession()


@pytest.fixture
def test_client(init_database):
    client = TestClient(app)
    return client


def test_get_flights_return_empty_list_when_flight_not_exist(test_client):
    response = test_client.get("/flights", params={"flight_id": "unknown"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_flights_is_200_when_flight_exist(test_client):
    response = test_client.get("/flights", params={"flight_id": "AI143/2022-06-03"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == jsonable_encoder([FIRST_FLIGHT])


def test_get_flights_skip_n_first_flights(test_client):
    response = test_client.get("/flights", params={"skip": 1})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == jsonable_encoder([SECOND_FLIGHT, THIRD_FLIGHT])


def test_get_flights_limit_result_to_n_flights(test_client):
    response = test_client.get("/flights", params={"limit": 2})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == jsonable_encoder([FIRST_FLIGHT, SECOND_FLIGHT])