FROM python:3.9-slim

ADD . /app/

WORKDIR /app/airport-service

RUN pip install pipenv && pipenv sync --system

ENTRYPOINT ["sh", "-c", "bash"]
