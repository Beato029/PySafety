from PySafetyServer import Client
import threading

client = Client("192.168.1.54", 8080)

thread = threading.Thread(target=client.start_stream)
thread.start()

while input("> ") != "STOP":
    continue

client.stop_stream()