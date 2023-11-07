import unittest

import requests
from hypothesis import given
from hypothesis import strategies as st


class TestFeedback(unittest.TestCase):
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

    def test_get_feedback_score_valid_players_single(self):
        player_names_test_list = [f"Player{i}" for i in range(1, 100)]
        for player_name_test in player_names_test_list:
            response = requests.get(
                "http://localhost:5000/v2/feedback/score",
                params={"name": player_name_test},
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            # print(f"Test Data: {data}, Response: {response.json()}")
            # Assert that the response is a dictionary
            self.assertIsInstance(data, list)

    # Custom assertion function to check if at least one response is valid
    def assert_at_least_one_valid_response(feedback_data, valid_player_names):
        assert isinstance(feedback_data, list)
        for item in feedback_data:
            if item["player_name"] in valid_player_names:
                return
        # If we reach this point, no valid response was found
        assert False, "No valid response found"

    # Define the list of player names
    player_names_list = [f"Player{i}" for i in range(1, 100)]

    # Define a Hypothesis strategy for player names
    player_names_strategy = st.sampled_from(player_names_list)

    @given(player_names=st.lists(player_names_strategy, min_size=1, max_size=10))
    def test_get_feedback_score_valid_players_multi(self, player_names):
        def assert_responses(feedback_data, valid_player_names):
            assert isinstance(feedback_data, list)
            unprocessable_entity_count = 0
            for item in feedback_data:
                if item["player_name"] in valid_player_names:
                    return
                if item["status_code"] == 422:
                    unprocessable_entity_count += 1
            # If we reach this point, no valid response was found
            assert (
                unprocessable_entity_count == 0
            ), f"Found {unprocessable_entity_count} 422 responses"

        params = {"name": player_names}
        response = requests.get(
            "http://localhost:5000/v2/feedback/score", params=params
        )

        # Check the response status code
        assert response.status_code == 200

        # Check that the response contains feedback for all the specified players
        feedback_data = response.json()

        # Assert that at least one response is valid
        assert_responses(feedback_data, player_names)

    @given(names=st.lists(st.text(min_size=1), min_size=1, max_size=13))
    def test_get_feedback_score_not_found(self, names):
        response = requests.get(
            "http://localhost:5000/v2/feedback/score",
            params={"name": names},
        )
        data = response.json()
        assert response.status_code == 404
        assert data["detail"] == "Player not found"
