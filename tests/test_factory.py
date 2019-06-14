from mirthful_rcis import (
    create_app,
    get_db
)

import pytest
import sqlite3 

# Test that the app factory sets the `testing` property correctly
def test_app_factory():
    assert create_app().testing == False
    assert create_app({'TESTING': True}).testing == True


# Test that we get the same connection when calling `get_db` multiple times
# Also test that after the application context has been popped, the connection
# is closed.
def test_open_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('select 1')

    assert 'closed database' in str(e)
