import os
import sys
import requests
from unittest import TestCase


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPlayerAPI(TestCase):

	def testPlayerGetKC(self):
		url = "http://localhost:5000/players/score"
		params = {"name":"Player1"}
		score = requests.get(url, params)
		assert score.status_code == 200