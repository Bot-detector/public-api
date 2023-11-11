import json
import os
import sys
from unittest import TestCase

import hypothesis.strategies as st
import requests
from hypothesis import given, settings

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPredictionAPI(TestCase):
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

    # def test_valid_player_breakdown_false_returns_success(self):
    #     url = "http://localhost:5000/v2/player/prediction"
    #     params = {}
    #     # build params
    #     params["name"] = "player1"
    #     params["breakdown"] = False
    #     score = requests.get(url, params)
    #     if score.status_code != 200:
    #         print(f"\nTest Data:\n{params}\nResponse:\n{score.json()}\n")
    #     assert score.status_code == 200

    # def test_valid_player_breakdown_false_returns_empty_property(self):
    #     url = "http://localhost:5000/v2/player/prediction"
    #     params = {}
    #     # build params
    #     params["name"] = "player1"
    #     params["breakdown"] = False
    #     score = requests.get(url, params)
    #     # get first element because conversion makes it in a list
    #     json_data = (json.loads(score.text))[0]
    #     # should be an empty list, empty dicts return False
    #     assert not json_data["predictions_breakdown"]

    # def test_valid_player_breakdown_true_returns_success(self):
    #     url = "http://localhost:5000/v2/player/prediction"
    #     params = {}
    #     # build params
    #     params["name"] = "player1"
    #     params["breakdown"] = True
    #     score = requests.get(url, params)
    #     assert score.status_code == 200

    # def test_valid_player_breakdown_true_returns_populated_property(self):
    #     url = "http://localhost:5000/v2/player/prediction"
    #     params = {}
    #     # build params
    #     params["name"] = "player1"
    #     params["breakdown"] = True
    #     score = requests.get(url, params)
    #     # get first element because conversion makes it in a list
    #     json_data = (json.loads(score.text))[0]
    #     # should return a populated dictionary, should be True
    #     assert bool(json_data["predictions_breakdown"])

    # @given(st.text(max_size=0))
    # def test_invalid_min_player_name_length_returns_unknown(self, name):
    #     url = "http://localhost:5000/v2/player/prediction"
    #     # build params
    #     params = {"name": name}
    #     params["breakdown"] = False
    #     response = requests.get(url, params)
    #     assert response.status_code == 422

    # @given(st.text(min_size=14))
    # def test_invalid_max_player_name_length_returns_unkonwn(self, name):
    #     url = "http://localhost:5000/v2/player/prediction"
    #     # build params
    #     params = {"name": name}
    #     params["breakdown"] = False
    #     response = requests.get(url, params)
    #     assert response.status_code == 422

    # def test_invalid_player_breakdown_true_returns_unknown(self):
    #     url = "http://localhost:5000/v2/player/prediction"
    #     params = {}
    #     # build params
    #     params["name"] = "abcdefg"
    #     params["breakdown"] = True
    #     response = requests.get(url, params)
    #     assert response.status_code == 404

    # def test_invalid_player_breakdown_false_returns_player_not_found(self):
    #     url = "http://localhost:5000/v2/player/prediction"
    #     params = {}
    #     # build params
    #     params["name"] = "abcdefg"
    #     params["breakdown"] = False
    #     score = requests.get(url, params)
    #     # get first element because conversion makes it in a list
    #     json_data = json.loads(score.text)
    #     # should be an empty list, empty dicts return False
    #     assert json_data["detail"] == "Player not found"

    # def test_invalid_player_breakdown_true_returns_player_not_found(self):
    #     url = "http://localhost:5000/v2/player/prediction"
    #     params = {}
    #     # build params
    #     params["name"] = "abcdefg"
    #     params["breakdown"] = True
    #     score = requests.get(url, params)
    #     # get first element because conversion makes it in a list
    #     json_data = json.loads(score.text)
    #     # should be an empty list, empty dicts return False
    #     assert json_data["detail"] == "Player not found"

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
        response = requests.get(
            "http://localhost:5000/v2/player/prediction",
            params={"name": player_names_count_valid, "breakdown": breakdown},
        )
        if response.status_code != 200:
            print(
                f"\nTest Data:\n{player_names_count_valid}\nBreakdown:\n{breakdown}\nResponse:\n{response.json()}\n"
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

        response = requests.get(
            "http://localhost:5000/v2/player/feedback/score",
            params={"name": player_names_count_invalid, "breakdown": breakdown},
        )

        if response.status_code != 200:
            print(
                f"\nTest Data:\n{player_names_count_invalid}\nBreakdown:\n{breakdown}\nResponse:\n{response.json()}\n"
            )

        # print(f"Response: {response.json()}")
        self.assertEqual(response.status_code, 200),
        assert response.json() == []
