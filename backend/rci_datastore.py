import uuid
import sqlite3
from datetime import datetime
from datetime import timedelta

# Connection string that will be used by the methods in this module
connection_string = "rci.db"

# Fetch a user record by username 
def get_user(username):
    connection = sqlite3.connect(connection_string)

    connection.row_factory = dict_factory 

    with connection:
        cursor = connection.cursor()

        cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
        LIMIT 1;""", (username,))

        return cursor.fetchone()
    

# Inserts a session record into the data store
def insert_session(session):
    connection = sqlite3.connect(connection_string)

    with connection:
        cursor = connection.cursor()

        cursor.execute("""INSERT INTO sessions VALUES (?,?,?,?)""",
                       (session['session_id'],
                       session['user_id'],
                       session['created_at'],
                       session['expires_at']))

# Sqlite's Row factory works well, however, I REALLY
# want to return my records as plain dictionaries.
# Makes it easier to handle in any modules that use 
# this module.
# See https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.row_factory
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

