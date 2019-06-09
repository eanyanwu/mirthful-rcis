from mirthful_rcis.dal import datastore
from mirthful_rcis.lib.exceptions import RecordNotFound

def get_users():
    """
    Fetches all users
    """
    return datastore.query(
        'select * '
        'from users ')

def get_user_record(user_id):
    user = datastore.query(
        'select * from users '
        'where user_id = ? '
        'limit 1', (user_id,),
        one=True)
    
    if user is None:
        raise RecordNotFound()
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
        raise RecordNotFound()
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
        raise RecordNotFound()
    else:
        return damage


