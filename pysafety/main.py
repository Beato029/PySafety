HTML = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="utf-8">
    <title>Mappa del mondo</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link
        rel="stylesheet"
        href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
        integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
        crossorigin=""
    />

    <style>
        html, body, #map {
            width: 100%;
            height: 100%;
            margin: 0;
            padding: 0;
            background: #000;
            overflow: hidden;
        }

        .leaflet-container {
            background: #000;
            font-family: Arial, sans-serif;
        }

        .leaflet-interactive:focus,
        path:focus,
        svg path:focus {
            outline: none !important;
        }

        .country-tooltip {
            background: rgba(0, 0, 0, 0.96);
            color: #ffffff;
            border: 1px solid #7a7a7a;
            border-radius: 8px;
            box-shadow: 0 0 12px rgba(0,0,0,0.55);
            padding: 6px 10px;
            font-size: 13px;
            line-height: 1.35;
        }

        .country-tooltip .name {
            font-weight: 700;
            font-size: 14px;
        }

        .leaflet-pane.labels-pane {
            pointer-events: none !important;
        }

        .leaflet-tile {
            image-rendering: auto;
        }

        #mouseCoords {
            position: absolute;
            left: 10px;
            bottom: 10px;
            z-index: 2000;
            background: rgba(0, 0, 0, 0.82);
            color: white;
            border: 1px solid #3a3a3a;
            border-radius: 10px;
            padding: 8px 10px;
            font-size: 13px;
            min-width: 170px;
        }
    </style>
</head>
<body>
<div id="map"></div>
<div id="mouseCoords">Lat: --<br>Lon: --</div>

<script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
    crossorigin="">
</script>

<script>
    const map = L.map('map', {
        zoomControl: true,
        worldCopyJump: true,
        preferCanvas: false,
        attributionControl: true
    }).setView([20, 0], 2);

    map.createPane('countriesPane');
    map.getPane('countriesPane').style.zIndex = 450;

    map.createPane('labelsPane');
    map.getPane('labelsPane').style.zIndex = 650;
    map.getPane('labelsPane').classList.add('labels-pane');

    L.tileLayer(
        'https://{s}.basemaps.cartocdn.com/dark_nolabels/{z}/{x}/{y}{r}.png',
        {
            maxZoom: 20,
            subdomains: 'abcd',
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
        }
    ).addTo(map);

    L.tileLayer(
        'https://{s}.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}{r}.png',
        {
            maxZoom: 20,
            subdomains: 'abcd',
            pane: 'labelsPane',
            attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
        }
    ).addTo(map);

    function getCountryName(props) {
        return (
            props.ADMIN ||
            props.admin ||
            props.NAME ||
            props.name ||
            props.SOVEREIGNT ||
            props.sovereignt ||
            "Stato sconosciuto"
        );
    }

    function escapeHtml(text) {
        return String(text ?? "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function buildTooltip(countryName) {
        return `<div class="name">${escapeHtml(countryName)}</div>`;
    }

    function defaultStyle() {
        return {
            pane: 'countriesPane',
            color: '#050505',
            weight: 1,
            opacity: 1,
            fillColor: '#000000',
            fillOpacity: 0.04,
            interactive: true
        };
    }

    function highlightStyle() {
        return {
            color: '#ffffff',
            weight: 2,
            opacity: 1,
            fillColor: '#000000',
            fillOpacity: 0.04
        };
    }

    let geojsonLayer = null;

    fetch('https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson')
        .then(response => {
            if (!response.ok) {
                throw new Error('Errore HTTP nel caricamento dei confini');
            }
            return response.json();
        })
        .then(data => {
            geojsonLayer = L.geoJSON(data, {
                pane: 'countriesPane',
                style: defaultStyle,
                onEachFeature: function(feature, layer) {
                    const countryName = getCountryName(feature.properties || {});

                    layer.bindTooltip(buildTooltip(countryName), {
                        sticky: true,
                        direction: 'top',
                        className: 'country-tooltip',
                        opacity: 1
                    });

                    layer.on('add', function() {
                        if (layer._path) {
                            layer._path.setAttribute('tabindex', '-1');
                            layer._path.style.outline = 'none';
                        }
                    });

                    layer.on({
                        mouseover: function(e) {
                            e.target.setStyle(highlightStyle());

                            if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
                                e.target.bringToFront();
                            }
                        },

                        mouseout: function(e) {
                            geojsonLayer.resetStyle(e.target);
                        },

                        mousedown: function(e) {
                            if (e.originalEvent) {
                                e.originalEvent.preventDefault();
                            }
                        },

                        click: function(e) {
                            if (e.originalEvent) {
                                e.originalEvent.preventDefault();
                                e.originalEvent.stopPropagation();
                            }
                        }
                    });
                }
            }).addTo(map);
        })
        .catch(error => {
            console.error(error);
            alert('Impossibile caricare i confini dei Paesi. Controlla la connessione Internet.');
        });

    map.on('mousemove', function(e) {
        document.getElementById('mouseCoords').innerHTML =
            'Lat: ' + e.latlng.lat.toFixed(4) + '<br>Lon: ' + e.latlng.lng.toFixed(4);
    });
