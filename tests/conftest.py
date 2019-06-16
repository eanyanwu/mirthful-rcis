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


@pytest.fixture
def user(user_factory):
    return user_factory()


@pytest.fixture
def rci(rci_factory):
    return rci_factory()

@pytest.fixture
def room(room_factory):
    return room_factory()

@pytest.fixture
def user_factory(app):
    def _make_user(permissions=0):
        random_string = str(uuid.uuid4())


        with app.app_context():
            db_connection = get_db()

            username = 'username_{}'.format(random_string)
            password = 'password_{}'.format(random_string)

            role = _create_role(db_connection=db_connection,
                                permissions=permissions)

            return _create_user(db_connection=db_connection, 
                                username=username,
                                password=password,
                                role=role['role'])

    return _make_user


@pytest.fixture
def rci_factory(app):
    def _make_rci(locked=False):
        id = str(uuid.uuid4())

        username = 'username_{}'.format(id)
        password = 'password_{}'.format(id)
        room_name = 'room_{}'.format(id)
        building_name = 'building_{}'.format(id)
        damage_item = 'item_{}'.format(id)
        damage_text = 'text_{}'.format(id)
        damage_url = 'http://url_{}'.format(id)
        is_locked = 1 if locked else 0
    
        with app.app_context():
            db = get_db()

            role = _create_role(db, permissions=0)

            user = _create_user(db,
                                username=username,
                                password=password,
                                role=role['role'])

            room = _create_room(db,
                                room_name=room_name,
                                building_name=building_name)

            rci = _create_rci(db,
                              building_name=building_name,
                              room_name=room_name,
                              created_by=user['user_id'],
                              is_locked=is_locked)

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

@pytest.fixture
def room_factory(app):
    def _make_room():
        random_id = str(uuid.uuid4())
        
        with app.app_context():
            db = get_db()
            room_name = 'room_{}'.format(random_id)
            building_name = 'building_{}'.format(random_id)

            room = _create_room(db_connection=db,
                                building_name=building_name,
                                room_name=room_name)
        return room

    return _make_room

@pytest.fixture
def room_area_factory(app):
    def _make_room_area(name):
        with app.app_context():
            db = get_db()
            room_area = _create_room_area(db_connection=db,
                                          name=name)

        return room_area
    
    return _make_room_area


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

def _create_role(db_connection, permissions):
    role = 'role_{}'.format(uuid.uuid4())

    insert_args = {
        'role': role,
        'description': 'A test role',
        'permissions': permissions
    }

    db_connection.execute(
        'insert into roles (role, description, permissions) '
        'values (:role, :description, :permissions) ',
        insert_args)

    db_connection.commit()

    results = db_connection.execute(
        'select * '
        'from roles '
        'where role = ?',
        (role,))

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
                created_by,
                is_locked):

    rci_id = str(uuid.uuid4())
    
    insert_args = {
        'rci_id': rci_id,
        'building_name': building_name,
        'room_name': room_name,
        'created_at': datetime.utcnow(),
        'created_by': created_by,
        'is_locked': is_locked
    }

    db_connection.execute(
        'insert into rcis '
        '(rci_id, building_name, room_name, created_at, created_by, is_locked) '
        'values '
        '(:rci_id,:building_name,:room_name,:created_at,:created_by,:is_locked) ',
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

def _create_room_area(db_connection, name):
    insert_args = {
        'room_area_name': name,
        'room_area_description': name
    }

    db_connection.execute(
        'insert into room_areas (room_area_name, room_area_description) '
        'values (:room_area_name,:room_area_description) ',
        insert_args)

    db_connection.commit()

    result = db_connection.execute(
        'select * '
        'from room_areas '
        'where room_area_name = ?',
        (name,))

    return result.fetchone()



