import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_feedback_score(custom_client):
    endpoint = "/v2/player/feedback/score"

    async with custom_client as client:
        client: AsyncClient
        params = {"name": "Player1"}
        response = await client.get(url=endpoint, params=params)
        json_response: list[dict] = response.json()

        assert isinstance(json_response, list)
        json_data: dict = json_response[0]
        assert "player_name" in json_data.keys()
        assert json_data["player_name"] == "Player1"
