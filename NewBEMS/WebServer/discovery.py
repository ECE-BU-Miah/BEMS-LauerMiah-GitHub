from flask import Blueprint, render_template, request
from . import database
from . import pubsub
import global_settings
import json

bp = Blueprint('discovery',__name__)

# @bp.route('/discovery')
# def discoverDevices():
#     if request.method == "GET":
#         deviceNames = loadSupportedDevices()
#         pubsub.publish('discovery', 'autoSearchForDevices')
#         return render_template('discovery.html',deviceNames=deviceNames)
#
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

@bp.route('/discovery/agents', methods=['POST'])
def handleAgentRequest():
    '''
    Handle any post request send by an agent
    through this URL.
    '''
    if request.method == "POST":
        activeDevices = loadActiveDevices()
    return render_template('discovery.html', deviceNames=activeDevices)

def loadSupportedDevices():
    db = database.DBConnection(global_settings.WEBSERVER_DIR + 'meta.db')
    db.cursor.execute('SELECT manufacturer, name FROM SupportedDevices')
    devices = db.cursor.fetchall()
    displayData = list()
    for device in devices:
        s = ' '.join(device)
        displayData.append(s)
    db.close()
    return displayData
