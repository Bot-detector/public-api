import json
import os
import sys
from unittest import TestCase

import requests
from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPlayerAPI(TestCase):
    # Define the list of player names
    player_names_list = [f"Player{i}" for i in range(1, 100)]

    # Define a Hypothesis strategy for player names
    player_names_strategy = st.sampled_from(player_names_list)

    def test_valid_player_returns_success(self):
        url = "http://localhost:5000/v2/player/report/score"
        params = {}
        # build params
        params["name"] = ["player1"]
        score = requests.get(url, params)
        assert score.status_code == 200

    def test_invalid_player_returns_success(self):
        url = "http://localhost:5000/v2/player/report/score"
        params = {"name": ["abdefg"]}
        score = requests.get(url, params)
        assert score.status_code == 200

    def test_valid_player_returns_data(self):
        url = "http://localhost:5000/v2/player/report/score"
        params = {}
        # build params
        params["name"] = ["player1"]
        score = requests.get(url, params)
        json_data = json.loads(score.text)
        error = f"Invalid response return type, expected list[dict]"
        # print(len(json_data))
        assert len(json_data) > 0

    def test_invalid_player_returns_empty(self):
        url = "http://localhost:5000/v2/player/report/score"
        params = {}
        # build params
        params["name"] = ["abcdefg"]
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = json.loads(score.text)
        # should return a populated dictionary, should be True
        assert len(json_data) == 0

    # multi valid player check returns list[dict]
    @settings(deadline=500)  # Increase the deadline to 500 milliseconds
    @given(player_names_count_valid=st.lists(player_names_strategy, min_size=1))
    def test_get_player_report_score_valid_players_multi(
        self, player_names_count_valid
    ):
        response = requests.get(
            "http://localhost:5000/v2/player/report/score",
            params={"name": player_names_count_valid},
        )
        # print(f"Test player: {player_names}, Response: {response.json()}")
        # Check that the response contains feedback for all the specified players
        json_data = response.json()
        self.assertEqual(response.status_code, 200),
        assert len(json_data) > 0, "List is empty"
        assert all(
            isinstance(item, dict) for item in json_data
        ), "Not all items in the list are dictionaries"

    # invalid player(s) check returns empty list
    @given(
        player_names_count_invalid=st.lists(
            st.text(min_size=1, max_size=13), min_size=1
        )
    )
    def test_get_player_report_score_invalid_players(self, player_names_count_invalid):
        # print(f"Test player: {player_names}")
        response = requests.get(
            "http://localhost:5000/v2/player/report/score",
            params={"name": player_names_count_invalid},
        )
        # print(f"Response: {response.json()}")
        self.assertEqual(response.status_code, 200),
        assert response.json() == []
