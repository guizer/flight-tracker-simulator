FROM python:3.9-slim-bullseye

ADD data /data
ADD flight-service /flight-service

WORKDIR /flight-service

RUN pip install pipenv && pipenv sync --system

ENV PYTHONPATH=/flight-service

ENTRYPOINT ["sh", "-c", "bash"]
