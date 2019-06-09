-- Delete the tables 
-- Disable the foreign key constraint first, so we can delete
-- the tables in arbitrary order

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS room_areas;
DROP TABLE IF EXISTS rcis;
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
    
    FOREIGN KEY (role) REFERENCES roles(role)
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
    created_by TEXT NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000',
    is_locked INTEGER NOT NULL DEFAULT 0,

    -- If the room is deleted, the rci doesn't mean much any longer and it should be safe to delete 
    FOREIGN KEY(building_name, room_name)
    REFERENCES rooms(building_name, room_name) ON DELETE CASCADE,

    -- If the user is deleted, we still want to keep a record of the damages
    FOREIGN KEY (created_by)
    REFERENCES users(user_id) ON DELETE SET DEFAULT
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

CREATE TABLE damages (
    damage_id TEXT PRIMARY KEY,
    rci_id TEXT NOT NULL,
    item TEXT NOT NULL,
    text TEXT NOT NULL,
    image_url TEXT,
    created_at TIMESTAMP NOT NULL,
    created_by TEXT NOT NULL DEFAULT '00000000-0000-0000-0000-000000000000',

    -- If an rci is deleted, we have no more need for the damages recorded within
    FOREIGN KEY(rci_id) REFERENCES rcis(rci_id) ON DELETE CASCADE,
    -- If a user is deleted, we still want to keep track of damages they recorded
    FOREIGN KEY(created_by) REFERENCES users(user_id) ON DELETE SET DEFAULT
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL, 
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,

    -- If a user is deleted, we can delete any active session they have
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
