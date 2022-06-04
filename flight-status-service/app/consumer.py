import json
import logging

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractQueue

from app import settings, models, crud
from app.database import SessionLocal
from app.dtos import FlightEventType, FlightStatusDto

logger = logging.getLogger()


async def consume_flight_event_messages() -> None:
    connection = await aio_pika.connect_robust(host=settings.RABBITMQ_URL, reconnect_interval=5)
    async with connection:
        channel: AbstractChannel = await connection.channel()
        queue: AbstractQueue = await channel.declare_queue(settings.FLIGHT_EVENTS_QUEUE_NAME, auto_delete=True,
                                                           durable=True)
        async with queue.iterator() as queue_iter:
            async for incoming_message in queue_iter:
                async with incoming_message.process():
                    json_message = json.loads(incoming_message.body)
                    session = SessionLocal()
                    alive = json_message["type"] == FlightEventType.POSITION.value
                    status: FlightStatusDto = FlightStatusDto(**json_message, alive=alive)
                    logger.debug(
                        f"The following status has been received and will be saved in the database {status}")
                    db_status = crud.find_status_by_id(session, status.flight_id)
                    if db_status is None and alive is True:
                        db_status = models.FlightStatus(**status.dict())
                        session.add(db_status)
                        setattr(db_status, "alive", alive)
                    elif db_status is not None:
                        for key, value in status.dict().items():
                            if value is not None:
                                setattr(db_status, key, value)
                        setattr(db_status, "alive", alive)
                    session.commit()
                    session.close()
                    if queue.name in incoming_message.body.decode():
                        break
