"""
Ventana de Guía de Uso.
Muestra instrucciones paso a paso para el usuario.
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont


class GuideWindow(QWidget):
    """Ventana de guía de uso con instrucciones paso a paso"""

    back_clicked = Signal()

    def __init__(self, parent=None, main_app=None):
        super().__init__()
        self.main_app = main_app
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de la guía de uso"""
        self.setWindowTitle("SDR - Guía de Uso")
        
        # --- SOLUCIÓN DE DIMENSIONES ---
        # Garantiza un tamaño base amplio pero permite estirar o maximizar la ventana
        self.setMinimumSize(900, 600)
        self.resize(1000, 700)
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.setStyleSheet("QWidget { background-color: #f4f6f9; }")

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        # Header con botón de volver
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Volver")
        back_btn.setFixedSize(120, 40)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #0284c7;
                color: white;
                border: none;
                border-radius: 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0369a1;
            }
        """)
        back_btn.clicked.connect(self.on_back_clicked)
        header_layout.addWidget(back_btn)

        header_layout.addStretch()

        title = QLabel("📖 Guía de Uso")
        title.setStyleSheet("color: #0f172a; background-color: transparent;")
        title_font = QFont()
        title_font.setPointSize(22)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)

        header_layout.addStretch()
        # Añadimos un espacio invisible a la derecha para equilibrar el botón de la izquierda y centrar el título
        spacer = QLabel()
        spacer.setFixedSize(120, 40)
        header_layout.addWidget(spacer)

        main_layout.addLayout(header_layout)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #cbd5e1; margin-top: 10px; margin-bottom: 10px;")
        main_layout.addWidget(separator)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
                border-radius: 5px;
            }
            QScrollBar:vertical {
                width: 12px;
                background-color: #f1f5f9;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)

        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(10, 10, 20, 10)
        content_layout.setSpacing(20)

        instructions = [
            {
                "number": "1",
                "icon": "🔒",
                "title": "Proteger el Acceso",
                "description": "Configure una contraseña en el inicio para evitar que el sistema sea cerrado o modificado sin su permiso."
            },
            {
                "number": "2",
                "icon": "🛡️",
                "title": "Activar protección",
                "description": "Activa el estado de protección mediante el menú de inicio y en configuraciones defina cada cuántos segundos el sistema debe analizar la pantalla."
            },
            {
                "number": "3",
                "icon": "📊",
                "title": "Monitorear Indicadores",
                "description": "Revisa el \"Detalles de Alertas\" para ver cuántas alertas de nivel bajo, medio o crítico se han detectado hoy."
            },
            {
                "number": "4",
                "icon": "🔍",
                "title": "Analiza y Actúa",
                "description": "Entra en \"Manejo de Alertas\" para leer los mensajes sospechosos resaltados y recibir las recomendaciones de cómo intervenir."
            },
            {
                "number": "5",
                "icon": "📋",
                "title": "Gestión de Historial",
                "description": "Usa la selección de \"Historial\" para revisar incidentes pasados, eliminar registros o descargar reportes detallados para tu seguimiento."
            }
        ]

        for instruction in instructions:
            instruction_box = self.create_instruction_box(instruction)
            content_layout.addWidget(instruction_box)

        content_layout.addStretch()

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)

        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def create_instruction_box(self, instruction):
        """Crea una caja de instrucción"""
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()

        number_icon = QLabel(f"{instruction['icon']} {instruction['number']}")
        number_icon_font = QFont()
        number_icon_font.setPointSize(20)
        number_icon_font.setBold(True)
        number_icon.setFont(number_icon_font)
        # Fondo transparente para evitar fallos de modo oscuro
        number_icon.setStyleSheet("color: #0284c7; background-color: transparent; border: none;") 
        header_layout.addWidget(number_icon)

        title = QLabel(instruction['title'])
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #0f172a; background-color: transparent; border: none;")
        header_layout.addWidget(title)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        description = QLabel(instruction['description'])
        description_font = QFont()
        description_font.setPointSize(11)
        description.setFont(description_font)
        description.setStyleSheet("color: #334155; line-height: 1.6; background-color: transparent; border: none;")
        description.setWordWrap(True)
        layout.addWidget(description)

        box.setLayout(layout)
        return box

    def on_back_clicked(self):
        """Maneja el click en el botón de volver y cierra la ventana actual"""
        self.back_clicked.emit()
        self.close()