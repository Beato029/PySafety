from logo import Logo
from systemName import getSystemName
import os
from alerts import Information
from alerts import Warning
from alerts import Success
from alerts import Error
from colors import Colors
from jsonPy import readJson
from jsonPy import writeJson
import socket
from pysafetySC import Server, Client
import time
from server_waiting_command import ServerConfig


TYPE = "beta"
VERSION = "1"

def clear():
    machine = getSystemName()
    match machine:
        case "Darwin":
            os.system("clear")
        case "Windows":
            os.system("cls")
        case "Linux":
            os.system("clear")

red, green, blue, yellow, magenta, cyan, reset = Colors()

def _check_binds_(host="localhost", port=8080):
    try:
        port = int(port)
        try:
            check_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            check_socket.bind((host, int(port)))
            check_socket.close()
            return True
        except OverflowError:
            Error("La porta deve essere tra 0 e 65535")
            return False
        except PermissionError:
            Error("Non hai il permesso per avviare il server (l'errore probabile è dovuto alla porta usata)")
            return False
        except socket.gaierror:
            Error("Host non valido")
            return False
        except TypeError:
            Error("Host non valido")
            return False
        except OSError as e:
            if e.errno == 48:
                Error("Server già avviato")
            elif e.errno == 49:
                Error("Host non valido")
            return False
        except:
            Error("Errore, impossibile impostare il campo selezionato")
            return False
    
    except:
        Error("La porta deve essere di tipo intero")


class Menu:
    def __init__(self):
        self._init_menu_()



    def _init_menu_(self):
        clear()
        Logo(green)
        print(green + f"Versione: {TYPE} {VERSION}")
        print(red + "-" * 50)



    def _settings_(self):
        self._init_menu_()
        path = "settings.json"
        if os.path.exists(path):
            try:
                data = readJson(path)

                print()
                print(reset + "[" + yellow + "0" + reset + "] " + green + "Host predefinito: " + red + data["default_host"])
                print(reset + "[" + yellow + "1" + reset + "] " + green + "Porta predefinita: " + blue + data["default_port"])
                print(reset + "[" + yellow + "2" + reset + "] " + green + "Verifica aggiornamenti: ", green + data["check_update"] if data["check_update"] == "True" else red + data["check_update"])
                print(reset + "[" + yellow + "Q" + reset + "] " + green + "Esci dalle impostazioni")
                print()
            except:
                pass
        else:
            data = {
                "default_host": "127.0.0.1",
                "default_port": "8080",
                "check_update": "True",
            }
            writeJson(data, path)
            
            print()
            print(reset + "[" + yellow + "0" + reset + "] " + green + "Host predefinito: " + red + data["default_host"])
            print(reset + "[" + yellow + "1" + reset + "] " + green + "Porta predefinita: " + blue + data["default_port"])
            print(reset + "[" + yellow + "2" + reset + "] " + green + "Verifica aggiornamenti: " + green + data["check_update"] if data["check_update"] == "True" else red + data["check_update"])
            print(reset + "[" + yellow + "Q" + reset + "] " + green + "Esci dalle impostazioni")
            print()

        while True:
            command = input(green + "Scegli un opzione> " + red)
            if command == "0":
                new_host = input(reset + "Inserisci il nuovo host: " + red)
                if _check_binds_(host=new_host):
                    data["default_host"] = new_host
                    writeJson(data, path)
                    self._settings_()
                    break
            
            elif command == "1":
                new_port = input(reset + "Inserisci la nuova porta: " + red)
                if _check_binds_(port=new_port):
                    data["default_port"] = new_port
                    writeJson(data, path)
                    self._settings_()
                    break

            elif command == "2":
                data["check_update"] = "True" if data["check_update"] == "False" else "False"
                writeJson(data, path)
                self._settings_()
                break

            elif command.lower() == "q" or command.lower() == "quit":
                break

            else:
                Error(f"'{command}' Comando non valido, riprovare")

        self._init_menu_()

                

    def _help_(self):
        commands = [
                    "Server",
                    "Client",
                    "Impostazioni",
                    "update",
                    "cls/clear",
                    "help",
                    "quit"
        ]

        descriptions = [
                    "Avvia il Server",
                    "Crea Client",
                    "Cambia impostazioni",
                    "Verifica aggiornamento/aggiorna",
                    "Pulisce lo schermo",
                    "Visualizza i comandi disponibili",
                    "Esci dal programma"
        ]

        i = 0
        print()
        for command in commands:
            print(reset + "\t[" + yellow + str(i) + reset + "] " + yellow + command + " --> " + descriptions[i])
            i += 1
        print()



    def start_menu(self):
        Information("Digital 'help' per visualizzare i comandi disponibili")
        while True:
            command = input(reset + "(" + green + "pysafety" + reset + ")" + blue + "~" + reset + "(" + red + "menu" + reset + ")" + green + "> " + red)
            
            if command == "server" or command == "0":
                # server = ServerConfig()
                Warning("Comando non disponibile, applicazione ancora in fase di sviluppo")

            elif command == "client" or command == "1":
                Warning("Comando non disponibile, applicazione ancora in fase di sviluppo")

            elif command == "settings" or command == "2":
                self._settings_()

            elif command == "update" or command == "3":
                pass

            elif command == "cls" or command == "clear" or command == "4":
                self._init_menu_()

            elif command == "help" or command == "5":
                self._help_()
 
            elif command.lower() == "q" or command.lower() == "quit":
                break
            
            elif command == "" or command == " ":
                pass

            else:
                Error(f"'{command}' Comando non valido, riprovare")



menu = Menu()
menu.start_menu()