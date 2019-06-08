import mirthful_rcis.datastore as datastore
from mirthful_rcis.authorization import Permission 
from mirthful_rcis.authorization import user_can
from mirthful_rcis.custom_exceptions import BadRequest, Unauthorized

import uuid
from datetime import datetime, timedelta

def get_user_record(user_id):
    return datastore.query(
        'select * from users '
        'where user_id = ? '
        'limit 1', (user_id,),
        one=True
    )

def get_rci_record(rci_id):
    """
    Useful method for quickly figuring out if an rci exists

    Returns the rci db record if it does.
    Returns None if it does not
    """
    return datastore.query(
        'select * from rcis '
        'where rci_id = ? '
        'limit 1',
        (rci_id,),
        one=True)


def get_damage_record(damage_id):
    """
    Useful method for quickly figuring out if a damage record

    Returns the damage record if it does
    Returns None if it does not
    """
    return datastore.query(
        'select * '
        'from damages '
        'where damage_id = ?', 
        (damage_id,),
        one=True)


def get_rci_collaborators(rci_id):
    """
    Useful method for listing the collaborators for an rci
    """
    return datastore.query(
        'select * ' 
        'from rci_collabs '
        'where rci_id = ?',
        (rci_id,))


def get_users():
    """
    Fetches all users
    """
    return datastore.query(
        'select * '
        'from users '
    )


def get_full_rci_document(rci_id):
    """
    Creates a complete rci document that includes
    the rci collaborators and damages recorded
    """
    rci = get_rci_record(rci_id)

    if rci is None:
        raise BadRequest('no such rci {}'.format(rci_id))

    rci_collaborators = datastore.query(
        'select u.* '
        'from rci_collabs as rc '
        'inner join users as u '
        'using(user_id) '
        'where rc.rci_id = ?',
        (rci_id,))

    damages = get_damages_for_rci(rci_id) 

    full_rci_doc = {
        'rci_id': rci_id,
        'collaborators': rci_collaborators,
        'damages': damages,
        'room_name': rci['room_name'],
        'building_name': rci['building_name'],
        'created_at': rci['created_at'],
        'is_locked': True if rci['is_locked'] == 1 else False
    }

    return full_rci_doc 


def get_damages_for_rci(rci_id):
    return datastore.query(
        'select * '
        'from damages '
        'where rci_id =? ',
        (rci_id,))


def get_building_manifest():
    """
    Return a summary of the building layout.
    """
    result = datastore.query('select * from rooms');
    
    manifest = {}

    for room in result:
        building_name = room['building_name']
        manifest.setdefault(building_name, []).append(room)

    return manifest

def get_room_areas():
    """
    Return the list of default room areas
    """
    return datastore.query(
        'select * '
        'from room_areas'
    )


def get_rci(rci_id): 
    """
    Fetch an rci document by id
    """
    rci = get_full_rci_document(rci_id)

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    return rci 

def get_user_rcis(user_id):
    """
    Fetch the rcis for the specified user
    """
    rci_ids = [ 
        x['rci_id'] 
        for x in datastore.query(
            'select rci_id '
            'from rci_collabs '
            'where user_id = ?', (user_id,))
    ]

    rcis = []

    for rci_id in rci_ids:
        rcis.append(get_full_rci_document(rci_id))

    return rcis

def get_building_rcis(buildings):
    """
    Fetch the rcis for the specified buildings
    """
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
        rcis.append(get_full_rci_document(rci_id))

    return rcis


def create_rci(user_id, building_name, room_name):
    """
    Creates a new rci record for a room.

    The user who created it is added to the list of collaborators on 
    this rci

    Multiple rcis can exist for the same room
    """
    new_rci_id = str(uuid.uuid4())

    rci_insert_args = {
        'rci_id': new_rci_id, 
        'room_name': room_name,
        'building_name': building_name,
        'created_at': datetime.utcnow()
    }

    rci_collab_insert_args = {
        'rci_id': new_rci_id, 
        'user_id': user_id
    }
   
    # Create the rci document
    datastore.query(
        'insert into rcis(rci_id, building_name, room_name, created_at) '
        'values(:rci_id,:building_name,:room_name,:created_at)',
        rci_insert_args)
    
    # Add the user as an a collaborator for the rci
    datastore.query(
        'insert into rci_collabs(rci_id, user_id) '
        'values(:rci_id, :user_id);',
        rci_collab_insert_args)

    # Fetch the newly created rci
    return get_full_rci_document(new_rci_id)


