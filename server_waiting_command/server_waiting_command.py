from colors import Colors
from jsonPy import readJson, writeJson
import time
from alerts import Information
from alerts import Warning
from alerts import Success
from alerts import Error
from pysafetySC import Server

red, green, blue, yellow, magenta, cyan, reset = Colors()

class ServerConfig:
    def __init__(self):

        host = input(reset + "Inserisci l'host (premi invio per usare l'host predefinit)> " + red)
        port = input(reset + "Inserisci la porta (premi invio per usare la porta predefinita)> " + red)
        if host == "":
            host = readJson("settings.json")["default_host"]
        if port == "":
            port = readJson("settings.json")["default_port"]
        
        server = Server(host, port)
        server.start_server()
        # Parte dei comandi durante l'attesa di connessioni

        time.sleep(0.2)
        Information("Digita 'help' per visualizzare i comandi disponibili")
        while True:
            command = input(reset + "(" + green + "pysafety" + reset + ")" + green + "~" + reset + "(" + blue + host + green + "~" + red + port + reset + ")" + green + "> "  + red)
            
            if command == "":
                pass


    def _help_(self):
        commands = [
            "nets",
            "connect <ID>",
            "help",
            "quit"
        ]

        descriptions = [
            "Visualizza i client connessi"
            "Connetti ad un client"
            "Visualizza i comandi disponibili",
            "Chiudi il server"
        ]