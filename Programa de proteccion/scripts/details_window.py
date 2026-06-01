"""
Ventana de Detalles de Alertas (Maestro).
Muestra una lista categorizada de incidentes con acceso a sus medidas.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from alert_logger import read_all_alerts, parse_alert_file

class DetailsWindow(QWidget):
    back_clicked = Signal()

    def __init__(self, parent=None, main_app=None):
        super().__init__()
        self.main_app = main_app
        # Para evitar problemas de importación circular, importamos la otra ventana aquí
        from manage_window import ManageWindow
        self.ManageWindowClass = ManageWindow
        
        self.init_ui()
        self.load_and_sort_alerts()

    def init_ui(self):
        self.setWindowTitle("SDR - Detalles Alertas")
        self.setFixedSize(900, 600)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget { background-color: #f4f6f9; }
            QLabel#main_title {
                color: white; font-size: 28px; font-weight: bold;
                background-color: #1e3a8a; /* Azul oscuro */
                padding: 15px; border-radius: 8px;
            }
            QLabel#subtitle {
                color: #000000; font-size: 16px; font-weight: bold;
                text-decoration: underline; margin-top: 10px;
            }
            QFrame.alert_row {
                background-color: white; border-radius: 10px; padding: 10px;
                border: 1px solid #e2e8f0;
            }
            QLabel.level_pill {
                color: #000000; font-weight: bold; font-size: 14px;
                padding: 5px 15px; border-radius: 15px;
            }
            QLabel.pill_critico { background-color: #fca5a5; }
            QLabel.pill_medio { background-color: #fde047; }
            QLabel.pill_bajo { background-color: #bbf7d0; }
            
            QLabel.alert_reason { color: #334155; font-size: 15px; }
            
            QPushButton.btn_ver {
                background-color: #0284c7; color: white; border-radius: 15px;
                padding: 8px 20px; font-weight: bold; font-size: 14px;
            }
            QPushButton.btn_ver:hover { background-color: #0369a1; }
            
            QPushButton.btn_volver {
                background-color: #0284c7; color: white; border-radius: 20px;
                padding: 10px 40px; font-weight: bold; font-size: 15px;
            }
            QPushButton.btn_volver:hover { background-color: #0369a1; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()
        icon = QLabel("📄")
        icon.setStyleSheet("font-size: 28px; background: transparent;")
        title = QLabel("Detalles Alertas")
        title.setObjectName("main_title")
        title.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(icon)
        header_layout.addWidget(title, 1)
        main_layout.addLayout(header_layout)

        # Subtítulo
        subtitle = QLabel("Resumen de Incidentes")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)

        # Scroll Area para la lista
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        
        self.scroll.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll, 1)

        # Botón Volver
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Volver")
        btn_back.setProperty("class", "btn_volver")
        btn_back.clicked.connect(self.go_back)
        btn_layout.addWidget(btn_back, alignment=Qt.AlignCenter)
        main_layout.addLayout(btn_layout)

    def load_and_sort_alerts(self):
        raw_alerts = read_all_alerts()
        self.parsed_alerts = []

        for fn, fp in raw_alerts:
            data = parse_alert_file(fp)
            if data:
                data['filepath'] = fp
                self.parsed_alerts.append(data)

        # Ordenar: 1º Fecha (Más reciente), 2º Nivel (Crítico > Medio > Bajo)
        def get_level_weight(lvl_str):
            l = lvl_str.lower().replace('í', 'i')
            if 'critico' in l: return 0
            if 'medio' in l: return 1
            if 'bajo' in l: return 2
            return 3

        self.parsed_alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        self.parsed_alerts.sort(key=lambda x: get_level_weight(x.get('level', '')))

        if not self.parsed_alerts:
            empty = QLabel("No hay alertas registradas aún.")
            empty.setAlignment(Qt.AlignCenter)
            empty.setStyleSheet("color: #64748b; font-size: 16px;")
            self.scroll_layout.addWidget(empty)
            return

        for index, alert in enumerate(self.parsed_alerts):
            self.add_alert_row(alert, index)

    def add_alert_row(self, alert, index):
        row = QFrame()
        row.setProperty("class", "alert_row")
        layout = QHBoxLayout(row)
        layout.setContentsMargins(15, 10, 15, 10)

        # Nivel (Píldora)
        lvl_str = alert.get('level', 'BAJO').upper()
        lbl_lvl = QLabel(lvl_str)
        lbl_lvl.setProperty("class", "level_pill")
        
        weight = lvl_str.lower().replace('í', 'i')
        if 'critico' in weight: lbl_lvl.setProperty("class", "level_pill pill_critico")
        elif 'medio' in weight: lbl_lvl.setProperty("class", "level_pill pill_medio")
        else: lbl_lvl.setProperty("class", "level_pill pill_bajo")
        
        lbl_lvl.setFixedWidth(100)
        lbl_lvl.setAlignment(Qt.AlignCenter)
        layout.addWidget(lbl_lvl)

        # Razón
        reason = QLabel(alert.get('reason', 'Incidente detectado'))
        reason.setProperty("class", "alert_reason")
        reason.setWordWrap(True)
        layout.addWidget(reason, 1)

        # Botón Ver Medidas
        btn_ver = QPushButton("Ver Medidas")
        btn_ver.setProperty("class", "btn_ver")
        btn_ver.clicked.connect(lambda checked, idx=index: self.open_manage_window(idx))
        layout.addWidget(btn_ver)

        self.scroll_layout.addWidget(row)

    def open_manage_window(self, index):
        self.hide()
        self.manage_win = self.ManageWindowClass(self.parsed_alerts, index, previous_window=self)
        self.manage_win.show()

    def go_back(self):
        self.back_clicked.emit()
        self.close()