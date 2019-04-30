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

