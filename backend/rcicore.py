import datastore
from authorization import Permission 
from authorization import user_can
from custom_exceptions import BadRequest, Unauthorized

import uuid
from datetime import datetime, timedelta

def find_rci(rci_id):
    return datastore.query(
        'select * from rcis '
        'where rci_id = ? '
        'limit 1',
        (rci_id,),
        one=True)

def find_room(room_id):
    return datastore.query(
        'select * from rooms '
        'where room_id = ? '
        'limit 1',
        (room_id,),
        one=True)

def find_user(user_id):
    return datastore.query(
        'select * from users '
        'where user_id = ? '
        'limit 1;',
        (user_id,),
        one=True)

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



def get_rci_collaborators(rci_id):
    return datastore.query(
        'select * '
        'from rci_collabs as rc '
        'left join rcis as r '
        'on r.rci_id = rc.rci_id '
        'where rc.rci_id = ?',
        (rci_id,))


def get_rci(rci_id): 
    """
    Fetch an rci document
    """
    rci = find_rci(rci_id)

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # TODO: Craft the full rci document with damages coments and whatnot
    return rci 

def get_user_rcis(user_id):
    """
    Get all the rcis for which the user is a collaborator
    """
    user = find_user(user_id)

    if user is None:
        raise BadRequest('user {} does not exist'.format(user_id))

    rcis = datastore.query(
        'select r.* '
        'from rci_collabs as rc '
        'inner join rcis as r '
        'on rc.rci_id = r.rci_id '
        'where rc.user_id = ? ',
        (user_id,))

    return rcis

def post_rci(user_id, room_id):
    """
    Creates a new rci record for a room.

    The user who created it is added to the list of collaborators on 
    this rci

    Multiple rcis can exist for the same room
    """
    new_rci_id = str(uuid.uuid4())

    # First check that the room exists
    room = find_room(room_id)

    if room is None:
        raise BadRequest('room {} does not exist'.format(room_id))

    rci_insert_args = {
        'rci_id': new_rci_id, 
        'room_id': room_id,
        'created_at': datetime.utcnow().isoformat(),
    }

    rci_collab_insert_args = {
        'rci_collab_id': str(uuid.uuid4()),
        'rci_id': new_rci_id, 
        'user_id': user_id
    }
   
    # Create the rci document
    datastore.query(
        'insert into rcis(rci_id, room_id, created_at) '
        'values(:rci_id, :room_id, :created_at)',
        rci_insert_args)
    
    # Add the user as an a collaborator for the rci
    datastore.query(
        'insert into rci_collabs(rci_collab_id, rci_id, user_id) '
        'values(:rci_collab_id, :rci_id, :user_id);',
        rci_collab_insert_args)

    # Fetch the newly created rci
    new_rci = datastore.query(
        'select * '
        'from rcis '
        'where rci_id=?',
        (new_rci_id,),
        one=True)

    return new_rci

def lock_rci(rci_id, user):
    """
    Freeze an rci, preventing it from being modified
    """

    # First check if the rci exists
    rci = find_rci(rci_id)

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

    rci = datastore.query(
        'select * from rcis where rci_id = ?',
        (rci_id,),
        one=True
    )

    return rci


def unlock_rci(rci_id, user):
    """
    Un-Freeze an rci, making it editable again 
    """

    # First check if the rci exists
    rci = find_rci(rci_id)

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

    rci = datastore.query(
        'select * from rcis where rci_id = ?',
        (rci_id,),
        one=True
    )

    return rci


def delete_rci(rci_id, user):
    """
    Delete an rci document
    """

    # First check that the rci exists
    rci = find_rci(rci_id)

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # You can only delete an rci if one of the following
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


def post_damage(user, rci_id, text, image_url):
    """
    Record a damage on the rci 
    """

    # Check that the rci exists
    rci = find_rci(rci_id)

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
        'text': text,
        'image_url': image_url,
        'user_id': user['user_id'],
        'created_at': datetime.utcnow().isoformat()
    }
    
    datastore.query(
        'insert into '
        'damages(damage_id, rci_id, text, image_url, user_id, created_at) '
        'values(:damage_id,:rci_id,:text,:image_url,:user_id,:created_at) ',
        damage_insert_args)

    new_damage = datastore.query(
        'select * '
        'from damages '
        'where damage_id = ?', 
        (damage_insert_args['damage_id'],),
        one=True)

    return new_damage 

def delete_damage(rci_id, damage_id, user):
    """
    Delete a damage record
    """

    # Check that the rci exists
    rci = find_rci(rci_id)

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

