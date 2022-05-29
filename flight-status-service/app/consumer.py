import json
import logging

import aio_pika
from aio_pika.abc import AbstractChannel, AbstractQueue

from app import settings, models, crud
from app.database import SessionLocal
from app.dtos import FlightEventType, FlightPositionDto

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
                    if json_message["type"] == FlightEventType.POSITION.value:
                        session = SessionLocal()
                        position: FlightPositionDto = FlightPositionDto(**json_message)
                        logger.info(
                            f"The following position has been received and will be saved in the database {position}")
                        db_status = crud.find_status(session, position.flight_id)
                        if db_status is None:
                            db_status = models.FlightStatus(**position.dict())
                            session.add(db_status)
                        else:
                            for key, value in position.dict().items():
                                setattr(db_status, key, value)
                        session.commit()
                        session.close()
                    if queue.name in incoming_message.body.decode():
                        break
