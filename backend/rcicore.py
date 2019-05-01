import datastore
from authorization import Permission 
from authorization import user_can
from custom_exceptions import BadRequest, Unauthorized

import uuid
from datetime import datetime, timedelta

def get_rci(rci_id): 
    """
    Fetch a full rci document for the user
    """

    rci = datastore.query(
        'select * '
        'from rcis '
        'where rci_id = ?',
        (rci_id,),
        one=True)

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # TODO: Craft the full rci document with damages coments and whatnot
    return rci 

def post_rci(user_id, room_id):
    """
    Creates a new rci record for a room.

    The user who created it is added to the list of collaborators on 
    this rci

    Multiple rcis can exist for the same room
    """
    new_rci_id = str(uuid.uuid4())

    # First check that the room exists
    room = datastore.query(
        'select * from rooms '
        'where room_id = ? '
        'limit 1', (room_id,), one=True)

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

def post_damage(user, rci_id, text, image_url):
    """
    Record a damage on the rci 
    """

    # Check that the rci exists
    rci = datastore.query(
        'select * from rcis where rci_id=?',(rci_id,),
        one=True
    )

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # Check that the user is one of the following
    # (a) a collaborator on the rci OR
    # (b) has Permission.MODERATE_DAMAGES
    if (user_can(Permission.MODERATE_DAMAGES, user)):
        pass
    else:
        rci_collaborators = datastore.query(
            'select * '
            'from rci_collabs as rc '
            'left join rcis as r '
            'on r.rci_id = rc.rci_id '
            'where rc.rci_id = ?', (rci_id,))

        rci_collaborators = [
            x['user_id'] 
            for x in rci_collaborators
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
    rci = datastore.query(
        'select * from rcis where rci_id=?',(rci_id,),
        one=True
    )

    if rci is None:
        raise BadRequest('rci {} does not exist'.format(rci_id))

    # Check that the user is one of the following
    # (a) a collaborator on the rci OR
    # (b) has Permission.MODERATE_DAMAGES
    if (user_can(Permission.MODERATE_DAMAGES, user)):
        pass
    else:
        rci_collaborators = datastore.query(
            'select * '
            'from rci_collabs as rc '
            'left join rcis as r '
            'on r.rci_id = rc.rci_id '
            'where rc.rci_id = ?', (rci_id,))

        rci_collaborators = [
            x['user_id'] 
            for x in rci_collaborators
        ]

        if user['user_id'] not in rci_collaborators:
            raise Unauthorized('You cannot delete damages from this rci.' 
                               'Please ask to be added to the list of '
                               'collaborators')

    datastore.query(
        'delete from damages '
        'where damage_id = ?',
        (damage_id,))

