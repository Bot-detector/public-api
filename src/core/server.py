import logging
from asyncio import Queue
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from src import api
from src.core.fastapi.dependencies.kafka_engine import AioKafkaEngine

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
    ]
    return middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create a message queue for reports
    app.state.report_queue = Queue()

    # Initialize the AioKafkaEngine for reports
    app.state.kafka_reports = AioKafkaEngine(
        bootstrap_servers=["127.0.0.1:9094"], #TODO
        topic="reports",
        message_queue=app.state.report_queue,
    )
    await app.state.kafka_reports.start_producer()
    yield
    await app.state.kafka_reports.stop_producer()


def create_app() -> FastAPI:
    _app = FastAPI(
        title="Bot-Detector-API",
        description="Bot-Detector-API",
        middleware=make_middleware(),
        lifespan=lifespan,
    )
    init_routers(_app=_app)
    return _app


app = create_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}
