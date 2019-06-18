from mirthful_rcis.lib import libuser
from mirthful_rcis.lib.authorization import Permission
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


def test_get_user_settings_BUT_no_setting(app, user):
    """
    Assert that the call to get user settings works as expected
    """
    with app.app_context():
        settings = libuser.get_user_settings(user_id=user['user_id'])

        for key in settings.keys():
            assert settings[key] is None


def test_get_user_permissions(app, user_factory):
    user1 = user_factory()
    user2 = user_factory(permissions=Permission.MODERATE_DAMAGES)
    user3 = user_factory(permissions=Permission.MODERATE_RCIS)
    user4 = user_factory(permissions=Permission.MODERATE_RCIS|
                         Permission.MODERATE_DAMAGES)

    with app.app_context():
        assert libuser.get_user_permissions(user1['user_id']) == Permission.NONE
        assert libuser.get_user_permissions(user2['user_id']) == Permission.MODERATE_DAMAGES
        assert libuser.get_user_permissions(user3['user_id']) == Permission.MODERATE_RCIS
        
        user4_permissions = libuser.get_user_permissions(user4['user_id'])
        assert user4_permissions == Permission.MODERATE_RCIS | Permission.MODERATE_DAMAGES







