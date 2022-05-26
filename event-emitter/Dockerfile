FROM python:3.9-slim

ADD . /app/

WORKDIR /app/event-emitter

RUN pip install pipenv && pipenv sync --system

ENTRYPOINT ["sh", "-c", "bash"]
