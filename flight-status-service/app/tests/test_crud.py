from datetime import datetime

from fastapi.encoders import jsonable_encoder

from app import crud
from app.tests.conftest import FIRST_STATUS, THIRD_STATUS, SECOND_STATUS, TestingSession


def test_find_all_status(init_database):
    actual_status = crud.find_all_status(TestingSession())
    assert jsonable_encoder(actual_status) == jsonable_encoder([FIRST_STATUS, THIRD_STATUS, SECOND_STATUS])


def test_find_all_status_more_recent_than(init_database):
    actual_status = crud.find_all_status_more_recent_than(TestingSession(), datetime.fromtimestamp(1653322864))
    assert jsonable_encoder(actual_status) == jsonable_encoder([THIRD_STATUS, SECOND_STATUS])


def test_find_status_by_id_when_status_not_exist(init_database):
    actual_status = crud.find_status_by_id(TestingSession(), "non_existing_id")
    assert actual_status is None


def test_find_status_by_id_when_status_exist(init_database):
    actual_status = crud.find_status_by_id(TestingSession(), FIRST_STATUS["flight_id"])
    assert jsonable_encoder(actual_status) == jsonable_encoder(FIRST_STATUS)
