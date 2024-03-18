# conftest.py
import os
import sys
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import server  # noqa: E402


@pytest.fixture
def app() -> FastAPI:
    return server.app


@pytest.fixture
@asynccontextmanager
async def custom_client(app: FastAPI):
    base_url = "http://srv.test/"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url=base_url) as client:
        yield client
