import threading
import time
import zmq
import subprocess
import importlib
import json
import sqlite3
import requests
import utils
import global_settings

class DiscoveryAgent():
    def __init__(self, port, topic):
        self.port = port
        self.topic = topic
        self.msg = ''
        # print("Starting thread!")
        self.subThread = threading.Thread(target=self.subscribe, args=(self.topic,))
        self.subThread.start()

    def subscribe(self, topic):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(f"tcp://localhost:{self.port}")
        socket.setsockopt(zmq.SUBSCRIBE, topic.encode("utf-8"))
        print("Starting main loop!")
        while True:
            print("Receiving!")
            self.msg = socket.recv().decode('utf-8')
            print(self.msg)
            topic, method = self.msg.split()
            self.processMethod(method)
            print("Sleeping!")
            time.sleep(0.5)
        context.term()

    def processMethod(self, method, args=None):
        if method=="searchForDevices":
            self.searchForDevices()
        elif method=="autoSearchForDevices":
            self.autoSearchForDevices()

    def searchForDevices(self):
        # ids = json.loads(args)
        conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
        curs = conn.cursor()

        curs.execute("SELECT api FROM SupportedDevices;")
        apis = curs.fetchall()
        print(str([api[0] for api in apis]))
        urlList = list()
        for api in apis:
            try:
                api_mod = importlib.import_module('DeviceDrivers.' + api[0] + 'API')
            except Exception as e:
                print(e)
            urlList = api_mod.findDevices()
            # print(urlList)
            for url in urlList:
                metadata = api_mod.findMetadata(url)
                # print("metadata: " + str(metadata))
                self.setDeviceToActive(metadata)
        curs.close()
        conn.close()
        requests.post('http://localhost:5000/active_devices/agents')

    def setDeviceToActive(self, metadata):
        conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
        curs = conn.cursor()
        #print('Executing cursor!')
        curs.execute("SELECT id FROM ActiveDevices WHERE name = ?;", (metadata['name'],))
        result = curs.fetchall()
        # print(result)
        if result == []:
            try:
                print('Adding device to active devices')
                curs.execute("INSERT INTO ActiveDevices (name, manufacturer, macaddress, image, api, ip, port, queryable) VALUES (?, ?, ?, ?, ?, ?, ?);", (metadata['name'], metadata['manufacturer'], metadata['macaddress'], metadata['image'], metadata['api'], metadata['ip'], metadata['port'], metadata['queryable']))
                conn.commit()

                curs.execute("SELECT id FROM ActiveDevices WHERE name=?", (metadata['name']))
                _data = curs.fetchall()
                if _data is not None:
                    id = _data[0][0]
                utils.createDeviceTSDTable(id)
            except Exception as e:
                #print("Insertion into active devices failed")
                print(e)
        curs.close()
        conn.close()

if __name__ == '__main__':
    discoveryAgent = DiscoveryAgent("5556", "discovery")
