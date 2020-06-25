import threading
import time
import zmq
import subprocess
import importlib
import json
import sqlite3

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
        # print("Starting main loop!")
        while True:
            #print("Receiving!")
            self.msg = socket.recv().decode('utf-8')
            #print(self.msg)
            topic, method, args = self.msg.split()
            self.processMethod(method, args)
            #print("Sleeping!")
            time.sleep(0.5)
        context.term()

    def processMethod(self, method, args):
        if method=="searchForDevices":
            self.searchForDevices(args)

    def searchForDevices(self, args):
        ids = json.loads(args)
        conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
        curs = conn.cursor()
        #print(ids)
        for id in ids:
            curs.execute("SELECT api FROM SupportedDevices WHERE id = ?", (id,))
            api = curs.fetchone()[0]
            #print(api)
            urlList = list()
            if api is not None:
                # The directory NewBEMS must be on the PYTHONPATH variable
                # for this to work. Do this by adding the directory to the
                # directories.pth file in the site-packages directory.
                try:
                    api_mod = importlib.import_module('DeviceDrivers.' + api + 'API')
                except Exception as e:
                    pass
                urlList = api_mod.findDevices()
                #print(urlList)
                for url in urlList:
                    metadata = api_mod.findMetadata(url)
                    #print(metadata)
                    self.setDeviceToActive(metadata)
        curs.close()
        conn.close()

    def setDeviceToActive(self, metadata):
        conn = sqlite3.connect(global_settings.WEBSERVER_DIR + 'meta.db')
        curs = conn.cursor()
        #print('Executing cursor!')
        curs.execute("SELECT id FROM ActiveDevices WHERE name = ?;", (metadata['name'],))
        result = curs.fetchall()
        #print(result)
        if result == []:
            try:
                #print('Adding device to active devices')
                curs.execute("INSERT INTO ActiveDevices (name, manufacturer, macaddress) VALUES (?, ?, ?);", (metadata['name'], metadata['manufacturer'], metadata['macaddress']))
                # For debugging:
                #curs.execute("SELECT * FROM ActiveDevices;")
                #print("Active devices table: ")
                #print(curs.fetchall())
            except Exception as e:
                #print("Insertion into active devices failed")
                print(e)
        curs.close()
        conn.close()

if __name__ == '__main__':
    discoveryAgent = DiscoveryAgent("5556", "discovery")
