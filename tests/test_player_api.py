import unittest
from unittest import TestCase

import hypothesis.strategies as st
import requests
from hypothesis import given, settings
from hypothesis import strategies as st


class TestPlayerAPI(unittest.TestCase):
    API_ENDPOINT_REPORT = "http://localhost:5000/v2/player/report/score"
    API_ENDPOINT_PREDICTION = "http://localhost:5000/v2/player/prediction"

    # fmt: off
    REPORT_IDS = [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 15, 24, 30, 47, 86,
        91, 126, 149, 183, 184, 194, 217, 249, 272, 284
    ]
    # fmt: on

    # Define a Hypothesis strategy for player names
    def name_strategy(player_ids):
        players = [f"player{i}" for i in player_ids]
        return players

    REPORTS = name_strategy(REPORT_IDS)
    REPORT_NAME_STRATEGY = st.sampled_from(REPORTS)

    # Test valid players and check if report scores are returned
    @settings(deadline=500)
    @given(valid_player_names=st.lists(REPORT_NAME_STRATEGY, min_size=1, max_size=5))
    def test_report_valid_players(self, valid_player_names):
        params = {"name": valid_player_names}
        response = requests.get(url=self.API_ENDPOINT_REPORT, params=params)

        # Check if the response status code is 200
        if response.status_code != 200:
            print({"status": response.status_code})
            print({"params": params, "response": response.json()})

        # Check that the response contains report scores for all specified players
        json_data = response.json()
        self.assertEqual(response.status_code, 200)

        error = "List is empty"
        assert len(json_data) > 0, error

        error = "Not all items in the list are dictionaries"
        assert all(isinstance(item, dict) for item in json_data), error

    # Test invalid players and check if response is an empty list
    @given(
        invalid_player_names=st.lists(
            st.text(min_size=1, max_size=13), min_size=1, max_size=5
        )
    )
    def test_report_invalid_players(self, invalid_player_names):
        params = {"name": invalid_player_names}
        response = requests.get(url=self.API_ENDPOINT_REPORT, params=params)

        # Check if the response status code is 200
        if response.status_code != 200:
            print({"status": response.status_code})
            print({"params": params, "response": response.json()})

        # Check that the response is an empty list
        self.assertEqual(response.status_code, 200)
        assert response.json() == []

    # multi valid check returns list[dict]
    @settings(deadline=500)  # Increase the deadline to 500 milliseconds
    @given(
        prediction_tuple=st.tuples(
            st.lists(REPORT_NAME_STRATEGY, min_size=1, max_size=5),
            st.booleans(),
        )
    )
    def test_prediction_valid_players(self, prediction_tuple):
        player_names_count_valid, breakdown = prediction_tuple

        params = {"name": player_names_count_valid, "breakdown": breakdown}
        response = requests.get(url=self.API_ENDPOINT_PREDICTION, params=params)

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
    def test__prediction_invalid_players(self, prediction_tuple):
        player_names_count_invalid, breakdown = prediction_tuple

        params = {"name": player_names_count_invalid, "breakdown": breakdown}
        response = requests.get(url=self.API_ENDPOINT_PREDICTION, params=params)

        if response.status_code != 404:
            print({"status": response.status_code})
            print({"params": params, "response": response.json()})

        self.assertEqual(response.status_code, 404)

        self.assertEqual(response.json(), {"detail": "Player not found"})


# Run the tests
if __name__ == "__main__":
    unittest.main()
