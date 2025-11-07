import socket
from clear import *
import colorama
from colorama import Fore
import socket
import time
import threading
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

def success(text):
    print(green + f"[✔] {text}")

def waitingConnectionsHelp():
    COMMANDS = ["help", "cls/clear", "quit", "nets", "connect <ID>"]
    DESCRIPTIONS = [
        "",
        ""
    ]
    i = 0
    for comm in COMMANDS:
        print(" " * 4 + reset + "[" + yellow + str(i) + reset + "] " + yellow + COMMANDS[i])
        i += 1

        
class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.acceptConnection = True
        self.clientCount = 0
        self.clients = []
        self.ip_clients = []

        self.setBindServer()
        
    def setBindServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def start(self):
        self.server.listen()
        time.sleep(0.1)
        success(f"In ascolto su: {blue + self.host + green} ~ {red + str(self.port)}")
        time.sleep(0.1)
        print(green + "In attesa di connessioni...")
        
        self.thread = threading.Thread(target=self.multiThreadAccept)
        self.thread.start()

        self.commands()


    def multiThreadAccept(self):
        while self.acceptConnection:
            try:
                self.conn, addr = self.server.accept()
                self.clientCount += 1
                self.clients.append(self.conn)
                ip_client = self.conn.recv(1024).decode()
                self.ip_clients.append(ip_client)
            except ConnectionAbortedError:
                pass
            except:
                pass
        for conn in self.clients:
            conn.close()
        success("Connessioni terminate")


    def commands(self):
        while True:
            command = input(reset + "(" + red + self.host + green + "~" + blue + str(self.port) + reset + ")" + green + "$ " + cyan)
            if command == "help":
                    waitingConnectionsHelp()

            elif command == "cls" or command == "clear":
                clear()
                success(f"In ascolto su: {blue + self.host + green} ~ {red + str(self.port)}")
                print(green + "In attesa di connessioni...")

            elif command == "quit":
                if self.AskCloseConnection():
                    break

            elif command == "nets":
                self.nets()

            elif command.startswith("connect "):
                id = command.rsplit()[1]
                if id < len(self.clientCount):
                    self.connect(id)
                else:
                    print(red + "Client non trovato")


            elif command == "" or command == " ":
                pass

            else:
                error(command)

    def AskCloseConnection(self):
        if input(reset + "Sei sicuro di voler chiudere il Server? [Y/N] " + red).lower() == "y":
            self.acceptConnection = False
            self.server.close()
            self.thread.join(timeout=5)
            success("Server chiuso")
            return True
        else:
            print("Operazione annullata")

    def nets(self):
        print(green + f"Client connessi: {str(self.clientCount)}")
        print("recupero informazioi sui client connessi...")
        if len(self.clients) > 0:
            i = 0
            for conn in self.clients:
                try:
                    conn.send("nets".encode())
                    print(f"{i}\t{self.ip_clients[i]}\tConnected")
                except:
                    print(f"{i}\t{self.ip_clients[i]}\tDisconnected")

                i += 1
        else:
            print(red + "Non ci sono client connessi")

    def connect(self, id):
        pass