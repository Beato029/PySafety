import socket
from alerts import Error
from alerts import Success
import threading
import struct
import pickle
import cv2
from colors import Colors

red, green, blue, yellow, magenta, cyan, reset = Colors()

class Server:
    def __init__(self, host, port, max_connection=50, quit_key="q"):
        self._host_ = host
        self._port_ = port
        self._max_connection_ = max_connection
        self._quit_key_ = quit_key
        self._clientCount_ = 0
        self._ips_ = []
        self._machines_ = []
        self._running_ = False
        self._flag_ = False

        self._server_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._check_binds_()

    def _check_binds_(self):
        flag = False

        if type(self._port_) != int:
            try:
                self._port_= int(self._port_)
                flag = True
            except:
                Error("La porta deve essere di tipo intero")

        if flag:
            try:
                check_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                check_socket.bind((self._host_, self._port_))
                check_socket.close()
                self._init_socket_()
                self._flag_ = True
            except OverflowError:
                Error("La porta deve essere tra 0 e 65535")
            except PermissionError:
                Error("Non hai il permesso per avviare il server (l'errore probabilmente è dovuto alla porta usata)")
            except socket.gaierror:
                Error("Host non valido")
            except TypeError:
                Error("Host non valido")
            except OSError as e:
                if e.errno == 48:
                    Error("Server già avviato")
                elif e.errno == 49:
                    Error("Host non valido")
            except:
                Error("Impossibile avviare il server")

    def _init_socket_(self):
        self._server_.bind((self._host_, self._port_))

    def start_server(self):
        # if self._running_:
        #     Error("Server già avviato")

        # else:
        if self._flag_:
            self._running_ = True
            server_thread = threading.Thread(target=self._server_listen_)
            server_thread.start()

    def _server_listen_(self):
        Success(f"Server in ascolto su: {blue + self._host_ + green} ~ {red + str(self._port_)}")
        print("")
        self._server_.listen()
        while self._running_:
            conn, addr = self._server_.accept()
            if self._max_connection_ >= self._clientCount_:
                conn.close()
                Error("Tutti gli slots sono occupati")
            else:
                self._clientCount_ += 1
                ip = conn.recv(1024).decode()
                self._ips_.append(ip)
                machine = conn.recv(1024).decode()
                self._machines_.append(machine)

    def stop_server(self):
        if self._running_:
            close_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            close_server.connect((self._host_, self._port_))
            close_server.close()
            self._server_.close()

            Success("Server chiuso con successo")

    # Screen Share
    def command_execute(self, command):
        pass