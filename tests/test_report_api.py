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


class TestReportAPI(unittest.TestCase):
    API_ENDPOINT = "http://localhost:5000/v2/report"

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
        response = requests.post(url=self.API_ENDPOINT, json=test_data)

        # Check if the response status code is 201
        if response.status_code != 201:
            print({"status": response.status_code})
            print({"test_data": test_data, "response": response.json()})

        self.assertEqual(response.status_code, 201)

    def test_post_reports_unprocessable_entity(self):
        response = requests.post(url=self.API_ENDPOINT, json=[{}])

        # Check if the response status code is 422
        if response.status_code != 422:
            print({"status": response.status_code})
            print({"response": response.json()})

        self.assertEqual(response.status_code, 422)

    def test_post_reports_bad_data(self):
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

        response = requests.post(url=self.API_ENDPOINT, json=bad_data)

        # Check if the response status code is 400
        if response.status_code != 400:
            print({"status": response.status_code})
            print({"data": bad_data, "response": response.json()})

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
