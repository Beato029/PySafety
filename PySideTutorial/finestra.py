import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QLabel, QTabWidget, QPushButton)
from PyQt6.QtCore import Qt

class SimpleTabWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OnionShare")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Crea il tab widget con le X per chiudere
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)  # Abilita le X
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Aggiungi il pulsante "+" per nuove schede
        self.add_tab_button = QPushButton("+")
        self.add_tab_button.setFixedSize(30, 30)
        self.add_tab_button.clicked.connect(self.add_new_tab)
        self.tab_widget.setCornerWidget(self.add_tab_button)
        
        # Aggiungi una tab iniziale
        self.add_new_tab("Condivisione 1")
        
        layout.addWidget(self.tab_widget)
    
    def add_new_tab(self, title=None):
        if title is None:
            tab_count = self.tab_widget.count()
            title = f"Condivisione {tab_count + 1}"
        
        # Crea un contenuto semplice per la tab
        tab_content = QLabel(f"Contenuto di {title}")
        tab_content.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Aggiungi la tab al tab widget
        index = self.tab_widget.addTab(tab_content, title)
        self.tab_widget.setCurrentIndex(index)
        
        return tab_content
    
    def close_tab(self, index):
        # Impedisce di chiudere l'ultima tab
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Stile minimale per le tab
    app.setStyle('Fusion')
    app.setStyleSheet("""
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
        }
        QTabBar::tab {
            background-color: #e0e0e0;
            border: 1px solid #c0c0c0;
            padding: 8px 12px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background-color: white;
        }
        QTabBar::close-button {
            margin: 2px;
        }
        QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            font-weight: bold;
        }
    """)
    
    window = SimpleTabWindow()
    window.show()
    
    sys.exit(app.exec())