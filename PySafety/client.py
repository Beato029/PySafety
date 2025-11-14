import socket
import requests

HOST = "127.0.0.1"
PORT = 8080

class CLIENT:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.flag = True

    def tryConnect(self):
        i = 0
        while True:
            try:
                print(f"Tentativo di connessione: {str(i)}")
                self.client.connect((HOST, PORT))
                break
            except:
                self.flag = False
                i += 1

        if self.flag:
            self.commands()

    def commands(self):
        while True:
            command = self.client.recv(1024).decode()
            match command:
                case "nets":
                    url = "https://ipinfo.io/json"
                    req = requests.get(url)
                    ip = req.json()["ip"]

                    self.client.send(str(ip).encode())


if __name__ == "__main__":
    start = CLIENT()
    start.tryConnect()