</script>
</body>
</html>
"""

from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWebEngineWidgets import QWebEngineView
import sys
from server import Server

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySafety")

        cursor = QPixmap("./cursor/cursor.png")
        self.setCursor(QCursor(cursor, 0, 0))

        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        perc = 0.65
        w = int(screen_geometry.width() * perc)
        h = int(screen_geometry.height() * perc)

        self.setMinimumSize(w, h)

        # widget centrale
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(10)
        self.central_widget.setLayout(self.main_layout)

        self.top_layout = QHBoxLayout()
        self.bottom_layout = QHBoxLayout()

        self.main_layout.addLayout(self.top_layout, 1)
        self.main_layout.addLayout(self.bottom_layout, 1)

        self.setStyleSheet("""
            QWidget {
                background-color: black;
            }

            QMenuBar {
                background-color: #111111;
                color: white;
                border-bottom: 1px solid #30363d;
            }

            QMenuBar::item {
                background: transparent;
                padding: 6px 12px;
            }

            QMenuBar::item:selected {
                background: #21262d;
            }

            QMenu {
                background-color: #161b22;
                color: white;
                border: 1px solid #30363d;
            }

            QMenu::item {
                padding: 6px 20px;
            }

            QMenu::item:selected {
                background-color: #1f3a5f;
            }

            QTableWidget {
                background-color: #0d1117;
                alternate-background-color: #161b22;
                gridline-color: #21262d;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px;
                selection-background-color: #1f3a5f;
                selection-color: #58a6ff;
                font-family: 'DejaVu Sans Mono', 'Monospace';
                font-size: 11px;
                font-weight: bold;
            }

            QTableWidget::item {
                padding: 4px 8px;
                border-bottom: 1px solid #1c2128;
            }

            QTableWidget::item:selected {
                background-color: #1f3a5f;
                color: #58a6ff;
            }

            QHeaderView::section {
                background-color: #161b22;
                color: #8b949e;
                border: none;
                border-right: 1px solid #30363d;
                border-bottom: 1px solid #30363d;
                padding: 6px 10px;
                font-weight: 700;
                font-size: 11px;
            }

            QHeaderView::section:hover {
                background-color: #21262d;
                color: #c9d1d9;
            }
                           
            QPlainTextEdit, QTextEdit {
                background-color: #0d1117;           
                border: 1px solid #30363d;
                border-radius: 6px;
                font-family: 'Consolas', 'Monospace';
                font-size: 15px;
                color: white;
                selection-background-color: #264f78;
            }
            
            #widget-map, #widget-log, #widget-clientInfo, #widget-terminal {
                background-color: #0d1117;
                border: 1px solid #30363d;
                border-radius: 6px;
                font-family: 'Consolas', 'Monospace';
                font-size: 15px;
                color: white;
            }
        """)

        # self._menu_bar()

        self._client_info()
        self._map()
        
        self._terminal()
        self._log()
        self.server = Server(terminal=self.terminal, table=self.table, log=self.log)
        self.server.terminal_signal.connect(self.terminal.insertPlainText)
        self.server.server_signal.connect(self.server.addRow)
        self.server.log_signal.connect(self.write_log)
        
    def resizeEvent(self, event):
        super().resizeEvent(event)

    def _menu_bar(self):
        menubar = self.menuBar()

        # Menu File
        file_menu = menubar.addMenu("File")

        new_action = QAction("Nuovo", self)
        open_action = QAction("Apri", self)
        save_action = QAction("Salva", self)
        exit_action = QAction("Esci", self)

        exit_action.triggered.connect(self.close)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Menu Plugins
        plugins_menu = menubar.addMenu("Plugins")

        map_action = QAction("Map", self)

        plugins_menu.addAction(map_action)

        # Menu Server
        server_menu = menubar.addMenu("Server")

        create_action = QAction("Create", self)
        start_action = QAction("Start", self)
        stop_action = QAction("Stop", self)
        status_action = QAction("Status", self)

        start_action.triggered.connect(lambda: print("Server avviato"))
        stop_action.triggered.connect(lambda: print("Server fermato"))
        status_action.triggered.connect(lambda: print("Stato server richiesto"))

        server_menu.addAction(create_action)
        server_menu.addAction(start_action)
        server_menu.addAction(stop_action)
        server_menu.addAction(status_action)

        # Menu Client
        client_menu = menubar.addMenu("Client")

        # Eventuale menu Aiuto
        help_menu = menubar.addMenu("Aiuto")
        about_action = QAction("Info", self)
        about_action.triggered.connect(
            lambda: QMessageBox.information(self, "Info", "PySafety v1.0")
        )
        help_menu.addAction(about_action)

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

    def _client_info(self):
        self.client_info_widget = QWidget()
        self.client_info_widget.setObjectName("widget-clientInfo")

        client_layout = QVBoxLayout(self.client_info_widget)
        client_layout.setContentsMargins(0, 0, 0, 0)
        
        self.counter = 0

        self.table = QTableWidget(self.client_info_widget)
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "#", "Date", "Public IP", "Port" ,"Destination", "~Country" ,"~City"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)

        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)

        # self.table.removeRow(0)

        client_layout.addWidget(self.table)
        self.top_layout.addWidget(self.client_info_widget, 2)

    def _terminal(self):
        self.terminal_widget = QWidget()
        self.terminal_widget.setObjectName("widget-terminal")

        terminal_layout = QVBoxLayout(self.terminal_widget)
        terminal_layout.setContentsMargins(0, 0, 0, 0)
        terminal_layout.setSpacing(0)

        self.terminal = QPlainTextEdit(self.terminal_widget)

        self.terminal.setUndoRedoEnabled(False)
        self.terminal.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.terminal.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.terminal.setCursorWidth(10)

        self.history = []
        self.history_index = 0

        self.terminal.keyPressEvent = self.terminal_keypress
        self.new_prompt()

        terminal_layout.addWidget(self.terminal)
        self.bottom_layout.addWidget(self.terminal_widget, 2)

    def new_prompt(self):
        if self.terminal.toPlainText():
            self.terminal.insertPlainText("\n")
        self.terminal.insertPlainText("root@pysafety:~$ ")
        self.prompt_position = len(self.terminal.toPlainText())
        self.terminal.moveCursor(QTextCursor.MoveOperation.End)

    def terminal_keypress(self, event):
        key = event.key()
        cursor = self.terminal.textCursor()

        if key in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            command = self.terminal.toPlainText()[self.prompt_position:].strip()
            if command:
                self.history.append(command)
            self.history_index = len(self.history)

            self.terminal.insertPlainText("\n")
            self.run_command(command)
            self.new_prompt()
            return

        if key == Qt.Key.Key_Backspace and cursor.position() <= self.prompt_position:
            return

        QPlainTextEdit.keyPressEvent(self.terminal, event)

    def run_command(self, command):
        command = str(command)

        if command.strip() == "":
            self.server.run("server LHOST 0.0.0.0 LPORT 8080 -S")

        elif command == "neofetch":
            self.terminal.insertPlainText("""
