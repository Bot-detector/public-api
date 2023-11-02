import json
import random
import string
import time


# Function to generate random strings for reporter and reported fields
def random_string(length):
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


# Function to generate random test data for Detection model
def generate_test_data(reporter):
    now = int(time.time())
    data = {
        "reporter": reporter,
        "reported": random_string(random.randint(1, 12)),
        "region_id": random.randint(0, 100000),
        "x_coord": random.randint(0, 100),
        "y_coord": random.randint(0, 100),
        "z_coord": random.randint(0, 100),
        "ts": now - random.randint(0, 100),
        "manual_detect": random.randint(0, 1),
        "on_members_world": random.randint(0, 1),
        "on_pvp_world": random.randint(0, 1),
        "world_number": random.randint(300, 1000),
        "equipment": {
            "equip_head_id": random.randint(0, 100),
            "equip_amulet_id": random.randint(0, 100),
            "equip_torso_id": random.randint(0, 100),
            "equip_legs_id": random.randint(0, 100),
            "equip_boots_id": random.randint(0, 100),
            "equip_cape_id": random.randint(0, 100),
            "equip_hands_id": random.randint(0, 100),
            "equip_weapon_id": random.randint(0, 100),
            "equip_shield_id": random.randint(0, 100),
        },
        "equip_ge_value": random.randint(0, 100),
    }
    return data


# Generate a random Detection instance
reporter = random_string(10)
test_data = [generate_test_data(reporter) for _ in range(5)]
print(json.dumps(test_data))
