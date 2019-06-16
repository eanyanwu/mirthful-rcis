from mirthful_rcis.lib import libuser

def test_get_users(app, user_factory):
    """
    Simple test that the get_users call reacts to database changes
    """

    with app.app_context():
        users = libuser.get_users()

        assert len(users) == 0

        user_factory()

        users = libuser.get_users()

        assert len(users) == 1


