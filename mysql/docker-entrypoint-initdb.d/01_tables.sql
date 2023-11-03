USE playerdata;
-- Create a table for Players
CREATE TABLE Players (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    possible_ban BOOLEAN,
    confirmed_ban BOOLEAN,
    confirmed_player BOOLEAN,
    label_id INTEGER,
    label_jagex INTEGER,
    ironman BOOLEAN,
    hardcore_ironman BOOLEAN,
    ultimate_ironman BOOLEAN,
    normalized_name TEXT
);
-- Create a table for Reports
CREATE TABLE Reports (
    ID BIGINT PRIMARY KEY AUTO_INCREMENT,
    created_at TIMESTAMP,
    reportedID INT,
    reportingID INT,
    region_id INT,
    x_coord INT,
    y_coord INT,
    z_coord INT,
    timestamp TIMESTAMP,
    manual_detect SMALLINT,
    on_members_world INT,
    on_pvp_world SMALLINT,
    world_number INT,
    equip_head_id INT,
    equip_amulet_id INT,
    equip_torso_id INT,
    equip_legs_id INT,
    equip_boots_id INT,
    equip_cape_id INT,
    equip_hands_id INT,
    equip_weapon_id INT,
    equip_shield_id INT,
    equip_ge_value BIGINT,
    CONSTRAINT `FK_Reported_Players_id` FOREIGN KEY (`reportedID`) REFERENCES `Players` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT `FK_Reporting_Players_id` FOREIGN KEY (`reportingID`) REFERENCES `Players` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
);
-- Create a table for Predictions
CREATE TABLE Predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(12),
    prediction VARCHAR(50),
    created TIMESTAMP,
    predicted_confidence DECIMAL(5, 2),
    real_player DECIMAL(5, 2) DEFAULT 0,
    pvm_melee_bot DECIMAL(5, 2) DEFAULT 0,
    smithing_bot DECIMAL(5, 2) DEFAULT 0,
    magic_bot DECIMAL(5, 2) DEFAULT 0,
    fishing_bot DECIMAL(5, 2) DEFAULT 0,
    mining_bot DECIMAL(5, 2) DEFAULT 0,
    crafting_bot DECIMAL(5, 2) DEFAULT 0,
    pvm_ranged_magic_bot DECIMAL(5, 2) DEFAULT 0,
    pvm_ranged_bot DECIMAL(5, 2) DEFAULT 0,
    hunter_bot DECIMAL(5, 2) DEFAULT 0,
    fletching_bot DECIMAL(5, 2) DEFAULT 0,
    clue_scroll_bot DECIMAL(5, 2) DEFAULT 0,
    lms_bot DECIMAL(5, 2) DEFAULT 0,
    agility_bot DECIMAL(5, 2) DEFAULT 0,
    wintertodt_bot DECIMAL(5, 2) DEFAULT 0,
    runecrafting_bot DECIMAL(5, 2) DEFAULT 0,
    zalcano_bot DECIMAL(5, 2) DEFAULT 0,
    woodcutting_bot DECIMAL(5, 2) DEFAULT 0,
    thieving_bot DECIMAL(5, 2) DEFAULT 0,
    soul_wars_bot DECIMAL(5, 2) DEFAULT 0,
    cooking_bot DECIMAL(5, 2) DEFAULT 0,
    vorkath_bot DECIMAL(5, 2) DEFAULT 0,
    barrows_bot DECIMAL(5, 2) DEFAULT 0,
    herblore_bot DECIMAL(5, 2) DEFAULT 0,
    unknown_bot DECIMAL(5, 2) DEFAULT 0
);
-- Create a table for Feedback
CREATE TABLE PredictionFeedback (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ts TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    -- Add comments for clarity
    voter_id INT NOT NULL,
    subject_id INT NOT NULL,
    prediction VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    vote INT NOT NULL DEFAULT '0',
    -- Add comments for clarity
    feedback_text TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
    reviewed TINYINT NOT NULL DEFAULT '0',
    -- Add comments for clarity
    reviewer_id INT DEFAULT NULL,
    user_notified TINYINT NOT NULL DEFAULT '0',
    -- Add comments for clarity
    proposed_label VARCHAR(50) DEFAULT NULL,
    -- Add comments for clarity
    UNIQUE KEY Unique_Vote (
        prediction,
        subject_id,
        voter_id
    ) USING BTREE,
    -- Add comments for clarity
    KEY Voter_ID (voter_id),
    KEY Subject_ID (subject_id),
    KEY Reviewer_ID (reviewer_id),
    CONSTRAINT Subject_ID FOREIGN KEY (subject_id) REFERENCES Players (id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    -- Add comments for clarity
    CONSTRAINT Voter_ID FOREIGN KEY (voter_id) REFERENCES Players (id) ON DELETE RESTRICT ON UPDATE RESTRICT -- Add comments for clarity
);