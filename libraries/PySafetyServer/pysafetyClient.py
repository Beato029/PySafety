import socket
import threading
import pickle
import cv2
import struct
from alerts import Error
from alerts import Information
from alerts import Success
from alerts import Warning

class Client:
    def __init__(self, host, port):
        self._host_ = host
        self._port_ = port
        self._configure()
        self._running_ = False

        self._client_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _configure(self):
        self._encoding_parameteres_ = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def _get_frame(self):
        return None
    
    def _cleanup(self):
        cv2.destroyAllWindows()

    def _client_streaming(self):
        self._client_.connect((self._host_, self._port_))
        while self._running_:
            frame = self._get_frame()
            result, frame = cv2.imencode(".jpg", frame, self._encoding_parameteres_)
            data = pickle.dumps(frame, 0)
            size = len(data)

            try:
                self._client_.sendall(struct.pack(">L", size) + data)
            except ConnectionResetError:
                self._running_ = False
            except ConnectionAbortedError:
                self._running_ = False
            except BrokenPipeError:
                self._running_ = False

        self._cleanup()

    def start_stream(self):
        if self._running_:
            Error("Client già avviato")
        else:
            self._running_ = True
            client_thread = threading.Thread(target=self._client_streaming)
            client_thread.start()

    def stop_stream(self):
        if self._running_:
            self._running_ = False
        else:
            Error("Client not streaming")


client = Client("localhost", 8080)
client.start_stream()