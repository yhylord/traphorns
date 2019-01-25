import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    Connect to the configured database. The connection is unique for each
    request and will be reused if this is called again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(error=None):
    """
    Close the connection to the database if connected.
    """
    db = g.pop('db', None)

    if db:
        db.close()


def init_db():
    """
    Drop existing tables and create new ones.
    """
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode())


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Add the CLI command for initializing the database.
    """
    init_db()

    click.echo('Database initialized.')


def init_app(app):
    """
    Register database functions with the Flask app.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