def lock_rci(rci_id, user):
    """
    Freeze an rci, preventing it from being modified
    """
    # First check if the rci exists
    rci = get_rci_record(rci_id)

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # You can only lock an rci if 
    # you have permission to MODERATE_RCIS
    if not user_can(Permission.MODERATE_RCIS, user):
        raise Unauthorized('you do not have sufficient permissions '
                           'to lock this rci')

    # Go ahead and lock it up
    datastore.query(
        'update rcis '
        'set is_locked = 1 '
        'where rci_id = ?',
        (rci_id,))


def unlock_rci(rci_id, user):
    """
    Un-Freeze an rci, making it editable again 
    """

    # First check if the rci exists
    rci = get_rci_record(rci_id)

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # You can only unlock an rci if 
    # you have permission to MODERATE_RCIS
    if not user_can(Permission.MODERATE_RCIS, user):
        raise Unauthorized('you do not have sufficient permissions '
                           'to unlock this rci')

    # Go ahead and unlock it up
    datastore.query(
        'update rcis '
        'set is_locked = 0 '
        'where rci_id = ?',
        (rci_id,))


def delete_rci(rci_id, user):
    """
    Delete an rci document
    """

    # First check that the rci exists
    rci = get_rci_record(rci_id)

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # You can only delete an rci if you areone of the following
    # (a) a collaborator on that rci OR
    # (b) a user with permission to MODERATE_RCIS
    if (user_can(Permission.MODERATE_RCIS, user)):
        pass
    else:
        rci_collaborators = [
            x['user_id'] 
            for x in get_rci_collaborators(rci_id)
        ]

        if user['user_id'] not in rci_collaborators:
            raise Unauthorized('You cannot delete this rci.' 
                               'Please ask to be added to the list of '
                               'collaborators')

    datastore.query(
        'delete from rcis '
        'where rci_id = ?',
        (rci_id,))


def create_damage(user, rci_id, item, text, image_url):
    """
    Record a damage on the rci 
    """

    # Check that the rci exists
    rci = get_rci_record(rci_id)

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # Cannot record a damage if the rci is locked
    if rci['is_locked']:
        raise BadRequest('rci {} is locked'.format(rci_id))

    # Check that the user is one of the following
    # (a) a collaborator on the rci OR
    # (b) has Permission.MODERATE_DAMAGES
    if (user_can(Permission.MODERATE_DAMAGES, user)):
        pass
    else:
        rci_collaborators = [
            x['user_id'] 
            for x in get_rci_collaborators(rci_id) 
        ]

        if user['user_id'] not in rci_collaborators:
            raise Unauthorized('You cannot record damage on this rci.' 
                               'Please ask to be added to the list of '
                               'collaborators')


    damage_insert_args = {
        'damage_id': str(uuid.uuid4()),
        'rci_id': rci_id,
        'item': item,
        'text': text,
        'image_url': image_url,
        'user_id': user['user_id'],
        'created_at': datetime.utcnow()
    }
    
    datastore.query(
        'insert into '
        'damages(damage_id, rci_id, item, text, image_url, user_id, created_at) '
        'values(:damage_id,:rci_id,:item,:text,:image_url,:user_id,:created_at) ',
        damage_insert_args)

    return get_damage_record(damage_insert_args['damage_id'])

def delete_damage(rci_id, damage_id, user):
    """
    Delete a damage record
    """

    # Check that the rci exists
    rci = get_rci_record(rci_id)

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # Cannot delete a damage if the rci is locked
    if rci['is_locked']:
        raise BadRequest('rci {} is locked'.format(rci_id))

    # Check that the user is one of the following
    # (a) a collaborator on the rci OR
    # (b) has Permission.MODERATE_DAMAGES
    if (user_can(Permission.MODERATE_DAMAGES, user)):
        pass
    else:
        rci_collaborators = [
            x['user_id'] 
            for x in get_rci_collaborators(rci_id) 
        ]

        if user['user_id'] not in rci_collaborators:
            raise Unauthorized('You cannot delete damages from this rci.' 
                               'Please ask to be added to the list of '
                               'collaborators')

    datastore.query(
        'delete from damages '
        'where damage_id = ?',
        (damage_id,))

