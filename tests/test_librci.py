from mirthful_rcis import get_db
from mirthful_rcis.dal.datastore import DbTransaction 
from mirthful_rcis.lib import librci
from mirthful_rcis.lib.exceptions import RecordNotFound, Unauthorized
from mirthful_rcis.lib.authorization import Permission

import pytest
from uuid import uuid4

def test_get_rci_by_id_BUT_rci_id_is_invalid(app):
    """
    Assert that the right exceptions are thrown when given invalid data
    """
    with app.app_context():
        with pytest.raises(RecordNotFound) as e1:
            librci.get_rci_by_id(rci_id=str(uuid4()))
    
    with app.app_context():
        with pytest.raises(ValueError) as e2:
            librci.get_rci_by_id(rci_id=uuid4())

    assert 'No such rci' in str(e1)
    assert 'not a valid id' in str(e2)

def test_get_rci_by_id_BUT_user_does_not_exist_anymore(app, rci):
    """
    An rci should still be valid when a collaborator gone.
    Put another way: if a user is deleted, their rcis and damages must remain
    """
    with app.app_context():
        full_rci = librci.get_rci_by_id(rci_id=rci['rci_id'], full=True)

    # Assert that we indeed have one damage
    assert len(full_rci['damages'].keys()) == 1

    collaborator = full_rci['collaborators'][0]

    # Delete the user that created the rci
    with app.app_context():
        with DbTransaction() as conn:
            conn.execute(
                'delete from users where user_id = ? ',
                (collaborator['user_id'],))


    with app.app_context():
        full_rci = librci.get_rci_by_id(rci_id=rci['rci_id'], full=True)

    # Assert that since the user has been deleted, they no longer appear as a
    # collaborator
    assert len(full_rci['collaborators']) == 0

    # Assert that even though the user has been deleted, the damage they entered
    # is still present
    assert len(full_rci['damages'].keys()) == 1

    damaged_item = list(full_rci['damages'].keys())[0]
    damage = full_rci['damages'][damaged_item][0]

    assert damage['firstname'] == 'DELETED'
    assert damage['lastname'] == 'USER'



def test_get_rci_by_id(app, rci):
    """
    A full rci should contain more fields than the normal record
    Assert that these fields are present in the full rci, but not in the normal
    one
    """
    with app.app_context():
        full_rci = librci.get_rci_by_id(rci_id=rci['rci_id'], full=True)

    assert 'collaborators' in full_rci
    assert 'damages' in full_rci

    with app.app_context():
        rci = librci.get_rci_by_id(rci_id=rci['rci_id'], full=False)

    assert 'collaborators' not in rci
    assert 'damages' not in rci

def test_get_rcis_for_user_BUT_user_id_is_invalid(app):
    """
    Assert that the right exceptions are thrown when given invalid data
    """
    with app.app_context():
        with pytest.raises(RecordNotFound) as e1:
            librci.get_rcis_for_user(str(uuid4()))

    with app.app_context():
        with pytest.raises(ValueError) as e2:
            librci.get_rcis_for_user(uuid4())

    assert 'No such user' in str(e1)
    assert 'not a valid id' in str(e2)


def test_get_rcis_for_user(app, rci):
    """
    Assert that the function fetches the expected rci(s)
    The creator of the fixture rci is also a collaborator.
    So we expect the same rci to be fetched when use use the creator's user_id
    to fetch rcis
    """

    with app.app_context():
        rcis = librci.get_rcis_for_user(rci['created_by'])

    assert len(rcis) == 1
    assert rcis[0]['rci_id'] == rci['rci_id']


def test_get_rcis_for_buildings_BUT_building_does_not_exist(app):
    """
    Assert that searching for invalid buildings yields no results
    """
    with app.app_context():
        result = librci.get_rcis_for_buildings(buildings=['invalid-building'])
    
    assert len(result) == 0


def test_get_rcis_for_buildings(app, rci_factory):
    """
    Assert that trying to get rcis for a list of buildings works as expected
    """

    rci1 = rci_factory()
    rci2 = rci_factory()

    building1 = rci1['building_name']
    building2 = rci2['building_name']

    # Just showing that these two buildings are different
    assert building1 != building2

    with app.app_context():
        results = librci.get_rcis_for_buildings(buildings=
                                                    [building1, building2])

    assert len(results) == 2


