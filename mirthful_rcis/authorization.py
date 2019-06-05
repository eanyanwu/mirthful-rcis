import mirthful_rcis.datastore as datastore
from mirthful_rcis.custom_exceptions import Unauthorized, BadRequest

from enum import IntEnum

def user_can(permissions, user):
    """
    Check a user's permissions against the permissions she seeks

    Throw if the user object does not have a permission attribute
    """
    user_permissions = user.get('permissions', None)

    if user_permissions is None:
        raise ValueError('user does not have permissions attribute') 

    return user_permissions & permissions == permissions


class Permission(IntEnum):
    MODERATE_DAMAGES    = 0b00000001
    MODERATE_RCIS       = 0b00000010
