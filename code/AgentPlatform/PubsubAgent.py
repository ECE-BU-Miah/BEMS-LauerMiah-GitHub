import zmq
import time

class PubsubAgent(object):
    def __init__(self, port):
        self.port = port
        self.msg = ""
        self.msgReceived = False

    def publish(self, topic, message):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.connect("")

    def subscribe(self, topic):
        context = zmq.Context()
        with context.socket(zmq.SUB) as socket:
            socket.connect(f"tcp://localhost:5556")
            socket.setsockopt(zmq.SUBSCRIBE, topic)
            while True:
                self.msg = socket.recv().decode('utf-8')
                msgReceived = True
                time.sleep(0.5)
            time.sleep(1)
        context.term()
