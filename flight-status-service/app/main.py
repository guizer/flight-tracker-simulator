import asyncio
import json
import logging

import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from app import models, crud, settings
from app.consumer import consume_flight_event_messages
from app.database import engine, SessionLocal
from app.dtos import FlightStatusDto

logging.basicConfig(format=settings.LOGGING_FORMAT, level=logging.INFO)
logger = logging.getLogger()

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine, checkfirst=True)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def status_stream(request: Request):
    async def event_publisher():
        try:
            last_status = None
            while True:
                disconnected = await request.is_disconnected()
                if disconnected:
                    logger.info(f"Disconnecting client {request.client}")
                    break
                session = SessionLocal()
                all_status = crud.find_all_status_more_recent_than(session, last_status.time) \
                    if last_status else crud.find_all_status(session)
                if all_status:
                    last_status = all_status[-1]
                    yield json.dumps(jsonable_encoder([FlightStatusDto.from_orm(status) for status in all_status]))
                session.close()
                await asyncio.sleep(settings.STREAM_DELAY_IN_SECS)
        except asyncio.CancelledError as error:
            logger.info(f"Disconnected from client (via refresh/close) {request.client}")
            raise error

    return EventSourceResponse(event_publisher())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
