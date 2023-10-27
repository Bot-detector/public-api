import os
import sys
import requests
from unittest import TestCase

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPredictionAPI(TestCase):
    def testValidPredictionReturns200(self):
        url = "http://localhost:5000/v2/prediction"
        params = {}
        # build params
        params["name"] = ["Player1"]
        params["breakdown"] = False
        score = requests.get(url, params)
        assert score.status_code == 200

    def testInvalidPredictionReturns200(self):
        url = "http://localhost:5000/v2/prediction"
        params = {"name": [""]}
        params["breakdown"] = False
        response = requests.get(url, params)
        assert response.status_code == 404

    # def testInvalidPredictionBodyIsEmpty(self):
    # 	url = "http://localhost:5000/v2/prediction"
    # 	params = {"name": [""]}
    # 	response = requests.get(url, params)
    # 	error = f"Invalid response return type, expected list[dict]"
    # 	print(response.json())
    # 	assert isinstance(response.json(), list), error
