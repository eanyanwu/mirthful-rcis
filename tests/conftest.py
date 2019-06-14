from mirthful_rcis import (
    create_app, 
    initialize_database,
    populate_database_with_test_data
)

import os
import pytest
import tempfile


@pytest.fixture
def app():
    """
    Fixture: An instance of the mirthful_rcis application
    """

    # Temporary file that will be used as our test database
    file_handle, file_name = tempfile.mkstemp()


    app = create_app({
        'TESTING': True,
        'DATABASE': file_name
    })


    # Setup the database 
    with app.app_context():
        initialize_database()
        populate_database_with_test_data()


    # Give up control. `app` is ready to be used by whatever test uses this
    # fixture
    yield app

    # dispose of the temporary file.
    os.close(file_handle)
    os.unlink(file_name)


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth(client):
    return AuthenticationActions(client)

@pytest.fixture
def dashboard(client):
    return DashboardActions(client)


class AuthenticationActions():
    def __init__(self, client):
        self._client = client

    def login(self, username='test_student', password='test_student'):
        return self._client.post(
            '/auth/login',
            data={'username':username, 'password':password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

class DashboardActions():
    def __init__(self, client):
        self._client = client

    def main(self):
        return self._client.get('/')

