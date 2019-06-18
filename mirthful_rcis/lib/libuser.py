from mirthful_rcis.dal import datastore
from mirthful_rcis.lib.authorization import Permission

def get_users():
    """
    Fetches all users
    """
    return datastore.query(
        'select * '
        'from users '
    )


def get_user_permissions(user_id):
    """
    Get the user's permissions
    """

    result = datastore.query(
        'select r.permissions ' 
        'from users as u '
        'inner join roles as r '
        'using(role) '
        'where u.user_id = ?',
        (user_id,),
        one=True)

    if result is None:
        return result
    else:
        return result['permissions']


def get_user_settings(user_id):
    """
    Fetch the settings for the user
    """

    result = datastore.query(
        'select * '
        'from user_settings '
        'where user_id = ?',
        (user_id,),
        one=True)

    if result is not None:
        return result
    else:
        # Make like we actually found the result. But instead of having values
        # for the keys, we just put None
        column_names = [
            x['name']
            for x in datastore.query(
                'select * '
                'from pragma_table_info(\'user_settings\') ')
        ]

        column_values = [ None for _ in column_names] 

        return dict(zip(column_names, column_values))
