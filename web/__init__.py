import os

from flask import Flask


def create_app(test_config=None):
    """
    Create the Flask app instance.

    Initialize the database and the views.

    Parameters
    ----------
    test_config
        The config used to create a Flask instance for testing.

    """
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='secret',
        DATABASE=os.path.join(app.instance_path, 'traps.db')
    )

    if test_config is None:
        # load the instance config if it exists
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # make sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import trap
    app.register_blueprint(trap.bp)

    return app
