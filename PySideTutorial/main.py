from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self): 
        super().__init__()

        self.setWindowTitle("BeatoShare")

        width, height = self.getGeometry()
        self.setMinimumSize(width // 2, height // 2)


    def getGeometry(self):
        screen = self.screen()
        screen_size = screen.size()
        width = int(screen_size.width())
        height = int(screen_size.height())

        return width, height

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()