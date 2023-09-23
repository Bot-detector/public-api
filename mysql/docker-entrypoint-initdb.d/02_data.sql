USE playerdata;

-- Insert data into the Players table
INSERT INTO Players (name, created_at, updated_at, possible_ban, confirmed_ban, confirmed_player, label_id, label_jagex, ironman, hardcore_ironman, ultimate_ironman, normalized_name)
SELECT
	CONCAT('Player', id) AS name,
	NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS created_at,
	NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS updated_at,
	1 AS possible_ban,
	0 AS confirmed_ban, 
	0 AS confirmed_player, 
	0 AS label_id,
	ROUND(RAND() * 1) AS label_jagex, -- Random label_jagex between 0 and 2 (inclusive)
	null ironman,
	null AS hardcore_ironman,
	null AS ultimate_ironman,
	CONCAT('player', id) AS normalized_name
FROM (
	SELECT
		(a.N + b.N * 10) AS id
	FROM
		(SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS a,
		(SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS b
) AS numbers
union
SELECT
	CONCAT('Player', id) AS name,
	NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS created_at,
	NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS updated_at,
	1 AS possible_ban,  -- 50% chance of possible_ban being true
	1 AS confirmed_ban, -- 30% chance of confirmed_ban being true, with possible_ban and label_jagex=2
	0 AS confirmed_player, -- 80% chance of confirmed_player being true
	0 AS label_id, -- Random label_id between 0 and 2 (inclusive)
	2 AS label_jagex, -- Random label_jagex between 0 and 2 (inclusive)
	null ironman,
	null AS hardcore_ironman,
	null AS ultimate_ironman,
	CONCAT('player', id) AS normalized_name
FROM (
	SELECT
		(a.N + b.N * 10+100) AS id
	FROM
		(SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS a,
		(SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS b
) AS numbers
union
SELECT
	CONCAT('Player', id) AS name,
	NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS created_at,
	NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS updated_at,
	0 AS possible_ban,  -- 50% chance of possible_ban being true
	0 AS confirmed_ban, -- 30% chance of confirmed_ban being true, with possible_ban and label_jagex=2
	1 AS confirmed_player, -- 80% chance of confirmed_player being true
	0 AS label_id, -- Random label_id between 0 and 2 (inclusive)
	0 AS label_jagex, -- Random label_jagex between 0 and 2 (inclusive)
	null ironman,
	null AS hardcore_ironman,
	null AS ultimate_ironman,
	CONCAT('player', id) AS normalized_name
FROM (
	SELECT
		(a.N + b.N * 10+200) AS id
	FROM
		(SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS a,
		(SELECT 0 AS N UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS b
) AS numbers

-- Insert data into the Reports table
INSERT INTO Reports (created_at, reportedID, reportingID, region_id, x_coord, y_coord, z_coord, timestamp, manual_detect, on_members_world, on_pvp_world, world_number, equip_head_id, equip_amulet_id, equip_torso_id, equip_legs_id, equip_boots_id, equip_cape_id, equip_hands_id, equip_weapon_id, equip_shield_id, equip_ge_value)
SELECT
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS created_at,
    p1.id AS reportedID,
    p2.id AS reportingID,
    ROUND(RAND() * 1000) AS region_id, -- Random region_id
    ROUND(RAND() * 1000) AS x_coord,   -- Random x_coord
    ROUND(RAND() * 1000) AS y_coord,   -- Random y_coord
    ROUND(RAND() * 1000) AS z_coord,   -- Random z_coord
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS timestamp,
    ROUND(RAND()) AS manual_detect,    -- Random manual_detect (0 or 1)
    ROUND(RAND() * 1000) AS on_members_world, -- Random on_members_world
    ROUND(RAND()) AS on_pvp_world,     -- Random on_pvp_world (0 or 1)
    ROUND(RAND() * 100) AS world_number, -- Random world_number
    ROUND(RAND() * 1000) AS equip_head_id, -- Random equip_head_id
    ROUND(RAND() * 1000) AS equip_amulet_id, -- Random equip_amulet_id
    ROUND(RAND() * 1000) AS equip_torso_id, -- Random equip_torso_id
    ROUND(RAND() * 1000) AS equip_legs_id, -- Random equip_legs_id
    ROUND(RAND() * 1000) AS equip_boots_id, -- Random equip_boots_id
    ROUND(RAND() * 1000) AS equip_cape_id,  -- Random equip_cape_id
    ROUND(RAND() * 1000) AS equip_hands_id, -- Random equip_hands_id
    ROUND(RAND() * 1000) AS equip_weapon_id, -- Random equip_weapon_id
    ROUND(RAND() * 1000) AS equip_shield_id, -- Random equip_shield_id
    ROUND(RAND() * 10000) AS equip_ge_value -- Random equip_ge_value
FROM
    Players p1
    CROSS JOIN Players p2
WHERE
    p1.id <> p2.id -- Ensure reportedID and reportingID are different
ORDER BY
    RAND() -- Randomize the order of the combinations
LIMIT
    10000 -- Limit the number of combinations to insert
; 