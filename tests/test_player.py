import os
import sys

import pytest
from httpx import AsyncClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.mark.asyncio
async def test_player_score(custom_client):
    endpoint = "/v2/player/report/score"

    async with custom_client as client:
        client: AsyncClient
        params = {"name": "Player1"}
        response = await client.get(url=endpoint, params=params)
        json_response: list[dict] = response.json()

        assert isinstance(json_response, list)
        assert len(json_response) == 3

        assert "count" in json_response[0].keys()
        assert "possible_ban" in json_response[0].keys()
        assert "confirmed_ban" in json_response[0].keys()
        assert "confirmed_player" in json_response[0].keys()
        assert "manual_detect" in json_response[0].keys()
