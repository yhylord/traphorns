from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .db import get_db

bp = Blueprint('trap', __name__)

@bp.route('/')
def index():
    links = get_links()
    dead_links = get_dead_links()
    return render_template('trap/index.html',
                           links=links, dead_links=dead_links)


def get_links():
    db = get_db()
    links = db.execute('SELECT * FROM links').fetchall()
    return links


def get_dead_links():
    db = get_db()
    dead_links = db.execute('SELECT * FROM links WHERE dead = 1').fetchall()
    return dead_links
