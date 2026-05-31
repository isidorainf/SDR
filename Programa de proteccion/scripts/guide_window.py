"""
Ventana de Guía de Uso.
Muestra instrucciones paso a paso para utilizar el SDR.
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class GuideWindow(QWidget):
    """Página de Guía de Uso idéntica al mockup de la Figura 14"""

    back_clicked = Signal()

    def __init__(self, parent=None, main_app=None):
        super().__init__(parent)
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("SDR - Guía de Uso")
        self.setFixedSize(850, 500)

        # Estilo global de la Guía
        self.setStyleSheet("""
            QWidget {
                background-color: #e0f2fe; /* Fondo celeste muy claro */
            }
            QLabel#main_title {
                color: #ffffff;
                font-size: 26px;
                font-weight: bold;
                background-color: #38bdf8;
                border-radius: 10px;
                padding: 10px;
            }
            QFrame.guide_box {
                background-color: #bfdbfe;
                border: 2px solid #7dd3fc;
                border-radius: 15px;
                padding: 15px;
            }
            QLabel.box_title {
                color: #000000;
                font-size: 15px;
                font-weight: bold;
                margin-bottom: 5px;
            }
            QLabel.box_text {
                color: #334155;
                font-size: 13px;
            }
            QPushButton.action_btn {
                background-color: #0284c7;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 40px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton.action_btn:hover {
                background-color: #0369a1;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)

        # Título Superior
        title = QLabel("Guía de Uso")
        title.setObjectName("main_title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Grilla para las cajas de información
        grid = QGridLayout()
        grid.setSpacing(20)

        # Caja 1
        box1 = self.create_info_box("1. Proteger el acceso", 
            "Configure una contraseña en el inicio para evitar que el sistema sea cerrado o modificado sin su permiso.")
        grid.addWidget(box1, 0, 0)

        # Caja 2
        box2 = self.create_info_box("2. Activar Protección", 
            "Vaya a Configuración, active el estado de protección y defina cada cuántos segundos el sistema debe analizar la pantalla.")
        grid.addWidget(box2, 0, 1)

        # Caja 3
        box3 = self.create_info_box("3. Monitorear Indicadores", 
            "Revise el 'Resumen de Alertas' para ver cuántas alertas de nivel Bajo, Medio o Crítico se han detectado hoy.")
        grid.addWidget(box3, 1, 0)

        # Caja 4
        box4 = self.create_info_box("4. Analiza y Actúa", 
            "Entre en 'Detalles Alertas' para leer los mensajes sospechosos resaltados y recibir las recomendaciones de cómo intervenir.")
        grid.addWidget(box4, 1, 1)

        main_layout.addLayout(grid)

        # Caja 5 (Ocupa todo el ancho abajo)
        box5 = self.create_info_box("5. Gestión de Historial", 
            "Use la sección de 'Historial' para revisar incidentes pasados, eliminar registros o descargar reportes detallados para su seguimiento.")
        main_layout.addWidget(box5)

        main_layout.addStretch()

        # Botón Volver
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Volver")
        btn_back.setProperty("class", "action_btn")
        btn_back.clicked.connect(self.on_back_clicked)
        btn_layout.addWidget(btn_back, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def create_info_box(self, title_text, body_text):
        """Crea una tarjeta de información redondeada"""
        frame = QFrame()
        frame.setProperty("class", "guide_box")
        layout = QVBoxLayout()
        
        title = QLabel(title_text)
        title.setProperty("class", "box_title")
        
        body = QLabel(body_text)
        body.setProperty("class", "box_text")
        body.setWordWrap(True)
        
        layout.addWidget(title)
        layout.addWidget(body)
        layout.addStretch()
        frame.setLayout(layout)
        return frame

    def on_back_clicked(self):
        self.back_clicked.emit()
        self.close()