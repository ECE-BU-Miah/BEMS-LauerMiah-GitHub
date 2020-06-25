from flask import Blueprint, render_template, request
from . import database
from . import pubsub
import global_settings
import json

bp = Blueprint('discovery',__name__)

@bp.route('/discovery')
def discoverDevices():
    if request.method == "GET":
        deviceNames = loadDeviceNames()
        return render_template('discovery.html',deviceNames=deviceNames)

@bp.route('/discovery/ajax', methods=['POST'])
def requestIDs():
    if request.method == "POST":
        db = database.DBConnection(global_settings.WEBSERVER_DIR + 'meta.db')
        # Decode JSON data and convert to python list
        data = json.dumps(request.data.decode('utf-8'))
        # Remove ids from the list that do not correspond to supported devices
        for id in data:
            db.cursor.execute('SELECT * FROM SupportedDevices WHERE id = ?', (id,))
            result = db.cursor.fetchall()
            if result is None:
                data.remove(id)
        dataJson = json.loads(str(data))
        pubsub.publish('discovery', 'searchForDevices', dataJson)
    return json.dumps(request.data.decode('utf-8'))

def loadDeviceNames():
    db = database.DBConnection(global_settings.WEBSERVER_DIR + 'meta.db')
    db.cursor.execute('SELECT manufacturer, name FROM SupportedDevices')
    devices = db.cursor.fetchall()
    displayData = list()
    for device in devices:
        s = ' '
        s = s.join(device)
        displayData.append(s)
    db.close()
    return displayData
