from server import Client
import threading

client = Client("localhost", 8080)

thread = threading.Thread(target=client.start_stream)
thread.start()

while input("> ") != "STOP":
    continue

client.stop_stream()