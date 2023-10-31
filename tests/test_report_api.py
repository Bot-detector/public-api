# FILEPATH: /Users/rustic/Library/Mobile Documents/com~apple~CloudDocs/workspace/bot-detector/public-api/src/tests/test_report.py

import unittest
import requests
from hypothesis import given
from hypothesis.strategies import (
    lists,
    text,
    dictionaries,
    integers,
    fixed_dictionaries,
    one_of,
    none,
    just,
)


class TestPostReports(unittest.TestCase):
    @given(
        lists(
            fixed_dictionaries(
                {
                    "reporter": text(min_size=1, max_size=13),
                    "reported": text(min_size=1, max_size=12),
                    "region_id": integers(min_value=0, max_value=100_000),
                    "x_coord": integers(min_value=0),
                    "y_coord": integers(min_value=0),
                    "z_coord": integers(min_value=0),
                    "ts": integers(min_value=0),
                    "manual_detect": one_of(just(0), just(1)),
                    "on_members_world": one_of(just(0), just(1)),
                    "on_pvp_world": one_of(just(0), just(1)),
                    "world_number": integers(min_value=300, max_value=1000),
                    "equipment": fixed_dictionaries(
                        {
                            "equip_head_id": one_of(integers(min_value=0), none()),
                            "equip_amulet_id": one_of(integers(min_value=0), none()),
                            "equip_torso_id": one_of(integers(min_value=0), none()),
                            "equip_legs_id": one_of(integers(min_value=0), none()),
                            "equip_boots_id": one_of(integers(min_value=0), none()),
                            "equip_cape_id": one_of(integers(min_value=0), none()),
                            "equip_hands_id": one_of(integers(min_value=0), none()),
                            "equip_weapon_id": one_of(integers(min_value=0), none()),
                            "equip_shield_id": one_of(integers(min_value=0), none()),
                        }
                    ),
                    "equip_ge_value": integers(min_value=0),
                }
            )
        )
    )
    def test_post_reports(self, test_data):
        # Make POST request to /reports endpoint
        response = requests.post("http://localhost:5000/v2/reports", json=test_data)

        # Print the test data and response data for debugging, but only for the first test case
        print(f"\nTest Data:\n{test_data}\nResponse:\n{response.json()}\n")
        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Assert that the response data is as expected
        self.assertEqual(response.json(), {"detail": "Reports created successfully"})

    @given(lists(integers()))
    def test_post_reports_invalid_data(self, test_data):
        # Make POST request to /reports endpoint with invalid data
        response = requests.post("http://localhost:5000/v2/reports", json=test_data)

        # Assert that the response status code is 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

        # Assert that the response data is as expected
        self.assertEqual(response.json(), {"detail": "invalid data"})


if __name__ == "__main__":
    unittest.main()
