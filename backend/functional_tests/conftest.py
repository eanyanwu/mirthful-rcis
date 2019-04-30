import datastore
import controllers

from app import app

import os.path
import pytest
import sqlite3
import uuid
import tempfile

@pytest.fixture
def client():
    """
    Fixture for providing a test client for the tests to use
    """
    # Get a test client
    # TODO: Learn more about what this does
    client = app.test_client()
    client.testing = True

    # Create a temporary file that will be used
    # for our test db
    file_handle, file_name = tempfile.mkstemp()

    # Set the database name
    datastore.DATABASE = file_name 
   
    # Setup our tables
    schema_sql = ''
    bootstrap_sql = ''
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_sql_file = os.path.join(base_dir, '../sql/reset_db.sql')
    test_data_sql_file = os.path.join(base_dir, '../sql/bootstrap_db.sql')

    with open(schema_sql_file, 'r') as f:
        schema_sql = f.read()

    with open(test_data_sql_file, 'r') as f:
        bootstrap_sql = f.read()

    with client.application.app_context():
        datastore.execute_script(schema_sql)
        datastore.execute_script(bootstrap_sql)

    yield client

    # Clean up the temporary file
    os.close(file_handle)

@pytest.fixture
def student():
    """
    Fixture for providing a student for the tests to use
    """

    test_client = app.test_client()

    with test_client.application.app_context():
        student = create_user('student')

    return student

@pytest.fixture
def room():
    """
    Fixture for providing a room for the tests to use
    """

    test_client = app.test_client()

    with test_client.application.app_context():
        room_id = str(uuid.uuid4())

        insert_args = {
            'room_id': room_id,
            'room': 'room_number_{}'.format(room_id),
            'building': 'Nyland'
        }

        datastore.query(
            'insert into rooms(room_id, room, building) '
            'values (:room_id, :room, :building) ',
            insert_args)

        room  = datastore.query(
            'select * '
            'from rooms '
            'where room_id = ? '
            'limit 1;',
            (room_id,), one=True)

        return room


def create_user(role):
    user_id = str(uuid.uuid4())
    
    insert_args = {
        'user_id': user_id,
        'username': 'test_user_{}'.format(user_id),
        'salt': 'test_salt_{}'.format(user_id),
        'password': 'test_password_{}'.format(user_id),
        'role': role 
    }

    datastore.query(
        'insert into users(user_id, username, salt, password, role) '
        'values(:user_id, :username, :salt, :password, :role) ',
        insert_args)

    user = datastore.query(
        'select * '
        'from users '
        'where user_id = ? '
        'limit 1;',
        (user_id,), one=True)

    return user

