import datastore

from functools import wraps
from enum import Enum, auto

class RciFilterType(Enum):
    ROOM_NAME = auto() 
    BUILDING_NAME = auto() 
    USER_ID = auto() 

# Mapping form filter type to method
RCI_FILTERS = {}

def rci_filter(filter_type):
    def decorator_register_filter(func):
        RCI_FILTERS[filter_type] = func
        return func

    return decorator_register_filter


@rci_filter(RciFilterType.USER_ID)
def filter_rcis_by_user_id(filter_params):
    user_ids = filter_params['filter_value']

    # Find all rcis this users have collaborated on.
    results = datastore.query(
        'select rci_id from rci_collabs '
        'where user_id in ({})'.format(', '.join('?' for _ in user_ids)),
        user_ids)

    return [ x['rci_id'] for x in results ]




@rci_filter(RciFilterType.ROOM_NAME)
def filter_rcis_by_room_name(filter_params):
    print('Filtering by room name')

@rci_filter(RciFilterType.BUILDING_NAME)
def filter_rcis_by_building_Name(filter_params):
    print('Filtering by building name')
