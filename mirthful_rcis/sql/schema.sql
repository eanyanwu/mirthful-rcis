-- Delete the tables 
-- Disable the foreign key constraint first, so we can delete
-- the tables in arbitrary order

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS user_settings;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS room_areas;
DROP TABLE IF EXISTS rcis;
DROP TABLE IF EXISTS  rci_index;
DROP TABLE IF EXISTS rci_collabs;
DROP TABLE IF EXISTS damages;
DROP TABLE IF EXISTS room_areas;
DROP TABLE IF EXISTS sessions;

PRAGMA foreign_keys = ON;

-- Recreate them 

CREATE TABLE roles(
    role TEXT PRIMARY KEY,
    description TEXT,
    permissions INTEGER
);

CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    salt TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    
    FOREIGN KEY(role) REFERENCES roles(role),
    CONSTRAINT unique_username UNIQUE (username)
);

CREATE TABLE user_settings (
    user_id TEXT PRIMARY KEY,
    default_buildings TEXT
);

CREATE TABLE rooms(
    building_name TEXT NOT NULL,
    room_name TEXT NOT NULL,

    PRIMARY KEY (building_name, room_name)
);

CREATE TABLE room_areas(
    room_area_name PRIMARY KEY,
    room_area_description NOT NULL
);

CREATE TABLE rcis (
    rci_id TEXT PRIMARY KEY,
    building_name TEXT NOT NULL,
    room_name TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT, 
    is_locked INTEGER NOT NULL DEFAULT 0,

    -- If the room is deleted, the rci doesn't mean much any longer and it should be safe to delete 
    FOREIGN KEY(building_name, room_name)
    REFERENCES rooms(building_name, room_name) ON DELETE CASCADE,

    -- If the user is deleted, we still want to keep a record of the damages
    FOREIGN KEY (created_by)
    REFERENCES users(user_id) ON DELETE SET NULL 
);


CREATE TABLE rci_collabs (
    rci_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    
    PRIMARY KEY(rci_id, user_id),
    -- If the rci is deleted, we can safely delete all the collaborations
    FOREIGN KEY(rci_id) REFERENCES rcis(rci_id) ON DELETE CASCADE,
    -- If the user is deleted, we can safely delete all his collaborations 
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Full-Text-Search index to use for the search functionality.
CREATE VIRTUAL TABLE rci_index USING fts5(
    rci_id UNINDEXED,
    user_id UNINDEXED,
    building_name,
    room_name,
    username,
    firstname, 
    lastname,
    -- The `-` and `_` characters should also be recognized as tokens instead of separators.
    -- Why? Tests and people who have names with hyphens
    tokenize = "unicode61 tokenchars'-_'"
);

-- Triggers to keep the Full-Text-Search table up to date
-- Note these triggers are for the rci_collabs table.
-- An rci is not associated with anyone until an entry for said user has been added 
-- to the rci_collabs table
CREATE TRIGGER rci_index_ai AFTER INSERT ON rci_collabs
BEGIN
    INSERT INTO rci_index (rci_id, user_id, building_name, room_name, username, firstname, lastname)
    SELECT r.rci_id AS rci_id,
            u.user_id AS user_id,
            r.building_name AS building_name,
            r.room_name AS room_name, 
            u.username AS username,
            u.firstname AS firstname,
            u.lastname AS lastname
    FROM rci_collabs AS rc
    INNER JOIN rcis AS r -- the rcis table has the room and building names
    USING(rci_id)
    INNER JOIN users as u -- the users table has the first and last name
    USING(user_id)
    WHERE r.rci_id = new.rci_id;
END;

CREATE TRIGGER rci_index_ad AFTER DELETE ON rci_collabs
BEGIN
    DELETE FROM rci_index
    WHERE rci_id = old.rci_id and user_id = old.user_id;
END;

-- Note: We never perform update operations on the rci_collabs table, so no need for 
-- a trigger

CREATE TABLE damages (
    damage_id TEXT PRIMARY KEY,
    rci_id TEXT NOT NULL,
    item TEXT NOT NULL,
    text TEXT NOT NULL,
    image_url TEXT,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT, 

    -- If an rci is deleted, we have no more need for the damages recorded within
    FOREIGN KEY(rci_id) REFERENCES rcis(rci_id) ON DELETE CASCADE,
    -- If a user is deleted, we still want to keep track of damages they recorded
    FOREIGN KEY(created_by) REFERENCES users(user_id) ON DELETE SET NULL 
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL, 
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,

    -- If a user is deleted, we can delete any active session they have
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
