from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys

# pip install nuitka
# python -m nuitka --onefile --lto=yes --mingw64 tuo_script.py

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySafety Installer")

        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        perc = 0.15
        w = int(screen_geometry.width() * perc)
        h = int(screen_geometry.height() * perc)

        self.setMinimumSize(w, h)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 10)
        # self.main_layout.setSpacing(15)

        self.label = QLabel("Preparazione sistema...")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)

        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 10px;
                background-color: #2a2a2a;
                height: 22px;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                border-radius: 10px;
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d2ff,
                    stop:1 #3a7bd5
                );
            }
        """)

        self.main_layout.addStretch()
        # self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.label)
        self.main_layout.addStretch()

        self.setLayout(self.main_layout)


        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_progress)

        # self.value  = 0
        
        self.askYesUpdate()
        # self.start_loading()

    def clear_window(self):
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    child = item.layout().takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()


    def askYesUpdate(self):
        self.label.setText("Procedere con l'installazione?")

        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: dark-gray;
                border-radius: 20px;
                font-weight: bold;
                font-style: italic;
            }
        """)

        vertical_layout = QVBoxLayout()

        label1 = QLabel("Il software è ancora in fase di sviluppo,", frame)
        label2 = QLabel("la versione disponibile è una beta ad uso esclusivo di test,")
        label3 = QLabel("possono causarsi bug o crash anomali")

        vertical_layout.addWidget(label1, alignment=Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addWidget(label2, alignment=Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addWidget(label3, alignment=Qt.AlignmentFlag.AlignCenter)

        frame.setLayout(vertical_layout)

        horizontal_layout = QHBoxLayout()

        yes_button = QPushButton("Installa")
        yes_button.clicked.connect(self.install)

        no_button = QPushButton("Annulla")
        no_button.clicked.connect(self.close)

        horizontal_layout.addWidget(no_button)
        horizontal_layout.addWidget(yes_button)

        self.main_layout.addWidget(frame)
        self.main_layout.addLayout(horizontal_layout)

    def install(self):
        import requests
        import time

        url = "https://raw.githubusercontent.com/Beato029/PySafety/main/pysafety/main.py"
        output_file = "main.py"

        response = requests.get(url, stream=True)

        if response.status_code != 200:
            from tkinter import messagebox
            messagebox.showerror("Errore", f"Errore: {response.status_code}")
            exit()

        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        chunk_size = 1024

        start_time = time.time()

        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

                    elapsed = time.time() - start_time
                    speed = downloaded / elapsed if elapsed > 0 else 0

                    eta = (total_size - downloaded) / speed if speed > 0 else 0
                    percent = (downloaded / total_size) * 100 if total_size else 0

                    sys.stdout.write(
                        f"\r[{percent:.2f}%] "
                        f"{downloaded/1024:.1f}KB / {total_size/1024:.1f}KB | "
                        f"{speed/1024:.1f} KB/s | "
                        f"ETA: {eta:.1f}s"
                    )
                    sys.stdout.flush()

    def start_loading(self):
        self.value = 0
        self.progress_bar.setValue(self.value)
        self.label.setText("Caricamento in corso...")
        self.timer.start(20)

    def update_progress(self):
        if self.value >= 100:
            self.timer.stop()
            self.label.setText("Caricamento completato ✔")
            return

        # smooth increment
        self.value += 0.8
        self.progress_bar.setValue(int(self.value))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())