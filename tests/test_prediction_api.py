import os
import sys
import requests
import json
from unittest import TestCase

from hypothesis import given
import hypothesis.strategies as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPredictionAPI(TestCase):
    def test_valid_player_breakdown_false_returns_success(self):
        url = "http://localhost:5000/v2/prediction"
        params = {}
        # build params
        params["name"] = ["Player1"]
        params["breakdown"] = False
        score = requests.get(url, params)
        assert score.status_code == 200

    def test_valid_player_breakdown_false_returns_empty_property(self):
        url = "http://localhost:5000/v2/prediction"
        params = {}
        # build params
        params["name"] = ["Player1"]
        params["breakdown"] = False
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = (json.loads(score.text))[0]
        # should be an empty list, empty dicts return False
        assert not json_data["predictions_breakdown"]

    def test_valid_player_breakdown_true_returns_success(self):
        url = "http://localhost:5000/v2/prediction"
        params = {}
        # build params
        params["name"] = ["Player1"]
        params["breakdown"] = True
        score = requests.get(url, params)
        assert score.status_code == 200

    def test_valid_player_breakdown_true_returns_populated_property(self):
        url = "http://localhost:5000/v2/prediction"
        params = {}
        # build params
        params["name"] = ["Player1"]
        params["breakdown"] = True
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = (json.loads(score.text))[0]
        # should return a populated dictionary, should be True
        assert bool(json_data["predictions_breakdown"])

    @given(st.text(min_size=0, max_size=2))
    def test_invalid_min_player_name_length_returns_unknown(self, name):
        url = "http://localhost:5000/v2/prediction"
        # build params
        params = {"name": [name]}
        params["breakdown"] = False
        response = requests.get(url, params)
        assert response.status_code == 404

    @given(st.text(min_size=14, max_size=None))
    def test_invalid_max_player_name_length_returns_unkonwn(self, name):
        url = "http://localhost:5000/v2/prediction"
        # build params
        params = {"name": [name]}
        params["breakdown"] = False
        response = requests.get(url, params)
        assert response.status_code == 404

    def test_invalid_player_breakdown_true_returns_unknown(self):
        url = "http://localhost:5000/v2/prediction"
        params = {}
        # build params
        params["name"] = [""]
        params["breakdown"] = True
        response = requests.get(url, params)
        assert response.status_code == 404

    def test_invalid_player_breakdown_false_returns_empty_property(self):
        url = "http://localhost:5000/v2/prediction"
        params = {}
        # build params
        params["name"] = [""]
        params["breakdown"] = False
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = (json.loads(score.text))[0]
        # should be an empty list, empty dicts return False
        assert not json_data["predictions_breakdown"]

    def test_invalid_player_breakdown_true_returns_empty_property(self):
        url = "http://localhost:5000/v2/prediction"
        params = {}
        # build params
        params["name"] = [""]
        params["breakdown"] = True
        score = requests.get(url, params)
        # get first element because conversion makes it in a list
        json_data = (json.loads(score.text))[0]
        # should be an empty list, empty dicts return False
        assert not json_data["predictions_breakdown"]
