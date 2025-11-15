import socket
from alerts import Error
from alerts import Information
from alerts import Success
from alerts import Warning
import threading
import struct
import pickle
import cv2

class Server:
    def __init__(self, host, port, max_connection=50, quit_key="q"):
        self._host_ = host
        self._port_ = port
        self._max_connection_ = max_connection
        self._quit_key_ = quit_key
        self._clientCount_ = 0
        self._running_ = False

        self._server_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._init_socket_()

    def _init_socket_(self):
        self._server_.bind((self._host_, self._port_))

    def start_server(self):
        if self._running_:
            Error("Server già arrivato")

        else:
            self._running_ = True
            server_thread = threading.Thread(target=self._server_listen_)
            server_thread.start()

    def _server_listen_(self):
        Success(f"Server in ascolto su: {self._host_} : {str(self._port_)}")
        self._server_.listen()
        while self._running_:
            conn, addr = self._server_.accept()
            if self._max_connection_ >= self._clientCount_:
                conn.close()
                Error("Non ci sono client liberi")
            else:
                self._clientCount_ += 1

            # thread = threading.Thread(target=self._screen_share_, args=(conn, addr,))
            # thread.start()

    def stop_server(self): # Aggiungere i try
        if self._running_:
            close_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            close_server.connect((self._host_, self._port_))
            close_server.close()
            self._server_.close()

            Success("Server chiuso con successo")
        
        else:
            Error("Il server non è attivo")

    def _screen_share_(self, conn, addr):
        payload_size = struct.calcsize(">L")
        data = b""

        while self._running_:
            break_loop = False

            while len(data) < payload_size:
                received = conn.recv(4096)
                if received == b"":
                    conn.close()
                    self._clientCount_ -= 1
                    break_loop = False
                    break
                data += received

            if break_loop:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack(">L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += conn.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow(str(addr), frame)
            if cv2.waitKey(1) == ord(self._quit_key_):
                conn.close()
                self._clientCount_ -= 1
                break        

serve = Server("localhost", 8080)
serve.start_server()