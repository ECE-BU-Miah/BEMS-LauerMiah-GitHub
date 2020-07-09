from flask import Blueprint, render_template, request, Response
from . import database
from . import pubsub
import global_settings
import json
import time
import sqlite3

bp = Blueprint('active_devices', __name__)

done_discovering = False

@bp.route('/active_devices')
def renderActiveDevices():
    global done_discovering
    activeDevices = list()
    if request.method == "GET":
        pubsub.publish('discovery', 'searchForDevices')
        print("Waiting for discovery agent...")
        while not done_discovering:
            time.sleep(0.1)
        activeDevices = loadActiveDevices()
        print("activeDevices: " + str(activeDevices))
    return render_template('active_devices.html', deviceNames=activeDevices)

@bp.route('/active_devices/agents', methods=['POST'])
def getRequestFromAgent():
    global done_discovering
    if request.method == "POST":
        done_discovering = True
    return ('', 204)

@bp.route('/active_devices/ajax', methods=['POST'])
def sendRequestToControlAgent():
    if request.method == "POST":
        data = request.data.decode('utf-8')
        print("decoded data" + data)
        data = json.loads(data)
        print("id: " + data["id"])
        pubsub.publish('control', 'setDeviceStatus', data)
    return data

def loadActiveDevices():
    conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
    curs = conn.cursor()
    curs.execute("SELECT id, manufacturer, name, image FROM ActiveDevices;")
    devices = curs.fetchall()
    displayData = []
    for device in devices:
        displayData.append([device[0], device[1] + ' ' + device[2], device[3]])
    curs.close()
    conn.close()
    return displayData
