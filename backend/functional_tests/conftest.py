import datastore

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
    sql = ''
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file = os.path.join(base_dir, '../sql/reset_db.sql')

    with open(sql_file, 'r') as f:
        sql = f.read()

    # To make any calls to the flask application we need a context
    with client.application.app_context():
        datastore.execute_script(sql)

    yield client

    # Clean up the temporary file
    os.close(file_handle)



# We are using a factory because we need the flask application context
# To actually  interact with the database. This fixture doesn't have 
# access to the context, but the tests that use them will
@pytest.fixture
def user_factory():
    """
    Fixture factory for creating and providing a test user
    """
    def _make_user_record():
        user_id = str(uuid.uuid4())
        
        insert_args = {
            'user_id': user_id,
            'username': 'test_user_{}'.format(user_id),
            'salt': 'test_salt_{}'.format(user_id),
            'password': 'test_password_{}'.format(user_id),
            'access_control': 'o:rw;g:rw;w:__'
        }

        datastore.query(
            'insert into users '
            'values(:user_id, :username, :salt, :password, :access_control) ',
            insert_args)

        user = datastore.query(
            'select * '
            'from users '
            'where user_id = ? '
            'limit 1;',
            (user_id,), one=True)

        return user

    return _make_user_record

@pytest.fixture
def room_factory():
    """
    Fixture factory for creating and providing a test room
    """
    def _make_room_record():
        room_id = str(uuid.uuid4())

        insert_args = {
            'room_id': room_id,
            'room_name': 'test_room_{}'.format(room_id)
        }

        datastore.query(
            'insert into rooms '
            'values (:room_id, :room_name) ',
            insert_args)

        room  = datastore.query(
            'select * '
            'from rooms '
            'where room_id = ? '
            'limit 1;',
            (room_id,), one=True)

        return room

    return _make_room_record








