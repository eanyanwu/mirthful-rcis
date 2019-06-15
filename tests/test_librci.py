from mirthful_rcis import get_db
from mirthful_rcis.dal.datastore import DbTransaction 
from mirthful_rcis.lib import librci
from mirthful_rcis.lib.exceptions import RecordNotFound

import pytest
from uuid import uuid4

def test_get_rci_by_id_BUT_rci_id_is_invalid(app):
    """
    Assert that the right exceptions are thrown when given invalid data
    """
    with app.app_context():
        with pytest.raises(RecordNotFound) as e1:
            librci.get_rci_by_id(rci_id=str(uuid4()))

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
        with DbTransaction() as conn:
            conn.execute(
                'delete from users where user_id = ? ',
                (collaborator['user_id'],))


        full_rci = librci.get_rci_by_id(rci_id=rci['rci_id'], full=True)

    # Assert that since the user has been deleted, they no longer appear as a
    # collaborator
    assert len(full_rci['collaborators']) == 0

    # Asser that even though the user has been deleted, the damage they entered
    # is still present
    assert len(full_rci['damages'].keys()) == 1



def test_get_rci_by_id_full(app, rci):
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
