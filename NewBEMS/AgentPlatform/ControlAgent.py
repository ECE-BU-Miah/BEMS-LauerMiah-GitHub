import threading
import time
import zmq
import subprocess
import sqlite3
import global_settings
import importlib
import json
# from PubsubAgent import PubsubAgent

class ControlAgent():
    def __init__(self, port, topic):
        self.port = port
        self.topic = topic
        self.msg = ''
        threading.Thread(target=self.subscribe, args=(self.topic,)).start()

    def subscribe(self, topic):
        context = zmq.Context()
        with context.socket(zmq.SUB) as socket:
            socket.connect(f"tcp://localhost:{self.port}")
            socket.setsockopt(zmq.SUBSCRIBE, topic)
            while True:
                print("Control agent receiving")
                self.msg = socket.recv().decode('utf-8')
                print(self.msg)
                # topic, method, args = self.msg.split()
                self.processMethod(method, args)
                time.sleep(0.5)
            time.sleep(1)
        context.term()

    def processMethod(self, method, args):
        if method=="setDeviceStatus":
            self.setDeviceStatus(args)

    def setDeviceStatus(self, data):
        # newStatus data format:
        # dictionary with key value pairs WHERE
        # keys are device properties and values are values
        conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
        curs = conn.cursor()
        # data = json.dumps(data.decode('utf-8'))
        print(data)
        # id = data['id']
        # powerState = data['powerState']
        # curs.execute("SELECT api FROM ActiveDevices WHERE id = ?;", (id, ))
        # deviceProperties = curs.fetchall() # tuple nested in list [('WeMo',)]
        # print(deviceProperties)
        # if deviceProperties is not []:
        #     apiName = deviceProperties[0][0]
        #     try:
        #         api_mod = importlib.import_module('DeviceDrivers.' + apiName)
        #     except Exception as e:
        #         print(e)
        # if powerState == "ON":
        #     api_mod.setState(id, "1")
        # elif powerState == "OFF":
        #     api_mod.setState(id, "0")

if __name__ == '__main__':
    controlAgent = ControlAgent("5556", b'control')
