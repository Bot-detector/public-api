import json
import os
import sys
from unittest import TestCase

import hypothesis.strategies as st
import requests
from hypothesis import given, settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPredictionAPI(TestCase):
    URL = "http://localhost:5000/v2/player/prediction"
    # fmt: off
    player_ids = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24,
        25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 41, 43, 44, 45, 46, 47, 48,
        50, 51, 52, 53, 54, 56, 57, 58, 59, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73,
        76, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97,
        98, 99, 100, 102, 103, 104, 105, 106, 107, 108, 109, 113, 114, 115
    ]
    # fmt: on
    player_names_list = [f"player{i}" for i in player_ids]

    # Define a Hypothesis strategy for player names
    player_names_strategy = st.sampled_from(player_names_list)

    # multi valid check returns list[dict]
    @settings(deadline=500)  # Increase the deadline to 500 milliseconds
    @given(
        prediction_tuple=st.tuples(
            st.lists(player_names_strategy, min_size=1, max_size=5),
            st.booleans(),
        )
    )
    def test_get_prediction_valid_players(self, prediction_tuple):
        player_names_count_valid, breakdown = prediction_tuple

        params = {"name": player_names_count_valid, "breakdown": breakdown}
        response = requests.get(url=self.URL, params=params)
        if response.status_code != 200:
            print(
                f"Url:\n{self.URL}\nTest Data:\n{player_names_count_valid}\nBreakdown:\n{breakdown}\nResponse:\n{response.json()}\n"
            )
        json_data = response.json()
        self.assertEqual(response.status_code, 200),
        assert len(json_data) > 0, "List is empty"
        assert all(
            isinstance(item, dict) for item in json_data
        ), "Not all items in the list are dictionaries"

        # Check if 'predictions_breakdown' in each dictionary is a populated dictionary when breakdown is True, and an empty dictionary when breakdown is False
        for item in json_data:
            predictions_breakdown = item.get("predictions_breakdown", {})
            if breakdown:
                assert (
                    predictions_breakdown
                ), "'predictions_breakdown' is not a populated dictionary"
            else:
                assert (
                    not predictions_breakdown
                ), "'predictions_breakdown' is not an empty dictionary"

    # invalid player(s) check returns empty list
    @given(
        prediction_tuple=st.tuples(
            st.lists(st.text(min_size=1, max_size=13), min_size=1, max_size=5),
            st.booleans(),
        )
    )
    def test_get_prediction_invalid_players(self, prediction_tuple):
        player_names_count_invalid, breakdown = prediction_tuple

        params = {"name": player_names_count_invalid, "breakdown": breakdown}
        response = requests.get(url=self.URL, params=params)

        if response.status_code != 404:
            print(
                f"Url:\n{self.URL}\nTest Data:\n{player_names_count_invalid}\nBreakdown:\n{breakdown}\nResponse:\n{response.json()}\n"
            )

        # print(f"Response: {response.json()}")
        self.assertEqual(response.status_code, 404),
        self.assertEqual(response.json(), {"detail": "Player not found"})
