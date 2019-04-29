-- Delete the tables 
-- Disable the foreign key constraint first, so we can delete
-- the tables in arbitrary order

PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS roles;
DROP TABLE IF EXISTS rooms;
DROP TABLE IF EXISTS role_assignments;
DROP TABLE IF EXISTS rci_documents;
DROP TABLE IF EXISTS rci_attachments;

DROP TABLE IF EXISTS user_acl_owners;
DROP TABLE IF EXISTS user_acl_groups;
DROP TABLE IF EXISTS role_acl_owners;
DROP TABLE IF EXISTS role_acl_groups;
DROP TABLE IF EXISTS rci_document_acl_owners;
DROP TABLE IF EXISTS rci_document_acl_groups;

DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS event_log;

PRAGMA foreign_keys = ON;

-- Recreate them 
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL,
    salt TEXT NOT NULL,
    password TEXT NOT NULL,
    access_control TEXT NOT NULL
);

CREATE TABLE roles(
    role_id TEXT PRIMARY KEY,
    role_name TEXT NOT NULL,
    access_control TEXT NOT NULL
);

CREATE TABLE rooms(
    room_id TEXT PRIMARY KEY,
    room_name TEXT NOT NULL
);

CREATE TABLE role_assignments(
    user_id NOT NULL,
    role_id NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(role_id) REFERENCES roles(role_id)
);

CREATE TABLE rci_documents (
    rci_document_id TEXT PRIMARY KEY,
    room_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    access_control TEXT NOT NULL,
    FOREIGN KEY(room_id) REFERENCES rooms(room_id)
);

CREATE TABLE rci_attachments (
    rci_attachment_id TEXT PRIMARY KEY,
    rci_document_id TEXT NOT NULL,
    rci_attachment_type TEXT NOT NULL,
    content TEXT NOT NULL,
    user_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY(rci_document_id) REFERENCES rci_documents(rci_document_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE user_acl_owners (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    acl_owner_id TEXT NOT NULL,
    UNIQUE (user_id, acl_owner_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (acl_owner_id) REFERENCES users(user_id)
);

CREATE TABLE user_acl_groups (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    acl_group_id NOT NULL,
    UNIQUE (user_id, acl_group_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (acl_group_id) REFERENCES roles(role_id)
);

CREATE TABLE role_acl_owners (
    id INTEGER PRIMARY KEY,
    role_id TEXT NOT NULL,
    acl_owner_id TEXT NOT NULL,
    UNIQUE (role_id, acl_owner_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id),
    FOREIGN KEY (acl_owner_id) REFERENCES users(user_id)
);

CREATE TABLE role_acl_groups (
    id INTEGER PRIMARY KEY,
    role_id TEXT NOT NULL,
    acl_group_id TEXT NOT NULL,
    UNIQUE (role_id, acl_group_id),
    FOREIGN KEY (role_id) REFERENCES roles(role_id),
    FOREIGN KEY (acl_group_id) REFERENCES roles(role_id)
);

CREATE TABLE rci_document_acl_owners (
    id INTEGER PRIMARY KEY,
    rci_document_id TEXT NOT NULL,
    acl_owner_id TEXT NOT NULL,
    FOREIGN KEY (rci_document_id) REFERENCES rci_documents(rci_document_id),
    FOREIGN KEY (acl_owner_id) REFERENCES users(user_id)
);

CREATE TABLE rci_document_acl_groups (
    id INTEGER PRIMARY KEY,
    rci_document_id TEXT NOT NULL,
    acl_group_id TEXT NOT NULL,
    FOREIGN KEY (rci_document_id) REFERENCES rci_documents(rci_document_id),
    FOREIGN KEY (acl_group_id) REFERENCES roles(role_id)
);

CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL, 
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE event_log (
    id INTEGER PRIMARY KEY, -- implicit autoincrement
    event_name TEXT NOT NULL,
    event_contents TEXT
);
