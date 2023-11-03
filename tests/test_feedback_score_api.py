import unittest
import requests
from hypothesis import given, strategies as st


class TestFeedbackScore(unittest.TestCase):
    @given(
        player_name=st.text(),
        vote=st.integers(min_value=-1, max_value=1),
        prediction=st.sampled_from(
            [
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
        ),
        confidence=st.floats(min_value=0, max_value=1),
        subject_id=st.integers(min_value=0),
        feedback_text=st.text(),
        proposed_label=st.sampled_from(
            [
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
        ),
    )
    def test_post_feedback_score(
        self,
        player_name,
        vote,
        prediction,
        confidence,
        subject_id,
        feedback_text,
        proposed_label,
    ):
        # Define the data to send
        data = {
            "player_name": player_name,
            "vote": vote,
            "prediction": prediction,
            "confidence": confidence,
            "subject_id": subject_id,
            "feedback_text": feedback_text,
            "proposed_label": proposed_label,
        }

        # Send the POST request
        response = requests.post("http://localhost:5000/v2/feedback/score", json=data)

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "Feedback submitted successfully"
        )  # replace with your actual success message
