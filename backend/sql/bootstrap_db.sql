-- Setup any records that need to be present for the application to function 

PRAGMA foreign_keys = ON;

INSERT INTO roles (role, description, permissions)
VALUES ('student', 'A college student', 0);

INSERT INTO roles (role, description, permissions)
VALUES ('res_life_staff', 'Member of Residence Life Staff', 3);

INSERT INTO roles (role, description, permissions)
VALUES ('admin', 'Residence Life Director', 4);



-- Records for testing

INSERT INTO users 
VALUES ('32151344-dfa6-4e70-89b1-140d756c0079',
    'test_student',
    'test',
    'test_student',
    'student');

INSERT INTO users
VALUES ('fcd02d33-ca85-4246-ab66-25cb67188360',
    'test_staff',
    'test',
    'test_staff',
    'res_life_staff');

