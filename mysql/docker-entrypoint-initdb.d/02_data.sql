USE playerdata;

-- Insert data into the Players table
INSERT INTO
    Players (
        name,
        created_at,
        updated_at,
        possible_ban,
        confirmed_ban,
        confirmed_player,
        label_id,
        label_jagex,
        ironman,
        hardcore_ironman,
        ultimate_ironman,
        normalized_name
    )
SELECT
    CONCAT('Player', id) AS name,
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS created_at,
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS updated_at,
    1 AS possible_ban,
    0 AS confirmed_ban,
    0 AS confirmed_player,
    0 AS label_id,
    ROUND(RAND() * 1) AS label_jagex,
    null AS ironman,
    null AS hardcore_ironman,
    null AS ultimate_ironman,
    CONCAT('player', id) AS normalized_name
FROM (
        SELECT id
        FROM (
            SELECT 1 + a.i + b.i * 10 AS id
            FROM (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS a
            CROSS JOIN (SELECT 0 AS i UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 UNION SELECT 9) AS b
        ) AS numbers
        WHERE id <= 100
    ) AS players;
-- Insert data into the Reports table

INSERT INTO
    Reports (
        created_at,
        reportedID,
        reportingID,
        region_id,
        x_coord,
        y_coord,
        z_coord,
        timestamp,
        manual_detect,
        on_members_world,
        on_pvp_world,
        world_number,
        equip_head_id,
        equip_amulet_id,
        equip_torso_id,
        equip_legs_id,
        equip_boots_id,
        equip_cape_id,
        equip_hands_id,
        equip_weapon_id,
        equip_shield_id,
        equip_ge_value
    )
SELECT
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS created_at,
    p1.id AS reportedID,
    p2.id AS reportingID,
    ROUND(RAND() * 1000) AS region_id,
    -- Random region_id
    ROUND(RAND() * 1000) AS x_coord,
    -- Random x_coord
    ROUND(RAND() * 1000) AS y_coord,
    -- Random y_coord
    ROUND(RAND() * 1000) AS z_coord,
    -- Random z_coord
    NOW() - INTERVAL FLOOR(RAND() * 365) DAY AS timestamp,
    ROUND(RAND()) AS manual_detect,
    -- Random manual_detect (0 or 1)
    ROUND(RAND() * 1000) AS on_members_world,
    -- Random on_members_world
    ROUND(RAND()) AS on_pvp_world,
    -- Random on_pvp_world (0 or 1)
    ROUND(RAND() * 100) AS world_number,
    -- Random world_number
    ROUND(RAND() * 1000) AS equip_head_id,
    -- Random equip_head_id
    ROUND(RAND() * 1000) AS equip_amulet_id,
    -- Random equip_amulet_id
    ROUND(RAND() * 1000) AS equip_torso_id,
    -- Random equip_torso_id
    ROUND(RAND() * 1000) AS equip_legs_id,
    -- Random equip_legs_id
    ROUND(RAND() * 1000) AS equip_boots_id,
    -- Random equip_boots_id
    ROUND(RAND() * 1000) AS equip_cape_id,
    -- Random equip_cape_id
    ROUND(RAND() * 1000) AS equip_hands_id,
    -- Random equip_hands_id
    ROUND(RAND() * 1000) AS equip_weapon_id,
    -- Random equip_weapon_id
    ROUND(RAND() * 1000) AS equip_shield_id,
    -- Random equip_shield_id
    ROUND(RAND() * 10000) AS equip_ge_value -- Random equip_ge_value
FROM Players p1
    CROSS JOIN Players p2
WHERE
    p1.id <> p2.id -- Ensure reportedID and reportingID are different
ORDER BY
    RAND() -- Randomize the order of the combinations
LIMIT
    10000 -- Limit the number of combinations to insert
;

DELIMITER $$

CREATE PROCEDURE INSERTROWS(NUM INT) BEGIN 
    DECLARE i INT;
    SET i = 1;
    WHILE i <= num DO SET @rand = FLOOR(1 + RAND() * 25);
    SET @multiplier = FLOOR(51 + RAND() * 50);
    INSERT INTO Predictions
    SET
        name = CONCAT('Player', i),
        created = NOW() - INTERVAL FLOOR(RAND() * 365) DAY,
        predicted_confidence = @multiplier,
        prediction = CASE @rand
            WHEN 1 THEN 'real_player'
            WHEN 2 THEN 'pvm_melee_bot'
            WHEN 3 THEN 'smithing_bot'
            WHEN 4 THEN 'magic_bot'
            WHEN 5 THEN 'fishing_bot'
            WHEN 6 THEN 'mining_bot'
            WHEN 7 THEN 'crafting_bot'
            WHEN 8 THEN 'pvm_ranged_magic_bot'
            WHEN 9 THEN 'pvm_ranged_bot'
            WHEN 10 THEN 'hunter_bot'
            WHEN 11 THEN 'fletching_bot'
            WHEN 12 THEN 'clue_scroll_bot'
            WHEN 13 THEN 'lms_bot'
            WHEN 14 THEN 'agility_bot'
            WHEN 15 THEN 'wintertodt_bot'
            WHEN 16 THEN 'runecrafting_bot'
            WHEN 17 THEN 'zalcano_bot'
            WHEN 18 THEN 'woodcutting_bot'
            WHEN 19 THEN 'thieving_bot'
            WHEN 20 THEN 'soul_wars_bot'
            WHEN 21 THEN 'cooking_bot'
            WHEN 22 THEN 'vorkath_bot'
            WHEN 23 THEN 'barrows_bot'
            WHEN 24 THEN 'herblore_bot'
            ELSE 'unknown_bot'
        END,
        real_player = IF(@rand = 1, 1, 0) * @multiplier,
        pvm_melee_bot = IF(@rand = 2, 1, 0) * @multiplier,
        smithing_bot = IF(@rand = 3, 1, 0) * @multiplier,
        magic_bot = IF(@rand = 4, 1, 0) * @multiplier,
        fishing_bot = IF(@rand = 5, 1, 0) * @multiplier,
        mining_bot = IF(@rand = 6, 1, 0) * @multiplier,
        crafting_bot = IF(@rand = 7, 1, 0) * @multiplier,
        pvm_ranged_magic_bot = IF(@rand = 8, 1, 0) * @multiplier,
        pvm_ranged_bot = IF(@rand = 9, 1, 0) * @multiplier,
        hunter_bot = IF(@rand = 10, 1, 0) * @multiplier,
        fletching_bot = IF (@rand = 11, 1, 0) * @multiplier,
        clue_scroll_bot = IF (@rand = 12, 1, 0) * @multiplier,
        lms_bot = IF (@rand = 13, 1, 0) * @multiplier,
        agility_bot = IF (@rand = 14, 1, 0) * @multiplier,
        wintertodt_bot = IF (@rand = 15, 1, 0) * @multiplier,
        runecrafting_bot = IF (@rand = 16, 1, 0) * @multiplier,
        zalcano_bot = IF (@rand = 17, 1, 0) * @multiplier,
        woodcutting_bot = IF (@rand = 18, 1, 0) * @multiplier,
        thieving_bot = IF (@rand = 19, 1, 0) * @multiplier,
        soul_wars_bot = IF (@rand = 20, 1, 0) * @multiplier,
        cooking_bot = IF (@rand = 21, 1, 0) * @multiplier,
        vorkath_bot = IF (@rand = 22, 1, 0) * @multiplier,
        barrows_bot = IF (@rand = 23, 1, 0) * @multiplier,
        herblore_bot = IF (@rand = 24, 1, 0) * @multiplier,
        unknown_bot = IF (@rand = 25, 1, 0) * @multiplier;
    SET i = i + 1;
    END WHILE;
    END$$ 


DELIMITER ;

CALL InsertRows(250);

INSERT INTO playerdata.Labels (label) VALUES
    ('Agility_bot'),
    ('Barrows_bot'),
    ('Blast_mine_bot'),
    ('Clue_Scroll_bot'),
    ('Construction_Magic_bot'),
    ('Cooking_bot'),
    ('Crafting_bot'),
    ('Fishing_bot'),
    ('Fishing_Cooking_bot'),
    ('Fletching_bot'),
    ('Herblore_bot'),
    ('Hunter_bot'),
    ('LMS_bot'),
    ('Mage_Guild_Store_bot'),
    ('Magic_bot'),
    ('Mining_bot'),
    ('mort_myre_fungus_bot'),
    ('Phosani_bot'),
    ('PVM_Melee_bot'),
    ('PVM_Ranged_bot'),
    ('PVM_Ranged_Magic_bot'),
    ('Real_Player'),
    ('Runecrafting_bot'),
    ('Smithing_bot'),
    ('Soul_Wars_bot'),
    ('temp_real_player'),
    ('test_label'),
    ('Thieving_bot'),
    ('Unknown'),
    ('Unknown_bot'),
    ('Vorkath_bot'),
    ('Wintertodt_bot'),
    ('Woodcutting_bot'),
    ('Woodcutting_Firemaking_bot'),
    ('Woodcutting_Mining_bot'),
    ('Zalcano_bot'),
    ('Zulrah_bot')
;

INSERT INTO PredictionFeedback (voter_id, subject_id, prediction, confidence, feedback_text, vote, proposed_label)
SELECT 
    pl1.id AS voter_id, 
    pl2.id AS subject_id,
    pr.prediction,
    RAND() AS confidence, -- Generate a random confidence value between 0 and 1
    "" AS feedback_text,
    CASE WHEN RAND() > 0.5 THEN 1 ELSE -1 END AS vote,
    (SELECT label FROM Labels ORDER BY RAND() LIMIT 1) AS proposed_label
FROM (SELECT * FROM Players WHERE id BETWEEN 1 AND 100 ORDER BY RAND()) pl1
JOIN (SELECT * FROM Players WHERE id BETWEEN 1 AND 100 ORDER BY RAND()) pl2 ON pl1.id <> pl2.id
JOIN Predictions pr ON pr.id = pl2.id
ORDER BY RAND()
LIMIT 1000;

UPDATE PredictionFeedback
    SET proposed_label = prediction
WHERE 1=1
    AND vote = 1
;