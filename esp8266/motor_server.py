from machine import Pin
import socket
import time

print('here')
HOST, PORT = "", 1200

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.setblocking(True)
server.listen(1)

led = Pin(5, Pin.OUT)
led.on()
time.sleep(1)
led.off()

print('Starting server')
client, address = server.accept()
print(client)
client.close()
while True:
    client, address = server.accept()
    while True:
        data = client.recv(1024)
        strData = data.decode('utf-8')
        if strData == 'ON':
            print('Turning ON')
            led.on()
        elif strData == 'OFF':
            print('Turning OFF')
            led.off()
        elif strData == 'Q':
            break
    client.close()
server.close()
