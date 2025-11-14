import socket
import threading
import struct
import pickle
import cv2
import pyautogui
import numpy as np

class Server:
    def __init__(self, host, port, max_connection=50, quit_key="q"):
        self._host = host
        self._port = port
        self._max_connection = max_connection
        self._quit_key = quit_key
        self._clientCount = 0
        self._running = False

        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._init_socket()


    def _init_socket(self):
        self._server.bind((self._host, self._port))


    def start_server(self):
        if self._running:
            return "Server già avviato"
        
        else:
            self._running = True
            server_thread = threading.Thread(target=self._server_listen)
            server_thread.start()

    def _server_listen(self):
        self._server.listen()
        while self._running:
            conn, addr = self._server.accept()
            if self._clientCount >= self._max_connection:
                conn.close()
                return "Non ci sono slots liberi"
            else:
                self._clientCount += 1

            thread = threading.Thread(target=self._screen_share, args=(conn, addr,))
            thread.start()

    def stop_server(self):
        if self._running:
            close_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            close_server.connect((self._host, self._port))
            close_server.close()
            self._server.close()

            return "Server chiuso con successo"
        else:
            return "Il Server non è attivo"
        
    def _screen_share(self, conn, addr):
        payload_size = struct.calcsize(">L")
        data = b""

        while self._running:

            break_loop = False

            while len(data) < payload_size:
                received = conn.recv(4096)
                if received == b"":
                    conn.close()
                    self._clientCount -= 1
                    break_loop = True
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
            if cv2.waitKey(1) == ord(self._quit_key):
                conn.close()
                self._clientCount -= 1
                break



class Client:
    def __init__(self, host, port, x_res=1024, y_res=576):
        self._host = host
        self._port = port
        self._configure()
        self._running = False
        self._x_res = x_res
        self._y_res = y_res

        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _configure(self):
        self._encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def _get_frame(self):
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self._x_res, self._y_res), interpolation=cv2.INTER_AREA)
        return frame

    def _cleanup(self):
        cv2.destroyAllWindows()

    def _client_streaming(self):
        self._client.connect((self._host, self._port))
        while self._running:
            frame = self._get_frame()
            result, frame = cv2.imencode('.jpg', frame, self._encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)

            try:
                self._client.sendall(struct.pack(">L", size) + data)
            except ConnectionResetError:
                self._running = False
            except ConnectionAbortedError:
                self._running = False
            except BrokenPipeError:
                self._running = False

        self._cleanup()

    def start_stream(self):
        if self._running:
            print("Client is already streaming!")
        else:
            self._running = True
            client_thread = threading.Thread(target=self._client_streaming)
            client_thread.start()

    def stop_stream(self):
        if self._running:
            self._running = False
        else:
            print("Client not streaming!")