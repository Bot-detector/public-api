from unittest import TestCase

import hypothesis.strategies as st
import requests
from hypothesis import given, settings


class TestPredictionAPI(TestCase):
    API_ENDPOINT = "http://localhost:5000/v2/player/prediction"

    # fmt: off
    PLAYER_IDS = [
        3, 5, 19, 23, 26, 29, 30, 34, 38, 39, 42, 45, 46, 52, 57, 58, 69, 74, 78, 79,
        80, 81, 82, 85, 92, 95, 98, 100, 108, 112, 113, 114, 116, 121, 123, 124, 134,
        139, 141, 142, 146, 149, 154, 156, 157, 158, 161, 162, 166, 168, 171, 173, 178,
        180, 181, 187, 190, 191, 195, 197, 199, 202, 204, 206, 207, 208, 212, 215, 220,
        222, 225, 226, 233, 236, 242, 261, 264, 265, 266, 268, 276, 277, 282
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
