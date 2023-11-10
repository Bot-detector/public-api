import json
import unittest

import requests
from hypothesis import given, settings
from hypothesis import strategies as st


class TestFeedbackAPI(unittest.TestCase):
    # Define the list of player names
    player_names_list = [f"Player{i}" for i in range(1, 100)]

    # Define a Hypothesis strategy for player names
    player_names_strategy = st.sampled_from(player_names_list)

    # Define common labels
    LABELS = [
        "Real_Player",
        "PVM_Melee_bot",
        "Smithing_bot",
        "Magic_bot",
        "Fishing_bot",
        "Mining_bot",
        "Crafting_bot",
        "PVM_Ranged_Magic_bot",
        "Hunter_bot",
        "Fletching_bot",
        "LMS_bot",
        "Agility_bot",
        "Wintertodt_bot",
        "Runecrafting_bot",
        "Zalcano_bot",
        "Woodcutting_bot",
        "Thieving_bot",
        "Soul_Wars_bot",
        "Cooking_bot",
        "Vorkath_bot",
        "Barrows_bot",
        "Herblore_bot",
        "Zulrah_bot",
        "Unknown_bot",
        "Something_else",
        "Unsure",
    ]

    # @given(
    #     player_name=st.text(min_size=1),
    #     vote=st.integers(min_value=-1, max_value=1),
    #     prediction=st.sampled_from(LABELS),
    #     confidence=st.floats(min_value=0, max_value=1),
    #     subject_id=st.integers(min_value=0),
    #     feedback_text=st.text(),
    #     proposed_label=st.sampled_from(LABELS),
    # )
    # def test_post_feedback(
    #     self,
    #     player_name,
    #     vote,
    #     prediction,
    #     confidence,
    #     subject_id,
    #     feedback_text,
    #     proposed_label,
    # ):
    #     # Define the data to send
    #     data = {
    #         "player_name": player_name,
    #         "vote": vote,
    #         "prediction": prediction,
    #         "confidence": confidence,
    #         "subject_id": subject_id,
    #         "feedback_text": feedback_text,
    #         "proposed_label": proposed_label,
    #     }

    #     # Send the POST request
    #     response = requests.post("http://localhost:5000/v2/feedback", json=data)

    #     print(f"Test Data: {data}, Response: {response.json()}")

    #     # Assert that the response is as expected
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()["message"], "Feedback submitted successfully")

    ## test get feedback
    # single valid player check returns success list[dict]
    # def test_get_feedback_valid_players_single(self):
    #     player_names_test_list = [f"Player{i}" for i in range(1, 100)]
    #     for player_name_test in player_names_test_list:
    #         response = requests.get(
    #             "http://localhost:5000/v2/player/feedback",
    #             params={"name": player_name_test},
    #         )
    #         json_data = response.json()
    #         # print(f"Test player: {player_name_test}, Response: {response.json()}")
    #         self.assertEqual(response.status_code, 200),
    #         assert len(json_data) > 0, "List is empty"
    #         assert all(
    #             isinstance(item, dict) for item in json_data
    #         ), "Not all items in the list are dictionaries"

    # # multi valid player check returns list[dict]
    # @settings(deadline=500)  # Increase the deadline to 500 milliseconds
    # @given(player_names_multi=st.lists(player_names_strategy, min_size=1, max_size=20))
    # def test_get_feedback_valid_players_multi(self, player_names_multi):
    #     response = requests.get(
    #         "http://localhost:5000/v2/player/feedback",
    #         params={"name": player_names_multi},
    #     )
    #     # print(f"Test player: {player_names}, Response: {response.json()}")
    #     # Check that the response contains feedback for all the specified players
    #     json_data = response.json()
    #     self.assertEqual(response.status_code, 200),
    #     assert len(json_data) > 0, "List is empty"
    #     assert all(
    #         isinstance(item, dict) for item in json_data
    #     ), "Not all items in the list are dictionaries"

    # # invalid player(s) check returns empty list
    # @given(player_names_invalid=st.lists(st.text(min_size=1, max_size=13), min_size=1))
    # def test_get_feedback_invalid_players(self, player_names_invalid):
    #     # print(f"Test player: {player_names}")
    #     response = requests.get(
    #         "http://localhost:5000/v2/player/feedback",
    #         params={"name": player_names_invalid},
    #     )
    #     # print(f"Response: {response.json()}")
    #     self.assertEqual(response.status_code, 200),
    #     assert response.json() == []

    ## Test feedback count

    # single valid player check returns success list[dict]
    def test_get_feedback_score_valid_players_single(self):
        player_names_test_list = [f"Player{i}" for i in range(1, 100)]
        for player_name_test in player_names_test_list:
            response = requests.get(
                "http://localhost:5000/v2/player/feedback/score",
                params={"name": player_name_test},
            )
            json_data = response.json()
            # print(f"Test player: {player_name_test}, Response: {response.json()}")
            self.assertEqual(response.status_code, 200),
            assert len(json_data) > 0, "List is empty"
            assert all(
                isinstance(item, dict) for item in json_data
            ), "Not all items in the list are dictionaries"

    # multi valid player check returns list[dict]
    @settings(deadline=500)  # Increase the deadline to 500 milliseconds
    @given(player_names_count_valid=st.lists(player_names_strategy, min_size=1))
    def test_get_feedback_score_valid_players_multi(self, player_names_count_valid):
        response = requests.get(
            "http://localhost:5000/v2/player/feedback/score",
            params={"name": player_names_count_valid},
        )
        # print(f"Test player: {player_names}, Response: {response.json()}")
        # Check that the response contains feedback for all the specified players
        json_data = response.json()
        self.assertEqual(response.status_code, 200),
        assert len(json_data) > 0, "List is empty"
        assert all(
            isinstance(item, dict) for item in json_data
        ), "Not all items in the list are dictionaries"

    # invalid player(s) check returns empty list
    @given(
        player_names_count_invalid=st.lists(
            st.text(min_size=1, max_size=13), min_size=1
        )
    )
    def test_get_feedback_score_invalid_players(self, player_names_count_invalid):
        # print(f"Test player: {player_names}")
        response = requests.get(
            "http://localhost:5000/v2/player/feedback/score",
            params={"name": player_names_count_invalid},
        )
        # print(f"Response: {response.json()}")
        self.assertEqual(response.status_code, 200),
        assert response.json() == []
