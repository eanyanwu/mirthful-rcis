from mirthful_rcis.db import get_db

import sqlite3
import os.path

# Thread-safe globals. Thanks flask
from flask import g

class DbTransaction:
    """
    Simplifies creating a database transaction 
    
    This is done by using a python context manager to place all the boiler
    plate code in one location.

    A check is performed to see if an existing connection exists.
    If it does not, it is created.

    When the context manager is used, it returns a cursor object.

    When the context manager is existed, it executes the commit() method
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

