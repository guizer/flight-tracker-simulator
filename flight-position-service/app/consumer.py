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
        queue: AbstractQueue = await channel.declare_queue(settings.FLIGHT_EVENTS_QUEUE_NAME, auto_delete=True)
        async with queue.iterator() as queue_iter:
            async for incoming_message in queue_iter:
                async with incoming_message.process():
                    json_message = json.loads(incoming_message.body)
                    if json_message["type"] == FlightEventType.POSITION.value:
                        session = SessionLocal()
                        position: FlightPositionDto = FlightPositionDto(**json_message)
                        logger.info(
                            f"The following position has been received and will be saved in the database {position}")
                        db_position = crud.find_position(session, position.flight_id)
                        if db_position is None:
                            db_position = models.FlightPosition(**position.dict())
                            session.add(db_position)
                        else:
                            for key, value in position.dict().items():
                                setattr(db_position, key, value)
                        session.commit()
                        session.close()
                    if queue.name in incoming_message.body.decode():
                        break
