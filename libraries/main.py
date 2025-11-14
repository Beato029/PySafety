from server import Server
import threading

server = Server("localhost", 8080)

thread = threading.Thread(target=server.start_server)
thread.start()

while input("> ") != "STOP":
    continue

server.stop_server( )