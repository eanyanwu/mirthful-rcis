from mirthful_rcis.dal import datastore

def get_users():
    """
    Fetches all users
    """
    return datastore.query(
        'select * '
        'from users '
    )

