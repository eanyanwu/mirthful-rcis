from mirthful_rcis.dal import datastore
from mirthful_rcis.lib import common
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

def create_damage(logged_in_user, rci_id, item, text, image_url):
    """
    Record a damage on the rci 
    """

    # Check that the rci exists
    try:
        rci = common.get_rci_record(rci_id)
    except RecordNotFound:
        raise BadRequest('Rci {} does not exist'.format(rci_id))

    # Cannot record a damage if the rci is locked
    if rci['is_locked']:
        raise BadRequest('rci {} is locked'.format(rci_id))

    # Check that the user is one of the following
    # (a) a collaborator on the rci OR
    # (b) has Permission.MODERATE_DAMAGES
    if (user_can(Permission.MODERATE_DAMAGES, logged_in_user)):
        pass
    else:
        rci_collaborators = [
            x['user_id'] 
            for x in common.get_rci_collaborators(rci_id) 
        ]

        if logged_in_user['user_id'] not in rci_collaborators:
            raise Unauthorized('You cannot record damage on this rci.' 
                               'Please ask to be added to the list of '
                               'collaborators')


    damage_insert_args = {
        'damage_id': str(uuid.uuid4()),
        'rci_id': rci_id,
        'item': item,
        'text': text,
        'image_url': image_url,
        'created_by': logged_in_user['user_id'],
        'created_at': datetime.utcnow()
    }
    
    datastore.query(
        'insert into '
        'damages(damage_id, rci_id, item, text, image_url, created_by, created_at) '
        'values(:damage_id,:rci_id,:item,:text,:image_url,:created_by,:created_at) ',
        damage_insert_args)

    return common.get_damage_record(damage_insert_args['damage_id'])

def delete_damage(damage_id, logged_in_user):
    """
    Delete a damage record
    """

    # Check that the damage exists 
    try:
        damage = common.get_damage_record(damage_id)
    except RecordNotFound:
        raise BadRequest('Damage {} does not exist'.format(damage_id))

    # Get the rci
    try:
        rci = common.get_rci_record(damage['rci_id'])
    except RecordNotFound:
        raise BadRequest('Rci {} does not exist'.format(damage['rci_id']))

    rci_id = rci['rci_id']

    # Cannot delete a damage if the rci is locked
    if rci['is_locked']:
        raise BadRequest('rci {} is locked'.format(rci_id))

    # Check that the user is one of the following
    # (a) a collaborator on the rci OR
    # (b) has Permission.MODERATE_DAMAGES
    if (user_can(Permission.MODERATE_DAMAGES, logged_in_user)):
        pass
    else:
        rci_collaborators = [
            x['user_id'] 
            for x in common.get_rci_collaborators(rci_id) 
        ]

        if logged_in_user['user_id'] not in rci_collaborators:
            raise Unauthorized('You cannot delete damages from this rci.' 
                               'Please ask to be added to the list of '
                               'collaborators')

    datastore.query(
        'delete from damages '
        'where damage_id = ?',
        (damage_id,))

    return damage

