import time
import unittest
from uuid import uuid4

import requests
from hypothesis import given
from hypothesis.strategies import (
    dictionaries,
    fixed_dictionaries,
    integers,
    just,
    lists,
    none,
    one_of,
    sampled_from,
    text,
)

# Calculate the minimum and maximum timestamp values
# 360 sec buffer for testing on min and max
current_time = int(time.time())
min_ts = current_time - (25200 - 360)
max_ts = current_time

# Generate a unique string for each reporter
unique_reporter = str(uuid4()).replace("-", "")[:13]


class TestPostReports(unittest.TestCase):
    @given(
        lists(
            fixed_dictionaries(
                {
                    "reporter": just(unique_reporter),
                    "reported": text(min_size=1, max_size=12),
                    "region_id": integers(min_value=0, max_value=100_000),
                    "x_coord": integers(min_value=0),
                    "y_coord": integers(min_value=0),
                    "z_coord": integers(min_value=0),
                    "ts": integers(min_value=min_ts, max_value=max_ts),
                    "manual_detect": one_of(just(0), just(1)),
                    "on_members_world": one_of(just(0), just(1)),
                    "on_pvp_world": one_of(just(0), just(1)),
                    "world_number": integers(min_value=300, max_value=1000),
                    "equipment": dictionaries(
                        keys=sampled_from(
                            [
                                "equip_head_id",
                                "equip_amulet_id",
                                "equip_torso_id",
                                "equip_legs_id",
                                "equip_boots_id",
                                "equip_cape_id",
                                "equip_hands_id",
                                "equip_weapon_id",
                                "equip_shield_id",
                            ]
                        ),
                        values=integers(min_value=0),
                        dict_class=dict,
                    ),
                    "equip_ge_value": integers(min_value=0),
                }
            ),
            min_size=1,  # Ensure the list has at least one element
        )
    )
    def test_post_reports(self, test_data):
        # Make POST request to /reports endpoint
        response = requests.post("http://localhost:5000/v2/reports", json=test_data)

        # Print the test data and response data for debugging
        if response.status_code != 201:
            print(f"\nTest Data:\n{test_data}\nResponse:\n{response.json()}\n")
        # Assert that the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

    def test_post_reports_unprocessable_entity(self):
        # Modify test_data to make it invalid

        # Make POST request to /reports endpoint
        response = requests.post("http://localhost:5000/v2/reports", json=[{}])

        # Print the test data and response data for debugging
        # print(f"\nResponse:\n{response.json()}\n")

        # Assert that the response status code is 422 (Unprocessable Entity)
        self.assertEqual(response.status_code, 422)

    def test_post_reports_bad_data(self):
        # Define the bad data
        bad_data = [
            {
                "reporter": "0",
                "reported": "0",
                "region_id": 0,
                "x_coord": 0,
                "y_coord": 0,
                "z_coord": 0,
                "ts": 0,
                "manual_detect": 0,
                "on_members_world": 0,
                "on_pvp_world": 0,
                "world_number": 300,
                "equipment": {},
                "equip_ge_value": 0,
            }
        ]

        # Make POST request to /reports endpoint with bad data
        response = requests.post("http://localhost:5000/v2/reports", json=bad_data)

        # Assert that the response status code is 400 (Bad Data)
        self.assertEqual(response.status_code, 400)

        # # Print the response data for debugging
        # print(f"\nResponse:\n{response.json()}\n")


if __name__ == "__main__":
    unittest.main()
