import datastore
from authorization import Permission 
from authorization import user_can
from custom_exceptions import BadRequest

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


    attachment_type = data.get('rci_attachment_type', None)

    if attachment_type is None:
        raise BadRequest('Invalid attachment type')

    content = data.get('content', None)

    if content is None:
        raise BadRequest('No content was provided to attachment')
    
    args = {
        'rci_attachment_id': str(uuid.uuid4()),
        'rci_document_id': rci_document_id ,
        'rci_attachment_type': attachment_type,
        'content': str(content),
        'user_id': user_id,
        'created_at': datetime.utcnow().isoformat()
    }
    
    datastore.query(
        'insert into rci_attachments '
        'values (:rci_attachment_id, :rci_document_id, :rci_attachment_type, :content, :user_id, :created_at) ',
        args)

    return args

def delete_rci_attachment(rci_document_id, rci_attachment_id, user_id):
    """
    Deletes an rci attachment
    """

    inputs, _ = get_authorization_inputs(
        Permission.WRITE,
        user_id,
        ProtectedResource.RCI_DOCUMENT,
        rci_document_id)

    authorize(**inputs)

    datastore.query(
        'delete from rci_attachments '
        'where rci_attachment_id = ? ',
        (rci_attachment_id,))
