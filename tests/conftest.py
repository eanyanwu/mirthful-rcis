from mirthful_rcis import (
    create_app, 
    get_db,
    initialize_database,
    populate_database_with_test_data
)

import os
import pytest
import tempfile
import uuid

from datetime import datetime


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
    with app.app_context():
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

@pytest.fixture
def rci(app, rci_factory):
    return rci_factory()

@pytest.fixture
def rci_factory(app):
    def _make_rci(user_role='student'):
        id = str(uuid.uuid4())

        username = 'username_{}'.format(id)
        password = 'password_{}'.format(id)
        room_name = 'room_{}'.format(id)
        building_name = 'building_{}'.format(id)
        damage_item = 'item_{}'.format(id)
        damage_text = 'text_{}'.format(id)
        damage_url = 'http://url_{}'.format(id)

        with app.app_context():
            db = get_db()
            user = _create_user(db,
                                username=username,
                                password=password,
                                role=user_role)
            room = _create_room(db,
                                room_name=room_name,
                                building_name=building_name)

            rci = _create_rci(db,
                              building_name=building_name,
                              room_name=room_name,
                              created_by=user['user_id'])

            damage = _create_damage(db,
                                    rci_id=rci['rci_id'],
                                    item=damage_item,
                                    text=damage_text,
                                    image_url=damage_url,
                                    created_by=user['user_id'])

            collab = _create_rci_collab(db,
                                        rci_id=rci['rci_id'],
                                        user_id=user['user_id'])

            return rci

    return _make_rci


def _create_room(db_connection, building_name, room_name):

    insert_args = {
        'building_name': building_name,
        'room_name': room_name
    }

    db_connection.execute(
        'insert into rooms (building_name, room_name) '
        'values (:building_name, :room_name)',
        insert_args)

    db_connection.commit()

    results = db_connection.execute(
        'select * '
        'from rooms '
        'where building_name = ? '
        'and room_name = ? '
        'limit 1', 
        (building_name, room_name))

    return results.fetchone()


def _create_user(db_connection, username, password, role):
    user_id = str(uuid.uuid4())

    insert_args = {
        'user_id': user_id,
        'username': username,
        'firstname': '{}_firstname'.format(username),
        'lastname': '{}_lastname'.format(username),
        'salt': 'test',
        'password': password,
        'role': role
    }

    db_connection.execute(
        'insert into users '
        '(user_id, username, firstname, lastname, salt, password, role) '
        'values '
        '(:user_id,:username,:firstname,:lastname,:salt,:password,:role) ',
        insert_args)

    db_connection.commit()

    results = db_connection.execute(
        'select * '
        'from users '
        'where user_id = ? '
        'limit 1 ',(user_id,))

    return results.fetchone()


def _create_rci(db_connection,
                building_name,
                room_name,
                created_by):

    rci_id = str(uuid.uuid4())
    
    insert_args = {
        'rci_id': rci_id,
        'building_name': building_name,
        'room_name': room_name,
        'created_at': datetime.utcnow(),
        'created_by': created_by 
    }

    db_connection.execute(
        'insert into rcis '
        '(rci_id, building_name, room_name, created_at, created_by) '
        'values '
        '(:rci_id,:building_name,:room_name,:created_at,:created_by) ',
        insert_args)

    db_connection.commit()

    results = db_connection.execute(
        'select * '
        'from rcis '
        'where rci_id = ? '
        'limit 1 ',
        (rci_id,))

    return results.fetchone()

def _create_rci_collab(db_connection, rci_id, user_id):
    insert_args = {
        'rci_id': rci_id,
        'user_id': user_id
    }

    db_connection.execute(
        'insert into rci_collabs (user_id, rci_id) '
        'values (:user_id, :rci_id) ',
        insert_args)

    db_connection.commit()

    results = db_connection.execute(
        'select * '
        'from rci_collabs '
        'where rci_id = ? '
        'and user_id = ? '
        'limit 1 ',
        (rci_id, user_id))

    return results.fetchone()


def _create_damage(db_connection,
                   rci_id,
                   item,
                   text,
                   image_url,
                   created_by):
    damage_id = str(uuid.uuid4())

    insert_args = {
        'damage_id': damage_id,
        'rci_id': rci_id,
        'item': item,
        'text': text,
        'image_url': image_url,
        'created_by': created_by,
        'created_at': datetime.utcnow()
    }

    db_connection.execute(
        'insert into damages '
        '(damage_id, rci_id, item, text, image_url, created_at, created_by) '
        'values '
        '(:damage_id,:rci_id,:item,:text,:image_url,:created_at,:created_by) ',
        insert_args)

    db_connection.commit()

    results = db_connection.execute(
        'select * from damages where damage_id = ?',
        (damage_id,))

    return results.fetchone()


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

