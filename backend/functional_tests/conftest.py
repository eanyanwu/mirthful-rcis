import datastore

from app import app

import os.path
import pytest
import sqlite3
import uuid
import tempfile

@pytest.fixture
def test_db():
    """
    Fixture for providing a test database for tests to use

    This is done by creating a tempfile and using that as the connection
    string for `datastore.DATABASE` (essentially setting a global variable)

    Any time a Dbtransaction is created, it will use the given temporary file
    as its database
    """
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

    # Populate the tables
    conn = sqlite3.connect(file_name)
    conn.row_factory = datastore.dict_factory

    conn.executescript(schema_sql)
    conn.executescript(bootstrap_sql)

    conn.commit()

    # Give up control -- at this point, the test db is ready
    yield conn

    # Clean up the temporary file
    os.close(file_handle)
    


@pytest.fixture
def flask_client():
    """
    Fixture for providing a test client for the tests to use
    """
    # Get a test client
    client = app.test_client()

    client.testing = True

    # We also define convenience method `login_as` and `logout` on
    # this client.
    def login_as(user):
        response = client.post(
            '/login',
            data={
                'username': user['username'],
                'password': user['password']
            })

        return response

    def logout():
        response = client.post('/logout')

        return response

    client.login_as = login_as
    client.logout = logout

    yield client

@pytest.fixture
def student(test_db):
    """
    Fixture for providing a student for the tests to use
    """
    return create_user_core('student', test_db)

@pytest.fixture
def res_life_staff(test_db):
    """
    Fixture for providing a res_life_staff member for the tests to use
    """
    return create_user_core('res_life_staff', test_db)

@pytest.fixture
def user_factory(test_db):
    """
    Fixture factory for creating users

    Useful if the test needs to create more than one user
    """
    def _make_user_record(role):
        return create_user_core(role, test_db)

    return _make_user_record 


@pytest.fixture
def room(test_db):
    """
    Fixture for providing a room for the tests to use
    """
    return create_room_core(test_db)


def create_room_core(db_connection):
    """
    Helper function for creating a room
    """

    room_id = str(uuid.uuid4())

    insert_args = {
        'room_id': room_id,
        'room_name': 'room_number_{}'.format(room_id),
        'building_name': 'Nyland'
    }

    db_connection.execute(
        'insert into rooms(room_id, room_name, building_name) '
        'values (:room_id, :room_name, :building_name) ',
        insert_args)

    db_connection.commit() # Don't forget to call commit

    results = db_connection.execute(
        'select * '
        'from rooms '
        'where room_id = ? '
        'limit 1;',
        (room_id,))

    return results.fetchone()


# Note that this is a raw sqlite3 db connection 
# So you manually need to call commit
def create_user_core(role, db_connection):
    """
    Helper function for creating a user 
    """
    user_id = str(uuid.uuid4())
    
    insert_args = {
        'user_id': user_id,
        'username': 'test_user_{}'.format(user_id),
        'salt': 'test_salt_{}'.format(user_id),
        'password': 'test_password_{}'.format(user_id),
        'role': role 
    }

    db_connection.execute(
        'insert into users(user_id, username, salt, password, role) '
        'values(:user_id, :username, :salt, :password, :role) ',
        insert_args)

    db_connection.commit() # Don't forget to call commit

    results = db_connection.execute(
        'select * '
        'from users '
        'where user_id = ? '
        'limit 1;',
        (user_id,))

    return results.fetchone() 
