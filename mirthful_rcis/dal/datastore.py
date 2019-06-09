import sqlite3
import os.path

from flask import g
from flask import current_app

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

def get_db():
    """
    Get a connection to the configured database
    A new one is created if it does not exist
    """
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'],
                               detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = dict_factory

    return g.db

class DbTransaction:
    """
    Simplifies creating a database transaction 

    A transaction in this sense is any sequence of commands that are executed
    before calling `commit`
    
    This is done by using a python context manager to place all the boiler
    plate code in one location.

    When the context manager is used, it returns a cursor object.

    When the context manager is exited, it executes the commit() method
    """
    connection = None

    def __init__(self):
        pass

    def __enter__(self):
        self.connection = get_db()
        cursor = self.connection.cursor()

        # Sqlite3 doesn't enable foreign keys by default.
        # See 2nd secion of the following link:
        # https://sqlite.org/foreignkeys.html
        cursor.execute('pragma foreign_keys = ON')

        return cursor 

    def __exit__(self, *args):
        self.connection.commit()

def query(sql, args=None, one=False):
    """
    Execute a single SQL command returns the results.
    """
    with DbTransaction() as conn:
        if args is None:
            args = ()

        conn.execute(sql, args)

        results = conn.fetchall()

        if one:
            return next(iter(results), None)
        else:
            return results

def executemany(*args, **kwargs):
    """
    Simple wrapper around the sqlite executemany method
    """
    with DbTransaction() as conn:
        conn.executemany(*args, **kwargs)


def execute_script(sql_script):
    """
    Execute multiple sql statments at once
    """
    with DbTransaction() as conn:
        return conn.executescript(sql_script)


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

