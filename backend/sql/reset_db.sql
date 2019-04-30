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

DROP TABLE IF EXISTS sessions;

PRAGMA foreign_keys = ON;

-- Recreate them 

CREATE TABLE roles(
    role TEXT PRIMARY KEY,
    description TEXT,
    permissions TEXT
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
    room_id TEXT PRIMARY KEY,
    room TEXT NOT NULL,
    building TEXT NOT NULL,

    UNIQUE (room, building)
);

CREATE TABLE rcis (
    rci_id TEXT PRIMARY KEY,
    room_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    is_locked INTEGER NOT NULl DEFAULT 0,

    FOREIGN KEY(room_id) REFERENCES rooms(room_id)
);

CREATE TABLE rci_collabs (
    rci_collab_id TEXT PRIMARY KEY,
    rci_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    
    UNIQUE (rci_id, user_id),
    FOREIGN KEY(rci_id) REFERENCES rcis(rci_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE damages (
    damage_id TEXT PRIMARY KEY,
    rci_id TEXT NOT NULL,
    text TEXT NOT NULL,
    image_url TEXT,
    user_id TEXT NOT NULL,
    created_at TEXT NOT NULL,

    FOREIGN KEY(rci_id) REFERENCES rcis(rci_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL, 
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,

    FOREIGN KEY(user_id) REFERENCES users(user_id)
);
