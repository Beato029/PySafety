import colorama
from colorama import Fore
from clear import *
import json
import sys

colorama.init(autoreset=True)

red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
yellow = Fore.LIGHTYELLOW_EX
blue = Fore.LIGHTBLUE_EX
cyan = Fore.LIGHTCYAN_EX
reset = Fore.RESET

def error(text):
    print(red + f"[-] '{text}' Comando non trovato")

def information(text):
    print(blue + f"[*] {text}")

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

    with open("settings.json", "r") as file:
        data = json.load(file)

    return data

def changeData(key, value):
    with open("settings.json", "r") as file:
        data = json.load(file)

    if key in data:
        data[key] = value
    else:
        print("Non trovato")
        sys.exit()

    with open("settings.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def settings():
    while True:
        clear()
        data = readData()
        print(reset + "[" + yellow + "0" + reset + "] " + green + "Host Default: " + red + data["host_default"])
        print(reset + "[" + yellow + "1" + reset + "] " + green + "Port Default: " + blue + data["port_default"])
        print(reset + "[" + yellow + "2" + reset + "] " + green + "Controlla aggiornamenti: " + green + "True" if data["check_update"] == True else reset + "[" + yellow + "2" + reset + "] " + green + "Controlla aggiornamenti: " + red + "False")
        print(reset + "[" + yellow + "R" + reset + "] " + green + "Reset impostazioni")
        print(reset + "[" + yellow + "X" + reset + "/" + yellow + "Q" + reset + "] " + green + "Esci")

        command = input(reset + "(" + red + "settings" + reset + ")> " + cyan).lower()
        match command:
            case "0":
                new_host = input(red + "> " + cyan)
                changeData("host_default", new_host)

            case "1":
                new_port = input(red + "> " + cyan)
                changeData("port_default", new_port)
                
            case "2":
                check_update = readData()
                changeData("check_update", not check_update["check_update"])
            
            case "r":
                changeData("host_default", "127.0.0.1")
                changeData("port_default", "8080")
                changeData("check_update", True)

            case "x" | "q":
                clear()
                break

            case _:
                clear()