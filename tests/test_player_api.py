import os
import sys
import requests
import json
from unittest import TestCase


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPlayerAPI(TestCase):
    def valid_player_returns_success(self):
        url = "http://localhost:5000/v2/players/score"
        params = {}
        # build params
        params["name"] = ["Player1"]
        score = requests.get(url, params)
        assert score.status_code == 200

    def invalid_player_returns_success(self):
        url = "http://localhost:5000/v2/players/score"
        params = {"name": [""]}
        score = requests.get(url, params)
        assert score.status_code == 200

    def valid_player_returns_data(self):
        url = "http://localhost:5000/v2/players/score"
        params = {}
        # build params
        params["name"] = ["Player1"]
        score = requests.get(url, params)
        json_data = json.loads(score.text)
        error = f"Invalid response return type, expected list[dict]"
        print(len(json_data))
        assert len(json_data) > 0
        # assert isinstance(score.json(), list), error

    def invalid_player_returns_empty(self):
        url = "http://localhost:5000/v2/players/score"
        params = {}
        # build params
        params["name"] = [""]
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = json.loads(score.text)
        # should return a populated dictionary, should be True
        print(len(json_data))
        assert len(json_data) == 0
