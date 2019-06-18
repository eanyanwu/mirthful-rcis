from mirthful_rcis.dal import datastore
from mirthful_rcis.lib.common import (
    get_rci_record,
    get_user_record,
    get_rci_collaborators,
    is_uuid
)
from mirthful_rcis.lib.authorization import (
    Permission,
    user_can
)
from mirthful_rcis.lib.exceptions import (
    BadRequest, 
    Unauthorized,
    RecordNotFound
)

import uuid
from datetime import datetime, timedelta

def throw_if_not_valid_uuid(id):
    if is_uuid(id):
        pass
    else:
        raise ValueError('{} is not a valid id'.format(id))


def get_rci_by_id(rci_id, full=False):
    """
    Fetch an rci
    """
    throw_if_not_valid_uuid(rci_id)

    rci = get_rci_record(rci_id)

    if not full:
        return rci

    rci_collaborators = datastore.query(
        'select u.* '
        'from rci_collabs as rc '
        'inner join users as u '
        'using(user_id) '
        'where rc.rci_id = ?',
        (rci_id,))

    damages = datastore.query(
        'select '
        'd.*, '
        'coalesce(u.firstname, \'DELETED\') as firstname, '
        'coalesce(u.lastname, \'USER\') as lastname '
        'from damages as d '
        'left join users as u '
        'on d.created_by = u.user_id '
        'where rci_id =? ',
        (rci_id,))

    damages_by_item = {}

    for damage in damages:
        damages_by_item.setdefault(damage['item'], []).append(damage)

    full_rci_doc = {
        'rci_id': rci_id,
        'collaborators': rci_collaborators,
        'damages': damages_by_item,
        'room_name': rci['room_name'],
        'building_name': rci['building_name'],
        'created_at': rci['created_at'],
        'created_by': rci['created_by'],
        'is_locked': True if rci['is_locked'] == 1 else False
    }

    return full_rci_doc 


def get_rcis_for_user(user_id, logged_in_user):
    """
    Fetch the rcis for which the user `user_id` is a collaborator.
    """

    throw_if_not_valid_uuid(user_id)

    # You can only lookup rcis for a user if
    # 1 - That user is you OR 
    # 2 - You have permissions to MODERATE_RCIS
    if (user_can(Permission.MODERATE_RCIS, logged_in_user)):
        pass
    else:
        if user_id != logged_in_user['user_id']:
            raise Unauthorized('You do not have sufficient permissions '
                               'to lookup rcis for someone else.')

    user = get_user_record(user_id)

    rci_ids = [ 
        x['rci_id'] 
        for x in datastore.query(
            'select rci_id '
            'from rci_collabs '
            'where user_id = ?', (user_id,))
    ]

    rcis = []

    for rci_id in rci_ids:
        rcis.append(get_rci_by_id(rci_id, full=True))

    return rcis


def get_rcis_for_buildings(buildings, logged_in_user):
    """
    Fetch the rcis for the specified buildings
    """

    # Only users that have the MODERATE_RCIS permission can do this
    if not user_can(Permission.MODERATE_RCIS, logged_in_user):
        raise Unauthorized('You do not have sufficient permissions '
                           'to lookup rcis for a building.')

    rci_ids = [
        x['rci_id']
        for x in datastore.query(
            'select rci_id '
            'from rcis '
            'where building_name in ({})'
            .format(', '.join('?' for i in buildings)),
            buildings)
    ]

    rcis = []

    for rci_id in rci_ids:
        rcis.append(get_rci_by_id(rci_id, full=True))

    return rcis


def search_rcis(search_string, logged_in_user):
    """
    Performs a full-text-search for rcis using the rci_index table
    """

    # Only those with the MODERATE_RCIS permission can do this
    if not user_can(Permission.MODERATE_RCIS, logged_in_user):
        raise Unauthorized('You do not have sufficient permissions '
                           'to perform an rci search')

    
    # If they did not have a search term, return an empty list
    if search_string is None or search_string.strip() == "":
        return []

    # Quote the search string. See https://sqlite.org/fts5.html
    # Not doing this would treat the hyphen character `-` as a column modifier
    search_string = '"{}"'.format(search_string)

    search_results = datastore.query(
        'select * '
        'from rci_index '
        'where rci_index = ?',
        (search_string,))

    rcis = []

    for result in search_results:
        rcis.append(get_rci_by_id(rci_id=result['rci_id'], full=True))

    return rcis 



def create_rci(user_id, building_name, room_name, logged_in_user):
    """
    Creates a new rci record for a room.

    The user who created it is added to the list of collaborators on 
    this rci

    Multiple rcis can exist for the same room
    """
    # You can only create rcis for someone else if you have
    # permissions to MODERATE_RCS or you are creating an 
    # rci for youself.
    if (user_can(Permission.MODERATE_RCIS, logged_in_user)):
        pass
    else:
        if user_id != logged_in_user['user_id']:
            raise Unauthorized('You do not have permissions '
                               'to create an rci for someone else.')

    new_rci_id = str(uuid.uuid4())

    rci_insert_args = {
        'rci_id': new_rci_id, 
        'room_name': room_name,
        'building_name': building_name,
        'created_at': datetime.utcnow(),
        'created_by': logged_in_user['user_id']
    }

    rci_collab_insert_args = {
        'rci_id': new_rci_id, 
        'user_id': user_id
    }
   
    # Create the rci document
    datastore.query(
        'insert into rcis '
        '(rci_id, building_name, room_name, created_at, created_by) '
        'values ' 
        '(:rci_id,:building_name,:room_name,:created_at,:created_by)',
        rci_insert_args)
    
    # Add the user as an a collaborator for the rci
    datastore.query(
        'insert into rci_collabs(rci_id, user_id) '
        'values(:rci_id, :user_id);',
        rci_collab_insert_args)

    # Fetch the newly created rci
    return get_rci_by_id(new_rci_id, full=True)


def lock_rci(rci_id, logged_in_user):
    """
    Freeze an rci, preventing it from being modified
    """
    # We will fail with a clear error here if the rci doesn't exist
    rci = get_rci_record(rci_id)

    # You can only lock an rci if 
    # you have permission to MODERATE_RCIS
    if not user_can(Permission.MODERATE_RCIS, logged_in_user):
        raise Unauthorized('You do not have sufficient permissions '
                           'to lock this rci')

    # Go ahead and lock it up
    datastore.query(
        'update rcis '
        'set is_locked = 1 '
        'where rci_id = ?',
        (rci_id,))


def unlock_rci(rci_id, logged_in_user):
    """
    Un-Freeze an rci, making it editable again 
    """
    # We will fail with a clear error here if the rci doesn't exist
    rci = get_rci_record(rci_id)

    # You can only unlock an rci if 
    # you have permission to MODERATE_RCIS
    if not user_can(Permission.MODERATE_RCIS, logged_in_user):
        raise Unauthorized('You do not have sufficient permissions '
                           'to unlock this rci')

    # Go ahead and unlock it up
    datastore.query(
        'update rcis '
        'set is_locked = 0 '
        'where rci_id = ?',
        (rci_id,))
