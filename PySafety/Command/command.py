import colorama
from colorama import Fore
from clear import *

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

def help_():
    COMMANDS = ["help", "cls/clear", "quit", "server", "client", "settings"]
    DESCRIPTIONS = [
        "",
        ""
    ]
    i = 0
    for comm in COMMANDS:
        print(" " * 4 + reset + "[" + yellow + str(i) + reset + "] " + yellow + COMMANDS[i])
        i += 1


def commands():
    information("Digita 'help' per visualizzare i comandi")
    while True:
        command = input(reset + "(" + red + "pysafety" + reset + ")> " + cyan)
        match command:
            case "help":
                help_()
            
            case "cls" | "clear":
                clear()
                information("Digita 'help' per visualizzare i comandi")
            
            case "quit":
                break

            case "server":
                from Server import checkServer
                checkServer.checkServer()

            case "client":
                pass

            case "settings":
                from Settings import settings
                settings.settings()

            case "" | " ":
                pass

            case _:
                error(command)

