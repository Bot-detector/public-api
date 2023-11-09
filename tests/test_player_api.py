import json
import os
import sys
from unittest import TestCase

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPlayerAPI(TestCase):
    def test_valid_player_returns_success(self):
        url = "http://localhost:5000/v2/players/report/score"
        params = {}
        # build params
        params["name"] = ["player1"]
        score = requests.get(url, params)
        assert score.status_code == 200

    def test_invalid_player_returns_success(self):
        url = "http://localhost:5000/v2/players/report/score"
        params = {"name": ["abdefg"]}
        score = requests.get(url, params)
        assert score.status_code == 200

    def test_valid_player_returns_data(self):
        url = "http://localhost:5000/v2/players/report/score"
        params = {}
        # build params
        params["name"] = ["player1"]
        score = requests.get(url, params)
        json_data = json.loads(score.text)
        error = f"Invalid response return type, expected list[dict]"
        # print(len(json_data))
        assert len(json_data) > 0

    def test_invalid_player_returns_empty(self):
        url = "http://localhost:5000/v2/players/report/score"
        params = {}
        # build params
        params["name"] = ["abcdefg"]
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = json.loads(score.text)
        # should return a populated dictionary, should be True
        assert len(json_data) == 0
