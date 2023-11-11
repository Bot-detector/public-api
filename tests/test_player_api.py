import json
import os
import sys
from unittest import TestCase

import requests
from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPlayerAPI(TestCase):
    URL = "http://localhost:5000/v2/player/report/score"
    # Define the list of player names
    # fmt: off
    player_ids = [
        3, 5, 19, 23, 26, 29, 30, 34, 34, 38, 39, 42, 42, 45, 46, 52, 52, 57, 57, 58,
        58, 69, 74, 78, 79, 80, 81, 81, 82, 85, 92, 92, 95, 98, 98, 100, 108, 112, 112,
        113, 114, 116, 121, 123, 123, 124, 134, 139, 141, 142, 146, 146, 149, 154, 156,
        157, 158, 158, 161, 162, 166, 168, 171, 173, 178, 180, 181, 187, 190, 191, 195,
        197, 199, 202, 202, 202, 204, 206, 207, 208, 212, 215, 220, 222, 222, 225, 226,
        226, 233, 236, 242, 261, 264, 265, 266, 268, 268, 276, 277, 282
    ]
    # fmt: on
    player_names_list = [f"player{i}" for i in player_ids]

    # Define a Hypothesis strategy for player names
    player_names_strategy = st.sampled_from(player_names_list)

    # multi valid player check returns list[dict]
    @settings(deadline=500)  # Increase the deadline to 500 milliseconds
    @given(
        player_names_count_valid=st.lists(player_names_strategy, min_size=1, max_size=5)
    )
    def test_get_player_report_score_valid_players_multi(
        self, player_names_count_valid
    ):
        params = {"name": player_names_count_valid}
        response = requests.get(url=self.URL, params=params)

        if response.status_code != 200:
            print(
                f"\nTest Data:\n{player_names_count_valid}\nResponse:\n{response.json()}\n"
            )
        json_data = response.json()
        self.assertEqual(response.status_code, 200),
        assert len(json_data) > 0, "List is empty"
        assert all(
            isinstance(item, dict) for item in json_data
        ), "Not all items in the list are dictionaries"

    # invalid player(s) check returns empty list
    @given(
        player_names_count_invalid=st.lists(
            st.text(min_size=1, max_size=13), min_size=1, max_size=5
        )
    )
    def test_get_player_report_score_invalid_players(self, player_names_count_invalid):
        params = {"name": player_names_count_invalid}
        response = requests.get(url=self.URL, params=params)
        if response.status_code != 200:
            print(
                f"\nTest Data:\n{player_names_count_invalid}\nResponse:\n{response.json()}\n"
            )
        self.assertEqual(response.status_code, 200),
        assert response.json() == []
