import socket
import requests



def getIp():
    url = "https://ipinfo.io/json"
    req = requests.get(url)
    ip = req.json()["ip"]
    client.send(str(ip).encode())

client = socket.socket()

HOST = "localhost"
PORT = 8080

client.connect((HOST, PORT))
getIp()
