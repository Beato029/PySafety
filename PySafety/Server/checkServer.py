from clear import *
import colorama
from colorama import Fore
import json
import socket
import time

colorama.init(autoreset=True)

red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
blue = Fore.LIGHTBLUE_EX
cyan = Fore.LIGHTCYAN_EX
reset = Fore.RESET

def error(text):
    print(red + f"[-] {text}")

def information(text):
    print(blue + f"[*] {text}")

def success(text):
    print(green + f"[✔] {text}")


def readData():
    try:
        with open("settings.json", "r") as file:
            data = json.load(file)
    except:
        with open("settings.json", "w") as file:
            data = {
                "host_default": "127.0.0.1",
                "port_default": "8080",
                "check_update": True
            }
            data_json = json.dumps(data)
            json.dump(data_json, file, indent=4, ensure_ascii=True)

    return data

def checkBind(host, port):
    try:
        check_server = socket.socket()
        check_server.bind((host, int(port)))
        check_server.close()
        time.sleep(0.1)
        success(f"Host: {host} OK!")
        time.sleep(0.1)
        success(f"Porta: {port} OK!")
    except socket.gaierror:
        error("Host non valido")
    except ValueError:
        error("Porta non valida")
    except OverflowError:
        error("La porta deve essere tra 0 e 65535")

    return True

def setHostAndPort():
    information("Lascia i campi vuoti per usare i dati di default")
    host = input(green + "Scegli l'Host > " + cyan)
    if host in ["", " "]:
        host = readData()["host_default"]

    port = input(green + "Scegli la porta > " + cyan)
    if port in ["", " "]:
        port = readData()["port_default"]

    if checkBind(host, port):
        from Server.server import Server
        startServer = Server(host, int(port))
        startServer.start()


def checkServer():
    clear()
    setHostAndPort()