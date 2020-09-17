import zmq
import time

def publish(topic, method, args=None):
    try:
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:5556")
        # The message must be sent twice to the subscriber in
        # order for it to be properly received. Not totally sure
        # why this is, possibly just the way zmq was designed.
        if args is not None:
            for _ in range(2):
                socket.send(f"{topic} {method}/{args}".encode('utf-8'))
                time.sleep(1)
            print("pubsub publish args: " + str(args))
        else:
            print("Sending message...")
            for _ in range(2):
                socket.send(f"{topic} {method}".encode("utf-8"))
                time.sleep(1)
        socket.close()
        context.term()
    except Exception as e:
        pass
