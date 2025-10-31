import socket

client = socket.socket()

HOST = "localhost"
PORT = 8080

client.connect((HOST, PORT))