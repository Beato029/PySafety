from PySafetyServer import Server
import threading

server = Server("192.168.1.61", 8080)

thread = threading.Thread(target=server.start_server)
thread.start()

while input("> ") != "STOP":
    continue

server.stop_server()