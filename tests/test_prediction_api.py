import json
import os
import sys
from unittest import TestCase

import hypothesis.strategies as st
import requests
from hypothesis import given

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPredictionAPI(TestCase):
    def test_valid_player_breakdown_false_returns_success(self):
        url = "http://localhost:5000/v2/player/prediction"
        params = {}
        # build params
        params["name"] = "player1"
        params["breakdown"] = False
        score = requests.get(url, params)
        if score.status_code != 200:
            print(f"\nTest Data:\n{params}\nResponse:\n{score.json()}\n")
        assert score.status_code == 200

    def test_valid_player_breakdown_false_returns_empty_property(self):
        url = "http://localhost:5000/v2/player/prediction"
        params = {}
        # build params
        params["name"] = "player1"
        params["breakdown"] = False
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = (json.loads(score.text))[0]
        # should be an empty list, empty dicts return False
        assert not json_data["predictions_breakdown"]

    def test_valid_player_breakdown_true_returns_success(self):
        url = "http://localhost:5000/v2/player/prediction"
        params = {}
        # build params
        params["name"] = "player1"
        params["breakdown"] = True
        score = requests.get(url, params)
        assert score.status_code == 200

    def test_valid_player_breakdown_true_returns_populated_property(self):
        url = "http://localhost:5000/v2/player/prediction"
        params = {}
        # build params
        params["name"] = "player1"
        params["breakdown"] = True
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = (json.loads(score.text))[0]
        # should return a populated dictionary, should be True
        assert bool(json_data["predictions_breakdown"])

    @given(st.text(max_size=0))
    def test_invalid_min_player_name_length_returns_unknown(self, name):
        url = "http://localhost:5000/v2/player/prediction"
        # build params
        params = {"name": name}
        params["breakdown"] = False
        response = requests.get(url, params)
        assert response.status_code == 422

    @given(st.text(min_size=14))
    def test_invalid_max_player_name_length_returns_unkonwn(self, name):
        url = "http://localhost:5000/v2/player/prediction"
        # build params
        params = {"name": name}
        params["breakdown"] = False
        response = requests.get(url, params)
        assert response.status_code == 422

    def test_invalid_player_breakdown_true_returns_unknown(self):
        url = "http://localhost:5000/v2/player/prediction"
        params = {}
        # build params
        params["name"] = "abcdefg"
        params["breakdown"] = True
        response = requests.get(url, params)
        assert response.status_code == 404

    def test_invalid_player_breakdown_false_returns_player_not_found(self):
        url = "http://localhost:5000/v2/player/prediction"
        params = {}
        # build params
        params["name"] = "abcdefg"
        params["breakdown"] = False
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = json.loads(score.text)
        # should be an empty list, empty dicts return False
        assert json_data["detail"] == "Player not found"

    def test_invalid_player_breakdown_true_returns_player_not_found(self):
        url = "http://localhost:5000/v2/player/prediction"
        params = {}
        # build params
        params["name"] = "abcdefg"
        params["breakdown"] = True
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = json.loads(score.text)
        # should be an empty list, empty dicts return False
        assert json_data["detail"] == "Player not found"
