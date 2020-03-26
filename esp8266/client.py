import socket
import time

HOST = "192.168.0.14"
PORT = 1200

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST,PORT))

# Continually prompt for user input until Q is entered
try:
    while True:
        data = input("Enter a command (Enter 'Q' to quit): ")
        client.send(bytes(data,'utf-8'))
        if data == 'Q':
            break
except Exception as e:
    print("Socket connection error!")
    print(e)

finally:
    client.close()
