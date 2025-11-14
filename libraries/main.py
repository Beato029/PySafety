# client_mac_web.py
import socket
import struct
import time
import cv2
import numpy as np
import mss
import mss.tools

class ScreenShareClient:
    def __init__(self, server_host='192.168.1.54', server_port=5000):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.running = False
        self.quality = 80
        
    def connect_to_server(self):
        """Connetti al server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.connect((self.server_host, self.server_port))
            print(f"Connesso al server {self.server_host}:{self.port}")
            print(f"Visualizza lo schermo su: http://{self.server_host}:8080")
            return True
        except Exception as e:
            print(f"Errore nella connessione al server: {e}")
            return False
    
    def capture_screen_mss(self):
        """Cattura lo schermo con mss"""
        try:
            with mss.mss() as sct:
                # Cattura tutto lo schermo
                screenshot = sct.grab(sct.monitors[1])
                
                # Converti in numpy array
                img = np.array(screenshot)
                
                # Converti da BGRA a BGR
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                return img
        except Exception as e:
            print(f"Errore nella cattura con mss: {e}")
            return None
    
    def capture_screen_pyautogui(self):
        """Cattura lo schermo con pyautogui (alternativa)"""
        try:
            import pyautogui
            screenshot = pyautogui.screenshot()
            img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return img
        except Exception as e:
            print(f"Errore nella cattura con pyautogui: {e}")
            return None
    
    def compress_frame(self, frame):
        """Comprime il frame in JPEG"""
        try:
            if frame is None:
                return None
                
            # Riduci dimensione per migliori performance
            scale = 0.6  # Scala al 60% per il web
            height, width = frame.shape[:2]
            new_width = int(width * scale)
            new_height = int(height * scale)
            frame = cv2.resize(frame, (new_width, new_height))
            
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.quality]
            result, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
            
            if result:
                return encoded_frame.tobytes()
            return None
        except Exception as e:
            print(f"Errore nella compressione del frame: {e}")
            return None
    
    def send_frame(self, frame_data):
        """Invia un frame al server"""
        try:
            if frame_data is None:
                return False
                
            # Invia prima la lunghezza del frame
            frame_len = struct.pack('<L', len(frame_data))
            self.socket.sendall(frame_len)
            
            # Invia i dati del frame
            self.socket.sendall(frame_data)
            return True
            
        except Exception as e:
            print(f"Errore nell'invio del frame: {e}")
            return False
    
    def test_capture(self):
        """Testa la cattura dello schermo"""
        print("Test cattura schermo...")
        
        # Prova mss prima
        frame = self.capture_screen_mss()
        if frame is not None:
            print("✓ mss funziona")
            return "mss"
        
        # Prova pyautogui come alternativa
        frame = self.capture_screen_pyautogui()
        if frame is not None:
            print("✓ pyautogui funziona")
            return "pyautogui"
        
        print("✗ Nessun metodo di cattura funziona")
        return None
    
    def start_streaming(self, fps=15):
        """Avvia lo streaming dello schermo"""
        if not self.connect_to_server():
            return
        
        # Testa quale metodo di cattura funziona
        capture_method = self.test_capture()
        if not capture_method:
            print("Impossibile catturare lo schermo")
            return
        
        self.running = True
        frame_interval = 1.0 / fps
        
        print(f"Avvio streaming a {fps} FPS con metodo: {capture_method}")
        print(f"📺 Apri http://{self.server_host}:8080 nel browser per vedere lo schermo")
        print("Premi Ctrl+C per fermare lo streaming")
        
        frame_count = 0
        start_time = time.time()
        
        try:
            while self.running:
                frame_start = time.time()
                frame_count += 1
                
                # Cattura lo schermo con il metodo che funziona
                if capture_method == "mss":
                    frame = self.capture_screen_mss()
                else:
                    frame = self.capture_screen_pyautogui()
                
                if frame is None:
                    continue
                
                # Comprimi il frame
                frame_data = self.compress_frame(frame)
                if frame_data is None:
                    continue
                
                # Invia il frame
                if not self.send_frame(frame_data):
                    print("Errore invio frame, riconnessione...")
                    if not self.connect_to_server():
                        break
                    continue
                
                # Calcola FPS ogni 30 frame
                if frame_count % 30 == 0:
                    elapsed = time.time() - start_time
                    current_fps = 30 / elapsed
                    print(f"FPS attuale: {current_fps:.1f}")
                    start_time = time.time()
                
                # Mantieni il frame rate
                elapsed_frame = time.time() - frame_start
                sleep_time = frame_interval - elapsed_frame
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except KeyboardInterrupt:
            print("\nStreaming interrotto dall'utente")
        except Exception as e:
            print(f"Errore durante lo streaming: {e}")
        finally:
            self.stop_streaming()
    
    def stop_streaming(self):
        """Ferma lo streaming"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("Streaming fermato")

if __name__ == "__main__":
    client = ScreenShareClient()
    
    # Configurazioni
    fps = int(input("Inserisci FPS (default 15): ") or "15")
    quality = int(input("Inserisci qualità (1-100, default 80): ") or "80")
    
    client.quality = max(1, min(100, quality))
    
    client.start_streaming(fps=fps)