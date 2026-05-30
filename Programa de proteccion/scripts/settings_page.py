"""
Página de configuración del sistema.
Permite ajustar preferencias y ver el estado del sistema.
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QCheckBox,
    QSpinBox,
    QScrollArea
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from settings_manager import load_settings, save_settings


class SettingsPage(QWidget):
    """Página de configuración con todas las opciones disponibles"""

    back_clicked = Signal()  # Señal para volver atrás

    def __init__(self, parent=None, main_app=None):
        super().__init__(parent)
        self.main_app = main_app  # Referencia a MainApp para obtener el estado
        self.settings = load_settings()
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de configuración"""
        self.setWindowTitle("⚙️ Configuración")
        self.setGeometry(100, 100, 800, 600)

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # Header con botón de volver
        header_layout = QHBoxLayout()
        back_btn = QPushButton("← Volver")
        back_btn.setFixedSize(100, 35)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11pt;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        back_btn.clicked.connect(self.on_back_clicked)
        header_layout.addWidget(back_btn)

        header_layout.addStretch()

        title = QLabel("⚙️ Configuración del Sistema")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)

        header_layout.addStretch()
        header_layout.addWidget(QLabel(""))  # Espaciador para centrar
        header_layout.children()[3].setFixedWidth(100)

        main_layout.addLayout(header_layout)

        # Área con scroll para el contenido
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)

        # Widget contenedor del scroll
        scroll_content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)

        # ===== SECCIÓN 1: Estado de Protección =====
        self.status_section = self.create_status_section()
        content_layout.addWidget(self.status_section)

        # Más secciones se agregarán aquí...

        content_layout.addStretch()
        scroll_content.setLayout(content_layout)
        scroll_area.setWidget(scroll_content)

        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

        # Aplicar estilo general
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                color: #333;
            }
        """)

    def create_status_section(self):
        """Crea la sección de estado de protección"""
        section = QFrame()
        section.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Título de la sección
        title = QLabel("📊 Estado de Protección")
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Descripción
        desc = QLabel("Estado actual del sistema de monitoreo y protección")
        desc.setStyleSheet("color: #666; font-size: 10pt;")
        layout.addWidget(desc)

        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #e0e0e0;")
        layout.addWidget(separator)

        # Estado actual
        status_layout = QHBoxLayout()

        status_label = QLabel("Estado del sistema:")
        status_label.setStyleSheet("font-size: 11pt; font-weight: bold;")
        status_layout.addWidget(status_label)

        status_layout.addStretch()

        # Indicador de estado (se actualizará dinámicamente)
        self.status_indicator = QLabel()
        self.update_status_indicator()
        status_layout.addWidget(self.status_indicator)

        layout.addLayout(status_layout)

        section.setLayout(layout)
        return section

    def update_status_indicator(self):
        """Actualiza el indicador de estado según si el sistema está corriendo"""
        if self.main_app and self.main_app.is_monitoring:
            self.status_indicator.setText("🟢 Activo")
            self.status_indicator.setStyleSheet("""
                font-size: 11pt;
                font-weight: bold;
                color: #4CAF50;
                background-color: #e8f5e9;
          padding: 8px 15px;
                border-radius: 5px;
            """)
        else:
            self.status_indicator.setText("🔴 Inactivo")
            self.status_indicator.setStyleSheet("""
              font-size: 11pt;
                font-weight: bold;
                color: #f44336;
                background-color: #ffebee;
                padding: 8px 15px;
                border-radius: 5px;
            """)

    def on_back_clicked(self):
        """Maneja el click en el botón volver"""
        self.back_clicked.emit()
        self.close()

    def showEvent(self, event):
        """Se llama cuando se muestra la ventana - actualizar el estado"""
        super().showEvent(event)
        self.update_status_indicator()
