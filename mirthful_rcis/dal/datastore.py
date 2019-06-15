from mirthful_rcis import get_db

import sqlite3
import os.path


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
