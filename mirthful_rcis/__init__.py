import click
import os
from flask import (
    g,
    Flask,
    current_app
)
from flask.cli import with_appcontext

def close_db(e=None):
    """
    Close the connection to the database if it exists
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def initialize_database():
    """
    Setup database schema and test data
    """
    from mirthful_rcis.dal.datastore import get_db

    db = get_db()

    with current_app.open_resource('sql/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('sql/bootstrap_db.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Clear the existing data and create new tables
    """
    initialize_database()
    click.echo('Initialized database.')
    

def initialize_application(app):
    """
    Initialize the application by registering the `close_db` function to run on
    request teardown.

    Additionally, register cli commands
    """
    # Application teardown
    app.teardown_appcontext(close_db)

    # Cli commands
    app.cli.add_command(init_db_command)


def create_app(test_config=None):
    app = Flask("mirthful_rcis", instance_relative_config=True)

    # Initial configuration 
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'rci.sqlite')
    )

    if test_config is None:
        # load actual configuration
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test configuration
        app.config.from_mapping(test_config)

    # Ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    initialize_application(app)

    from mirthful_rcis.controllers import auth 
    from mirthful_rcis.controllers import dashboard
    from mirthful_rcis.controllers import rci
    from mirthful_rcis.controllers import damage

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(rci.bp)
    app.register_blueprint(damage.bp)

    return app