██████╗ ██╗   ██╗███████╗ █████╗ ███████╗███████╗████████╗██╗   ██╗
██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██╔════╝██╔════╝╚══██╔══╝╚██╗ ██╔╝
██████╔╝ ╚████╔╝ ███████╗███████║█████╗  █████╗     ██║    ╚████╔╝ 
██╔═══╝   ╚██╔╝  ╚════██║██╔══██║██╔══╝  ██╔══╝     ██║     ╚██╔╝  
██║        ██║   ███████║██║  ██║██║     ███████╗   ██║      ██║   
╚═╝        ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝   ╚═╝      ╚═╝   
            """)
        
        elif command == "server close":
            self.server._server_close()

        elif command.split()[0] == "server":
            self.server.run(command)
            
        elif command == "help":
            self.terminal.insertPlainText("""
server show <LHOST/LPORT>   Visualizza l'host o la porta impostata
server <LHOST/LPORT> <localhost/8080> Imposta host o porta del server
server -S   Avvia il server
            """)

        else:
            self.terminal.insertPlainText("Comando non valido, riprovare")

    def _map(self):
        self.widget_map = QWidget()
        self.widget_map.setObjectName("widget-map")

        map_layout = QVBoxLayout(self.widget_map)
        map_layout.setContentsMargins(1, 1, 1, 1)

        browser = QWebEngineView()
        browser.loadFinished.connect(lambda ok: print("Caricamento HTML:", ok))
        browser.setHtml(HTML, QUrl("https://localhost/"))
        
        # html_file = Path(__file__).resolve().parent / "map.html"
        # browser.load(QUrl.fromLocalFile(str(html_file)))
        

        map_layout.addWidget(browser)
        self.top_layout.addWidget(self.widget_map, 2)

    def _log(self):
        self.widget_log = QWidget()
        self.widget_log.setObjectName("widget-log")

        log_layout = QVBoxLayout(self.widget_log)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.setSpacing(0)

        self.log = QTextEdit(self.widget_log)
        self.log.setReadOnly(True)

        # self.log.setUndoRedoEnabled(False)
        # self.log.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        # self.log.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        # self.log.setCursorWidth(10)

        log_layout.addWidget(self.log)
        self.bottom_layout.addWidget(self.widget_log, 2)

    def write_log(self, content, color):
        self.log.insertHtml(f'<span style="color: {color};">{content}</span><br>')
        self.log.moveCursor(QTextCursor.MoveOperation.End)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())