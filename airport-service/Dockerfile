FROM python:3.9-slim

ADD . /flight-events-simulator/

WORKDIR /flight-events-simulator/airport-service

RUN pip install pipenv && pipenv sync --system

ENV PYTHONPATH=/flight-events-simulator/airport-service

ENTRYPOINT ["sh", "-c", "bash"]
