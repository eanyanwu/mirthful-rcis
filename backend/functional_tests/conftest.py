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


@pytest.fixture
def user_factory():
    """
    Fixture factory for creating and providing a test user

    We are using a factory because we need the flask application context
    To actually  interact with the database. This fixture doesn't have 
    access to the context, but the tests that use it will
    """
    def _make_user_record():
        user_id = str(uuid.uuid4())
        datastore.insert_user(
            user_id=user_id,
            username='test_user_{}'.format(user_id),
            salt='salt',
            password='password',
            access_control='o:rw;g:rw;w:__')

        user = datastore.select_user(user_id=user_id)

        return user

    return _make_user_record








