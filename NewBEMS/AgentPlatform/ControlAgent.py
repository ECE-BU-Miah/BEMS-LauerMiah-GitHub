import threading
import time
import zmq
import subprocess
# from PubsubAgent import PubsubAgent

class ControlAgent():
    def __init__(self, port, topic):
        self.port = port
        self.topic = topic
        self.msg = ''

    def subscribe(self, topic):
        context = zmq.Context()
        with context.socket(zmq.SUB) as socket:
            socket.connect(f"tcp://localhost:{self.port}")
            socket.setsockopt(zmq.SUBSCRIBE, topic)
            while True:
                self.msg = socket.recv().decode('utf-8')
                topic, method = self.msg.split()
                self.processMethod(method)
                time.sleep(0.5)
            time.sleep(1)
        context.term()

    def processMethod(self, method):
        if method=="findDevices":
            self.findDevices()

    def findDevices(self):
        print("Found a device!")

    # Set up and start threads calling back to target methods
    def startThreads(self):
        subThread = threading.Thread(target=self.subscribe, args=(self.topic,))
        subThread.start()

if __name__ == '__main__':
    discovery = DiscoveryAgent("5556", b'control')
    discovery.startThreads()
