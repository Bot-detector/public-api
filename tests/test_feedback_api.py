import unittest
import requests
from hypothesis import given, strategies as st


class TestFeedbackScore(unittest.TestCase):
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

    @given(
        player_name=st.text(),
        vote=st.integers(min_value=-1, max_value=1),
        prediction=st.sampled_from(LABELS),
        confidence=st.floats(min_value=0, max_value=1),
        subject_id=st.integers(min_value=0),
        feedback_text=st.text(),
        proposed_label=st.sampled_from(LABELS),
    )
    def test_post_feedback(
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
        response = requests.post("http://localhost:5000/v2/feedback", json=data)

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "Feedback submitted successfully"
        )  # replace with your actual success message

    @given(
        player_name=st.text(),
    )
    def test_get_feedback_score(self, player_name):
        # Define the parameters to send
        params = {
            "player_name": player_name,
        }

        # Send the GET request
        response = requests.get(
            "http://localhost:5000/v2/feedback/score", params=params
        )

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)

        # Assert that the returned data is as expected
        data = response.json()
        self.assertIn("player_name", data)
        self.assertIn("vote", data)
        self.assertIn("prediction", data)
        self.assertIn("confidence", data)
        self.assertIn("subject_id", data)
        self.assertIn("feedback_text", data)
        self.assertIn("proposed_label", data)
        self.assertEqual(data["player_name"], player_name)

        # Assert that the returned data is of specific types
        self.assertIsInstance(data["player_name"], str)
        self.assertIsInstance(data["vote"], int)
        self.assertIsInstance(data["prediction"], str)
        self.assertIsInstance(data["confidence"], float)
        self.assertIsInstance(data["subject_id"], int)
        self.assertIsInstance(data["feedback_text"], str)
        self.assertIsInstance(data["proposed_label"], str)
