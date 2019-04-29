import datastore
from authorization import Permission, ProtectedResource
from authorization import authorize, get_authorization_inputs
from custom_exceptions import BadRequest

import uuid
from datetime import datetime, timedelta

def get_rci(rci_document_id, user_id): 
    """
    Fetch a full rci document for the user
    """
    inputs, rci_document = get_authorization_inputs(
        Permission.READ,
        user_id,
        ProtectedResource.RCI_DOCUMENT,
        rci_document_id)

    authorize(**inputs)

    # TODO: Craft the full rci document with damages coments and whatnot
    return rci_document

def post_rci(user_id, room_id):
    """
    Creates a new rci record and adds the user to the list of owners
    """

    args = {
        'rci_document_id': str(uuid.uuid4()),
        'room_id': room_id,
        'created_at': datetime.utcnow().isoformat(),
        'access_control': 'o:rw;g:rw;w:__',
        'acl_owner_id': user_id
    }
   
    # Create the rci document
    datastore.query(
        'insert into rci_documents '
        'values '
        '(:rci_document_id, '
        ':room_id, '
        ':created_at, '
        ':access_control);',
        args)
    
    # Add the user as an owner for the document
    datastore.query(
        'insert into rci_document_acl_owners '
        'values (NULL, :rci_document_id, :acl_owner_id);',
        args)

    return args

def post_rci_attachment(rci_document_id, user_id, data):
    """
    Creates a new rci attachment
    """
    inputs, _  = get_authorization_inputs(
        Permission.WRITE,
        user_id,
        ProtectedResource.RCI_DOCUMENT,
        rci_document_id)

    authorize(**inputs)

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
