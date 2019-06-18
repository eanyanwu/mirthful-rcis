from mirthful_rcis.dal import datastore
from mirthful_rcis.lib.exceptions import Unauthorized, BadRequest

from enum import IntEnum

def user_can(permissions, user):
    """
    Check a user's permissions against the permissions she seeks

    Throw if the user object does not have a permission attribute
    """
    user_permissions = datastore.query(
        'select * '
        'from roles '
        'where role = ? ',
        (user['role'],), one=True)

    if user_permissions is None:
        raise ValueError('user does not have permissions attribute') 

    return user_permissions['permissions'] & permissions == permissions


class Permission(IntEnum):
    NONE                = 0b00000000
    MODERATE_DAMAGES    = 0b00000001
    MODERATE_RCIS       = 0b00000010
    MODERATE_SYSTEM     = 0b00000100
