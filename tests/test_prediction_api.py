from unittest import TestCase

import hypothesis.strategies as st
import requests
from hypothesis import given, settings


class TestPredictionAPI(TestCase):
    API_ENDPOINT = "http://localhost:5000/v2/player/prediction"

    # fmt: off
    PLAYER_IDS = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24,
        25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 37, 38, 39, 41, 43, 44, 45, 46, 47, 48,
        50, 51, 52, 53, 54, 56, 57, 58, 59, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73,
        76, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97,
        98, 99, 100, 102, 103, 104, 105, 106, 107, 108, 109, 113, 114, 115
    ]
    # fmt: on

    # Define a Hypothesis strategy for player names
    PLAYERS = [f"player{i}" for i in PLAYER_IDS]
    PLAYER_NAME_STRATEGY = st.sampled_from(PLAYERS)

    # multi valid check returns list[dict]
    @settings(deadline=500)  # Increase the deadline to 500 milliseconds
    @given(
        prediction_tuple=st.tuples(
            st.lists(PLAYER_NAME_STRATEGY, min_size=1, max_size=5),
            st.booleans(),
        )
    )
    def test_valid_players(self, prediction_tuple):
        player_names_count_valid, breakdown = prediction_tuple

        params = {"name": player_names_count_valid, "breakdown": breakdown}
        response = requests.get(url=self.API_ENDPOINT, params=params)

        # Check if the response status code is 200
        if response.status_code != 200:
            print({"status": response.status_code})
            print({"params": params, "response": response.json()})

        # Check that the response contains report scores for all specified players
        json_data: list[dict] = response.json()
        self.assertEqual(response.status_code, 200)

        error = "List is empty"
        assert len(json_data) > 0, error

        error = "Not all items in the list are dictionaries"
        assert all(isinstance(item, dict) for item in json_data), error

        for item in json_data:
            predictions_breakdown = item.get("predictions_breakdown", {})
            if breakdown:
                error = "'predictions_breakdown' is not a populated dictionary"
                assert predictions_breakdown, error
            else:
                error = "'predictions_breakdown' is not an empty dictionary"
                assert not predictions_breakdown, error

    # invalid player(s) check returns empty list
    @given(
        prediction_tuple=st.tuples(
            st.lists(st.text(min_size=1, max_size=13), min_size=1, max_size=5),
            st.booleans(),
        )
    )
    def test_invalid_players(self, prediction_tuple):
        player_names_count_invalid, breakdown = prediction_tuple

        params = {"name": player_names_count_invalid, "breakdown": breakdown}
        response = requests.get(url=self.API_ENDPOINT, params=params)

        if response.status_code != 404:
            print({"status": response.status_code})
            print({"params": params, "response": response.json()})

        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.json(), {"detail": "Player not found"})
