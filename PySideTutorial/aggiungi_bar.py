import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QLabel, QTabWidget, QPushButton)
from PyQt6.QtCore import Qt

class OnionShareWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OnionShare")
        self.setGeometry(100, 100, 900, 700)
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Crea il tab widget identico a OnionShare
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)  # Abilita le X sulle tab
        self.tab_widget.setMovable(True)       # Tab trascinabili
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Aggiungi il pulsante "+" per nuove schede (in alto a destra)
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(30, 30)
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.tab_widget.setCornerWidget(self.add_tab_button)
        
        # Aggiungi una tab iniziale
        self.add_new_tab()
        
        layout.addWidget(self.tab_widget)
    
    def add_new_tab(self):
        tab_count = self.tab_widget.count()
        title = f"Condivisione {tab_count + 1}"
        
        # Crea un contenuto VUOTO per la tab
        tab_content = QWidget()
        
        # Aggiungi la tab al tab widget
        index = self.tab_widget.addTab(tab_content, title)
        self.tab_widget.setCurrentIndex(index)
        
        return tab_content
    
    def close_tab(self, index):
        # Come in OnionShare, impedisce di chiudere l'ultima tab
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Stile IDENTICO a OnionShare
    app.setStyle('Fusion')
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            background-color: white;
            top: -1px;
        }
        QTabBar::tab {
            background-color: #e0e0e0;
            border: 1px solid #c0c0c0;
            border-bottom: none;
            padding: 8px 15px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            font-size: 12px;
            min-width: 120px;
        }
        QTabBar::tab:selected {
            background-color: white;
            border-bottom: 1px solid white;
            margin-bottom: -1px;
        }
        QTabBar::tab:hover {
            background-color: #f0f0f0;
        }
        QTabBar::close-button {
            subcontrol-origin: margin;
            subcontrol-position: right;
            margin-right: 3px;
            margin-top: 3px;
            margin-bottom: 3px;
            image: url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM2NjYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48bGluZSB4MT0iMTgiIHkxPSI2IiB4Mj0iNiIgeTI9IjE4Ij48L2xpbmU+PGxpbmUgeDE9IjYiIHkxPSI2IiB4Mj0iMTgiIHkyPSIxOCI+PC9saW5lPjwvc3ZnPg==);
        }
        QTabBar::close-button:hover {
            background-color: #ff4444;
            border-radius: 2px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 5px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """)
    
    window = OnionShareWindow()
    window.show()
    
    sys.exit(app.exec())