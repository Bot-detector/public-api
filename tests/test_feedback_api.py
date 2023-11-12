import unittest

import requests
from hypothesis import given, settings
from hypothesis import strategies as st


class TestFeedbackAPI(unittest.TestCase):
    API_ENDPOINT = "http://localhost:5000/v2/player/feedback/score"

    # fmt: off
    PLAYER_IDS = [
        3, 5, 19, 23, 26, 29, 30, 34, 34, 38, 39, 42, 42, 45, 46, 52, 52, 57, 57, 58,
        58, 69, 74, 78, 79, 80, 81, 81, 82, 85, 92, 92, 95, 98, 98, 100, 108, 112, 112,
        113, 114, 116, 121, 123, 123, 124, 134, 139, 141, 142, 146, 146, 149, 154, 156,
        157, 158, 158, 161, 162, 166, 168, 171, 173, 178, 180, 181, 187, 190, 191, 195,
        197, 199, 202, 202, 202, 204, 206, 207, 208, 212, 215, 220, 222, 222, 225, 226,
        226, 233, 236, 242, 261, 264, 265, 266, 268, 268, 276, 277, 282
    ]

    COMMON_LABELS = [
        "Real_Player", "PVM_Melee_bot", "Smithing_bot", "Magic_bot", "Fishing_bot",
        "Mining_bot", "Crafting_bot", "PVM_Ranged_Magic_bot", "Hunter_bot", "Fletching_bot",
        "LMS_bot", "Agility_bot", "Wintertodt_bot", "Runecrafting_bot", "Zalcano_bot",
        "Woodcutting_bot", "Thieving_bot", "Soul_Wars_bot", "Cooking_bot", "Vorkath_bot",
        "Barrows_bot", "Herblore_bot", "Zlrah_bot", "Unknown_bot", "Something_else", "Unsure"
    ]
    # fmt: on

    # Define a Hypothesis strategy for player names
    PLAYERS = [f"player{i}" for i in PLAYER_IDS]
    PLAYER_NAME_STRATEGY = st.sampled_from(PLAYERS)

    # Test valid players and check if feedback scores are returned
    @settings(deadline=500)
    @given(valid_player_names=st.lists(PLAYER_NAME_STRATEGY, min_size=1, max_size=5))
    def test_valid_players(self, valid_player_names):
        params = {"name": valid_player_names}
        response = requests.get(url=self.API_ENDPOINT, params=params)

        # Check if the response status code is 200
        if response.status_code != 200:
            print(f"status:\n{response.status_code}")
            print(f"params:\n{params}\nresponse:\n{response.json()}")

        # Check that the response contains report scores for all specified players
        json_data = response.json()
        self.assertEqual(response.status_code, 200)

        error = "List is empty"
        assert len(json_data) > 0, error

        error = "Not all items in the list are dictionaries"
        assert all(isinstance(item, dict) for item in json_data), error

    @given(
        invalid_player_names=st.lists(
            st.text(min_size=1, max_size=13), min_size=1, max_size=5
        )
    )
    def test_invalid_players(self, invalid_player_names):
        params = {"name": invalid_player_names}
        response = requests.get(url=self.API_ENDPOINT, params=params)

        # Check if the response status code is 200
        if response.status_code != 200:
            print(f"status:\n{response.status_code}")
            print(f"params:\n{params}\nresponse:\n{response.json()}")

        # Check that the response is an empty list
        self.assertEqual(response.status_code, 200)
        assert response.json() == []


if __name__ == "__main__":
    unittest.main()
