import os
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import Base

engine = create_engine("sqlite:///{}/test.db".format(os.path.join(os.path.dirname(os.path.abspath(__file__)))),
                       connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

FIRST_STATUS = {'time': datetime.fromtimestamp(1653322864), 'flight_id': 'BR87/2022-05-23', 'latitude': 23.984116,
                'longitude': 119.671883, 'altitude': 28300.0, 'speed': 458.0, 'heading': 225.0, 'alive': True}
SECOND_STATUS = {'time': datetime.fromtimestamp(1653323542), 'flight_id': 'AF401/2022-05-23', 'latitude': -33.209747,
                 'longitude': -70.787109, 'altitude': 7325.0, 'speed': 247.0, 'heading': 13.0, 'alive': True}
THIRD_STATUS = {'time': datetime.fromtimestamp(1653323540), 'flight_id': 'AF415/2022-05-23', 'latitude': -21.787872,
                'longitude': -70.68988, 'altitude': 18775.0, 'speed': 296.0, 'heading': 3.0, 'alive': True}


@pytest.fixture
def init_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    all_status = [models.FlightStatus(**FIRST_STATUS), models.FlightStatus(**SECOND_STATUS),
                  models.FlightStatus(**THIRD_STATUS)]
    session = TestingSession()
    session.add_all(all_status)
    session.commit()
    session.close()
