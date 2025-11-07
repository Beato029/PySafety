import sys
import numpy as np
import pyaudio
import soundfile as sf
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
)
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import datetime


class SimpleRecorder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registratore Audio - Registrazione Accumulata")
        self.setGeometry(100, 100, 1000, 500)

        # Config audio
        self.chunk = 2048
        self.rate = 44100
        self.format = pyaudio.paInt16
        self.channels = 1

        self.p = pyaudio.PyAudio()
        self.stream = None
        self.recorded_frames = []

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_recording)

    def init_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("Pronto per registrare...")
        layout.addWidget(self.status_label)

        # Traccia audio registrata
        self.waveform_plot = pg.PlotWidget(title="Audio Registrato")
        self.waveform_curve = self.waveform_plot.plot(pen='y')
        self.waveform_plot.setYRange(-32768, 32768)
        self.waveform_plot.enableAutoRange(x=False, y=False)  # Disabilita autoscale
        layout.addWidget(self.waveform_plot)

        # Pulsanti
        self.start_button = QPushButton("Start / Riavvia")
        self.start_button.clicked.connect(self.start_recording)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop e Salva")
        self.stop_button.clicked.connect(self.stop_recording)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def start_recording(self):
        if self.stream is None:
            self.stream = self.p.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk)
            self.timer.start(30)
            self.status_label.setText("Registrazione in corso...")

    def stop_recording(self):
        if self.stream is not None:
            self.timer.stop()
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

            self.status_label.setText("Registrazione salvata.")
            self.save_audio()

    def update_recording(self):
        if self.stream is None:
            return

        data = self.stream.read(self.chunk, exception_on_overflow=False)
        samples = np.frombuffer(data, dtype=np.int16)
        self.recorded_frames.append(samples)

        full_audio = np.concatenate(self.recorded_frames)

        self.waveform_curve.setData(full_audio)

        # Scroll automatico della visualizzazione
        visible_duration = 5  # secondi da mostrare
        num_samples_visible = int(self.rate * visible_duration)
        total_samples = len(full_audio)

        if total_samples > num_samples_visible:
            start = total_samples - num_samples_visible
            end = total_samples
        else:
            start = 0
            end = num_samples_visible

        self.waveform_plot.setXRange(start, end)


    def save_audio(self):
        if not self.recorded_frames:
            return

        audio_np = np.concatenate(self.recorded_frames).astype(np.int16)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"registrazione_{timestamp}.wav"
        sf.write(filename, audio_np, self.rate)
        print(f"Audio salvato automaticamente: {filename}")

    def closeEvent(self, event):
        self.stop_recording()
        self.p.terminate()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleRecorder()
    window.show()
    sys.exit(app.exec_())
