import click
import sqlite3
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    Get a connection to the configured database
    A new one is created if it does not exist
    """
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = dict_factory

    return g.db


def close_db(e=None):
    """
    Close the connection to the database if it exists
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def initialize_db():
    """
    Setup the database using the schema file. 
    """
    db = get_db()

    with current_app.open_resource('sql/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def populate_db_with_test_data():
    db = get_db()

    with current_app.open_resource('sql/bootstrap_db.sql') as f:
        db.executescript(f.read().decode('utf8'))


def initialize_application(app):
    """
    Initialize the application by registering the `close_db` function to run on
    request teardown.

    Additionally, register cli commands
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(initialize_db_command)
    app.cli.add_command(initialize_db_test_data_command)


@click.command('init-db')
@with_appcontext
def initialize_db_command():
    """
    Clear the existing data and create new tables
    """
    initialize_db()
    click.echo('Initialized database.')

@click.command('init-db-data')
@with_appcontext
def initialize_db_test_data_command():
    initialize_db()
    populate_db_with_test_data()
    click.echo('Initialized database with test data.')





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
