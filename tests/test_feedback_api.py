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

    @given(
        player_name=st.text(min_size=1),
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

        print(f"Test Data: {data}, Response: {response.json()}")

        # Assert that the response is as expected
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Feedback submitted successfully")

    def test_get_feedback_score(self):
        response = requests.get(
            "http://localhost:5000/v2/feedback/score", params={"name": ["Player1"]}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Assert that the response is a list
        self.assertIsInstance(data, list)

        # Check the structure of each feedback item in the list
        for feedback in data:
            self.assertIn("player_name", feedback)
            self.assertIn("vote", feedback)
            self.assertIn("prediction", feedback)
            self.assertIn("confidence", feedback)
            self.assertIn("subject_id", feedback)
            self.assertIn("feedback_text", feedback)
            self.assertIn("proposed_label", feedback)

        for feedback in data:
            self.assertIsInstance(feedback["player_name"], str)
            self.assertIsInstance(feedback["vote"], int)
            self.assertIsInstance(feedback["prediction"], str)
            self.assertIsInstance(
                feedback["confidence"], (int, float)
            )  # Adjust data types as needed
            self.assertIsInstance(feedback["subject_id"], int)
            self.assertIsInstance(
                feedback["feedback_text"], (str, type(None))
            )  # It can be a string or None
            self.assertIsInstance(
                feedback["proposed_label"], (str, type(None))
            )  # It can be a string or None
