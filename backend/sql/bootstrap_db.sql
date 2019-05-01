-- Setup any records that need to be present for the application to function 

INSERT INTO roles (role, description, permissions)
VALUES ('student', 'A college student', 0);

INSERT INTO roles (role, description, permissions)
VALUES ('res_life_staff', 'Member of Residence Life Staff', 3);

INSERT INTO roles (role, description, permissions)
VALUES ('admin', 'Residence Life Director', 4);
