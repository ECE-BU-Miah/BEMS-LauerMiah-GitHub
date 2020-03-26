from machine import Pin, PWM
import socket
import time

print('here')
HOST, PORT = "", 1200

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.setblocking(True)
server.listen(1)

led = Pin(5, Pin.OUT) # Corresponds to D1

p4 = Pin(4) # Corresponds to D2
pwmPin = PWM(p4)
pwmPin.freq(500)
pwmPin.duty(0)

pwmValue = 0

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
        elif strData.startswith('PWM'): # format 'PWM: <int:value>'
            pwmValue = int(strData.split(' ')[1])
            if isinstance(pwmValue, int):
                pwmPin.duty(pwmValue)
            else:
                pass
        else:
            pass # invalid command entered
    client.close()
server.close()
