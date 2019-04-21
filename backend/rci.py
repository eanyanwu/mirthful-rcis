import rci_datastore

import uuid
# Business Logic for Rci-related things

DEFAULT_RCI_ACL = 'rw:rw:__'


def find_rci(rci_id):
    if not rci_id:
        raise ValueError('user_id is None')

    rci = rci_datastore.get_rci(rci_id)

    if not rci:
        # TODO: Return custom exception
        raise ValueError()

    return rci


def create_new_rci(user_id, room_id):
    if not user_id:
        raise ValueError('user_id is None')

    if not room_id:
        raise ValueError('room_id is None')

    rci_id = str(uuid.uuid4())
    user_id = str(user_id)
    acl = DEFAULT_RCI_ACL

    # Create it
    rci_datastore.insert_rci_document(
        rci_id=rci_id,
        user_id=user_id,
        room_id=room_id,
        acl_string=acl)

    # Fetch it
    new_rci = rci_datastore.get_rci(rci_id)

    return new_rci