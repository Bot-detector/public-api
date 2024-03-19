import os
import sys

import pytest
from httpx import AsyncClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.asyncio
async def test_prediction(custom_client):
    endpoint = "/v2/player/prediction"

    async with custom_client as client:
        client: AsyncClient
        params = {"name": "Player1", "breakdown": True}
        response = await client.get(url=endpoint, params=params)
        json_response: list[dict] = response.json()

        assert isinstance(json_response, list)
