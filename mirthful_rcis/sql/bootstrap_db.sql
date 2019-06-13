-- Setup any records that need to be present for the application to function 

PRAGMA foreign_keys = ON;

INSERT INTO roles (role, description, permissions)
VALUES ('student', 'A college student', 0);

INSERT INTO roles (role, description, permissions)
VALUES ('res_life_staff', 'Member of Residence Life Staff', 3);

INSERT INTO roles (role, description, permissions)
VALUES ('admin', 'Residence Life Director', 3);



-- Records for testing

-- Users
INSERT INTO users 
VALUES ('32151344-dfa6-4e70-89b1-140d756c0079',
    'test_student',
    'John',
    'Riley',
    'test',
    'test_student',
    'student');

INSERT INTO users
VALUES ('fcd02d33-ca85-4246-ab66-25cb67188360',
    'test_staff',
    'Libbie',
    'Wamble',
    'test',
    'test_staff',
    'res_life_staff');

INSERT INTO users
VALUES ('6a134499-3c0a-4f24-93c6-ac936508a0ff',
    'test_admin',
    'Clayton',
    'Bernos',
    'test',
    'test_admin',
    'admin');

-- Rooms
INSERT INTO rooms
VALUES ('Nyland', '210');

INSERT INTO rooms
VALUES ('Fulton', '211');

INSERT INTO rooms
VALUES ('Fulton', '101');


-- Walkthrough Items
INSERT INTO room_areas
VALUES ('Door(s)/Doorframe/Locks', 'Anything damages around the room entrance');

INSERT INTO room_areas
VALUES('Carpet/Floor', 'Stains, scratchs, and other imperfections');

INSERT INTO room_areas
VALUES('Walls', 'Discollorations, nail holes, paint chips ... ');

INSERT INTO room_areas
VALUES('Desks/Chair', 'Any missing furniture, broken drawers etc...');
