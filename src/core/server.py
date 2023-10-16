import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from src import api
from src.core.kafka.report import report_engine
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
    global report_engine
    logger.info("startup initiated")
    while True:
        try:
            await report_engine.start_producer()
            logger.info("report_engine started")
            break
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(5)
            continue

    while True:
        if report_engine.is_ready():
            asyncio.ensure_future(report_engine.produce_messages())
            break
        logger.info("not ready")
        await asyncio.sleep(5)


@app.on_event("shutdown")
async def shutdown_event():
    global report_engine
    logger.info("shutdown initiated")
    await report_engine.stop_producer()
