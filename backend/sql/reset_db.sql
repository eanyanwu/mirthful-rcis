-- Delete the tables 
-- Disable the foreign key constraint first, so we can delete
-- the tables in arbitrary order

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS rooms;
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

CREATE TABLE rcis (
    rci_id TEXT PRIMARY KEY,
    building_name TEXT NOT NULL,
    room_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_locked INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY(building_name, room_name)
    REFERENCES rooms(building_name, room_name) ON DELETE CASCADE
);

CREATE TABLE rci_collabs (
    rci_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    
    PRIMARY KEY(rci_id, user_id),
    FOREIGN KEY(rci_id) REFERENCES rcis(rci_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE damages (
    damage_id TEXT PRIMARY KEY,
    rci_id TEXT NOT NULL,
    item TEXT NOT NULL,
    text TEXT NOT NULL,
    image_url TEXT,
    user_id TEXT NOT NULL,
    created_at TEXT NOT NULL,

    FOREIGN KEY(rci_id) REFERENCES rcis(rci_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

CREATE TABLE room_areas (
    area TEXT PRIMARY KEY,
    area_prompt TEXT
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL, 
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
