FROM python:3.9-slim

ADD . /flight-events-simulator/

WORKDIR /flight-events-simulator/flight-status-service

RUN pip install pipenv && pipenv sync --system

ENTRYPOINT ["sh", "-c", "bash"]
