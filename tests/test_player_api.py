import os
import sys
import requests
from unittest import TestCase


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPlayerAPI(TestCase):

	def testValidPlayerReturns200(self):
		url = "http://localhost:5000/v2/players/score"
		params = {"name": ["Player1"]}
		score = requests.get(url, params)
		assert score.status_code == 200

	def testInvalidPlayerReturns200(self):
		url = "http://localhost:5000/v2/players/score"
		params = {"name": [""]}
		response = requests.get(url, params)
		assert response.status_code == 200
	
	def testInvalidPlayerBodyIsEmpty(self):
		url = "http://localhost:5000/v2/players/score"
		params = {"name": [""]}
		response = requests.get(url, params)
		error = f"Invalid response return type, expected list[dict]"
		print(response.json())
		assert isinstance(response.json(), list), error