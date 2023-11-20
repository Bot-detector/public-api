import asyncio
import logging
from asyncio import Queue

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from src import api
from src.core.fastapi.dependencies import kafka
from src.core.fastapi.middleware.logging import LoggingMiddleware

from . import logging_config  # needed for log formatting

logger = logging.getLogger(__name__)


def init_routers(_app: FastAPI) -> None:
    _app.include_router(api.router)


def make_middleware() -> list[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=[
                "http://osrsbotdetector.com/",
                "https://osrsbotdetector.com/",
                "http://localhost",
                "http://localhost:8080",
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(LoggingMiddleware),
    ]
    return middleware


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Bot-Detector-API",
        description="Bot-Detector-API",
        middleware=make_middleware(),
    )
    init_routers(_app=_app)
    return _app


app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup_event():
    logger.info("startup initiated")
    producer = await kafka.kafka_producer(kafka.producer)
    asyncio.create_task(
        kafka.send_messages(
            topic="report", producer=producer, send_queue=kafka.report_send_queue
        )
    )


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("shutdown initiated")
    await kafka.producer.stop()
