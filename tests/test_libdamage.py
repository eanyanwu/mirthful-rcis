from mirthful_rcis import get_db
from mirthful_rcis.lib import libdamage
from mirthful_rcis.lib.authorization import Permission
from mirthful_rcis.lib.exceptions import Unauthorized

import pytest

def test_create_damage_BUT_user_has_no_special_permissions(app,
                                                           user_factory,
                                                           rci):
    """
    When the user has no special permissions, they can only create 
    a damage entry on an rci in which they are listed as a collaborator.
    """
    with app.app_context():
        # user with not special permissions
        user = user_factory()
        # a collaborator for the rci 
        rci_collaborator = get_db().execute(
            'select u.* '
            'from rci_collabs as rc '
            'inner join users as u '
            'using(user_id) '
            'where rc.rci_id = ?',
            (rci['rci_id'],)).fetchone()

        # only the collaborator should be able to add a damage
        with pytest.raises(Unauthorized) as e:
            libdamage.create_damage(logged_in_user=user,
                                    rci_id=rci['rci_id'],
                                    item='Door',
                                    text='It is missing',
                                    image_url=None)
        assert 'cannot record damage' in str(e)

        damage = libdamage.create_damage(logged_in_user=rci_collaborator,
                                         rci_id=rci['rci_id'],
                                         item='Door',
                                         text='It is missing',
                                         image_url=None)

        assert damage['created_by'] == rci_collaborator['user_id']



def test_create_damage_BUT_user_has_MODERATE_DAMAGES_permission(app,
                                                                user_factory,
                                                                rci):
    """
    A user with the MODERATE_DAMAGES permission can add damages to any unlocked
    rci
    """

    with app.app_context():
        user = user_factory(permissions=Permission.MODERATE_DAMAGES)

        damage = libdamage.create_damage(logged_in_user=user,
                                rci_id=rci['rci_id'],
                                item='Door',
                                text='It is missing',
                                image_url=None)

        assert damage['created_by'] == user['user_id']


def test_create_damage_BUT_rci_is_locked(app,
                                         user_factory,
                                         rci_factory):
    """
    A locked rci cannot have damages added to it.
    """

    locked_rci = rci_factory(locked=True)

    with app.app_context():
        user = user_factory(permissions=Permission.MODERATE_DAMAGES)

        with pytest.raises(Unauthorized) as e:
            libdamage.create_damage(logged_in_user=user,
                                    rci_id=locked_rci['rci_id'],
                                    item='Door',
                                    text='It is missing',
                                    image_url=None)

        assert 'is locked' in str(e)
                                         


def test_delete_damage_BUT_user_has_no_special_permissions(app,
                                                           rci,
                                                           user_factory):
    """
    When the user has no special permissions, they can only delete 
    a damage entry from an rci in which they are listed as a collaborator.
    """
    with app.app_context():
        # user with not special permissions
        user = user_factory()
        # a collaborator for the rci 
        rci_collaborator = get_db().execute(
            'select u.* '
            'from rci_collabs as rc '
            'inner join users as u '
            'using(user_id) '
            'where rc.rci_id = ?',
            (rci['rci_id'],)).fetchone()

        damage = get_db().execute(
            'select * from damages where rci_id = ?',
            (rci['rci_id'],)).fetchone()


        # only the collaborator should be able to delete the damage
        with pytest.raises(Unauthorized) as e:
            libdamage.delete_damage(damage_id=damage['damage_id'],
                                    logged_in_user=user)
        assert 'cannot delete damage' in str(e)

        libdamage.delete_damage(damage_id=damage['damage_id'],
                                         logged_in_user=rci_collaborator)


def test_delete_damage_BUT_user_has_MODERATE_DAMAGES_permission(app,
                                                                user_factory,
                                                                rci):
    """
    A user with the MODERATE_DAMAGES permission can delete damages form any
    unlocked rci
    """
    user = user_factory(permissions=Permission.MODERATE_DAMAGES)

    with app.app_context():
        damage = get_db().execute(
            'select * from damages where rci_id = ?',
            (rci['rci_id'],)).fetchone()

        libdamage.delete_damage(damage_id=damage['damage_id'],
                                logged_in_user=user)



def test_delete_damage_BUT_rci_is_locked(app,
                                         user_factory,
                                         rci_factory):

    locked_rci = rci_factory(locked=True)

    user = user_factory(permissions=Permission.MODERATE_DAMAGES)

    with app.app_context():
        damage = get_db().execute(
            'select * from damages where rci_id = ?',
            (locked_rci['rci_id'],)).fetchone()

        with pytest.raises(Unauthorized) as e:
            libdamage.delete_damage(damage_id=damage['damage_id'],
                                    logged_in_user=user)

        assert 'is locked' in str(e)



    
