from unittest import TestCase
import os
import sys

from src.app.models import Player
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestPlayer(TestCase):
	
	def test_init(self):
		init_object = Player(self)
		assert init_object.session is not None