from flask import Blueprint, render_template, request, Response
from . import database
from . import pubsub
import global_settings
import json
import time
import sqlite3

bp = Blueprint('applications', __name__)

@bp.route('/applications')
def renderSettings():
    return render_template('applications.html')
