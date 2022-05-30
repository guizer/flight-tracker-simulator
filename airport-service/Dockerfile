FROM python:3.9-slim-bullseye

ADD data /data
ADD airport-service /airport-service

WORKDIR /airport-service

RUN pip install pipenv && pipenv sync --system

ENV PYTHONPATH=/airport-service

ENTRYPOINT ["sh", "-c", "bash"]
