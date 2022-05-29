import asyncio
import json
import logging

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from app import models, crud, settings
from app.consumer import consume_flight_event_messages
from app.database import engine, SessionLocal

logging.basicConfig(format=settings.LOGGING_FORMAT, level=logging.INFO)
logger = logging.getLogger()

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine, checkfirst=True)
app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(consume_flight_event_messages())


@app.get("/stream")
async def position_stream(request: Request, session: Session = Depends(get_session)):
    async def event_publisher():
        last_position = None
        try:
            while True:
                disconnected = await request.is_disconnected()
                if disconnected:
                    logger.info(f"Disconnecting client {request.client}")
                    break
                positions = crud.find_all_positions_more_recent_than(session, last_position.time) \
                    if last_position else crud.find_all_positions(session)
                if positions:
                    last_position = positions[-1]
                    yield json.dumps(jsonable_encoder(positions))

                await asyncio.sleep(settings.STREAM_DELAY_IN_SECS)
        except asyncio.CancelledError as error:
            logger.info(f"Disconnected from client (via refresh/close) {request.client}")
            raise error

    return EventSourceResponse(event_publisher())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
