from mirthful_rcis.dal import datastore
from mirthful_rcis.lib.exceptions import RecordNotFound

import uuid

def get_users():
    """
    Fetches all users
    """
    return datastore.query(
        'select * '
        'from users ')


def get_rci_collaborators(rci_id):
    """
    List the collaborators for an rci
    """
    return datastore.query(
        'select * ' 
        'from rci_collabs '
        'where rci_id = ?',
        (rci_id,))


def get_user_record(user_id):
    user = datastore.query(
        'select * from users '
        'where user_id = ? '
        'limit 1', (user_id,),
        one=True)
    
    if user is None:
        raise RecordNotFound('No such user {}'.format(user_id))
    else:
        return user

def get_rci_record(rci_id):
    rci = datastore.query(
        'select * from rcis '
        'where rci_id = ? '
        'limit 1',
        (rci_id,),
        one=True)

    if rci is None:
        raise RecordNotFound('No such rci {}'.format(rci_id))
    else:
        return rci


def get_damage_record(damage_id):
    damage = datastore.query(
        'select * '
        'from damages '
        'where damage_id = ?', 
        (damage_id,),
        one=True)

    if damage is None:
        raise RecordNotFound('No such damage {}'.format(damage_id))
    else:
        return damage


def is_uuid(thing):
    """
    Is `thing` a UUID?
    """

    if thing is None:
        return False 

    try:
        uuid.UUID(thing)
        return True 
    except:
        return False 
