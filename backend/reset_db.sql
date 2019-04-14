-- Delete the tables 
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS sessions;

-- Recreate them 
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    salt TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

-- Populate with test data
INSERT INTO users (user_id, username, salt, password)
VALUES ('8aececed-eee4-4ddc-af28-c0e1cdb56d80', 'eanyanwu', '1', 'password')

