FROM python:3.9-slim-bullseye

ADD flight-status-service /flight-status-service

WORKDIR /flight-status-service

RUN pip install pipenv && pipenv sync --system

ENV PYTHONPATH=/flight-status-service

ENTRYPOINT ["sh", "-c", "bash"]
