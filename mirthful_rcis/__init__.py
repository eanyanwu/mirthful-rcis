import os
from flask import Flask


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

    from mirthful_rcis import db
    db.initialize_application(app)

    from mirthful_rcis import login_controller
    from mirthful_rcis import rcis_controller

    app.register_blueprint(login_controller.bp)
    app.register_blueprint(rcis_controller.bp)

    return app