def test_search_rcis_BUT_invalid_input(app):
    """
    Make sure that input such as `None` or an empty string don't blow up the
    search. 
    If the search function can't find anything, or make sense of the input, it
    should just return an empty list instead of raising an exception.
    """

    with app.app_context():
        result1 = librci.search_rcis(None)
        result2 = librci.search_rcis("")

    assert len(result1) == 0
    assert len(result2) == 0


def test_search_rcis(app, rci):
    """
    After an rci has been created, we should be able to search for it
    by building name, room name, and by username of name of a collaborator

    Also, verify that we can do partial searches using `*`
    """
    room_name = rci['room_name']
    building_name = rci['building_name']

    
    with app.app_context():
        db = get_db()
        collaborator = db.execute(
            'select u.* from rci_collabs as r '
            'inner join users as u using(user_id) '
            'where r.rci_id = ?',
            (rci['rci_id'],)).fetchone()

        assert len(librci.search_rcis(room_name)) == 1
        assert len(librci.search_rcis(building_name)) == 1
        assert len(librci.search_rcis(collaborator['firstname'])) == 1
        assert len(librci.search_rcis(collaborator['lastname'])) == 1
        assert len(librci.search_rcis(collaborator['username'])) == 1


def test_create_rci(app, user_factory, room):
    """
    Assert that users without the MODERATE_RCIS permission cannot create an rci
    for someone other than themselves.
    Assert that users with the MODERATE_RCIS permission can create rcis for others
    """
    user1 = user_factory() 
    user2 = user_factory(permissions=Permission.MODERATE_RCIS)

    with app.app_context():
        # user1 can create an rci for themselves
        rci = librci.create_rci(user_id=user1['user_id'],
                          building_name=room['building_name'],
                          room_name=room['room_name'],
                          logged_in_user=user1)

        assert rci['created_by'] == user1['user_id']

        # user1 can't create an rci for someone else
        with pytest.raises(Unauthorized) as e:
            librci.create_rci(user_id=user2['user_id'],
                              building_name=room['building_name'],
                              room_name=room['room_name'],
                              logged_in_user=user1)

            assert 'do not have permissions' in str(e)

        # user2 can create rci for someone else 
        rci = librci.create_rci(user_id=user1['user_id'],
                          building_name=room['building_name'],
                          room_name=room['room_name'],
                          logged_in_user=user2)

        assert rci['created_by'] == user2['user_id']


def test_lock_rci(app, rci_factory, user_factory):
    """
    Assert that users without the MODERATE_RCIS permission cannot lock an rci
    Assert that users with the MODERATE_RCIS permission can lock rcis
    """
    user1 = user_factory() 
    user2 = user_factory(permissions=Permission.MODERATE_RCIS)

    with app.app_context():
        # user1 can't lock an rci 
        with pytest.raises(Unauthorized) as e:
            librci.lock_rci(rci_id=rci_factory()['rci_id'],
                            logged_in_user=user1)

        assert 'You do not have sufficient permissions' in str(e)

        # user2 can lock an rci
        librci.lock_rci(rci_id=rci_factory()['rci_id'],
                        logged_in_user=user2)


def test_unlock_rci(app, rci_factory, user_factory):
    """
    Assert that users without the MODERATE_RCIS permission cannot unlock an rci
    Assert that users with the MODERATE_RCIS permission can unlock rcis
    """

    user1 = user_factory() 
    user2 = user_factory(permissions=Permission.MODERATE_RCIS)

    with app.app_context():
        # user1 can't unlock an rci 
        with pytest.raises(Unauthorized) as e:
            librci.unlock_rci(rci_id=rci_factory()['rci_id'],
                            logged_in_user=user1)

        assert 'You do not have sufficient permissions' in str(e)

        # user2 can unlock an rci
        librci.unlock_rci(rci_id=rci_factory()['rci_id'],
                        logged_in_user=user2)
