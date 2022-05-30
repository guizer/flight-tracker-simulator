FROM python:3.9-slim-bullseye

ADD data /data
ADD event-producer /event-producer

WORKDIR /event-producer

RUN pip install pipenv && pipenv sync --system

ENV PYTHONPATH=/event-producer

ENTRYPOINT ["sh", "-c", "bash"]
