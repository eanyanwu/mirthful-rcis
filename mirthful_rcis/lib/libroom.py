from mirthful_rcis.dal import datastore

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
