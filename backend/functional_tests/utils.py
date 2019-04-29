def login_as(user, client):
    """
    Convenience method for logging in as a certain user
    """
    response = client.post(
        '/login',
        data={
            'username': user['username'],
            'password': user['password']
        })

    return response

def setup_user(client, user_factory):
    """
    Convenience method for returning a user from the user factory
    """
    with client.application.app_context():
        return user_factory()

def setup_room(client, room_factory):
    """
    Convenience mthod fo returning a room from the room factory
    """
    with client.application.app_context():
        return room_factory()

