"""
Menú lateral deslizable para el dashboard.
Proporciona acceso a Guía, Historial, Configuración y Cerrar sesión.
"""
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
)
from PySide6.QtCore import Qt, Signal, QTimer, QRect
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import QPropertyAnimation, QEasingCurve


class SideMenu(QWidget):
    """Menú lateral deslizable"""

    # Signals
    guide_clicked = Signal()
    history_clicked = Signal()
    settings_clicked = Signal()
    logout_clicked = Signal()
    menu_toggled = Signal(bool)  # True = abierto, False = cerrado

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_open = False
        self.menu_width = 300  # Aumentado de 250 a 300

        self.init_ui()
        self.setup_animation()

        # Configurar como widget flotante
        self.setWindowFlags(Qt.Widget)

        # Ajustar tamaño inicial
        if parent:
            self.setFixedHeight(parent.height())
            self.move(0, 0)

    def init_ui(self):
        """Inicializa la interfaz del menú"""
        self.setStyleSheet("""
            QWidget {
                background-color: #1e3a5f;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                border: none;
                padding: 20px 25px;
                text-align: left;
                font-size: 14pt;
                font-weight: bold;
                border-radius: 5px;
                margin: 5px 10px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:pressed {
            background-color: #1e40af;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Encabezado
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 15, 20, 15)

        title = QLabel("⚙️ Menú")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: white;")

        header_layout.addWidget(title)
        header_layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setMaximumWidth(50)
        close_btn.setMinimumHeight(40)
        close_btn.clicked.connect(self.toggle_menu)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                font-size: 20pt;
                padding: 5px;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #e74c3c;
                border-radius: 5px;
            }
        """)
        header_layout.addWidget(close_btn)

        layout.addLayout(header_layout)

        # Separador
        separator = QLabel()
        separator.setStyleSheet("background-color: #3b5998; max-height: 2px;")
        layout.addWidget(separator)

        # Espaciado
        layout.addSpacing(10)

        # Botones de menú
        self.guide_btn = QPushButton("📖 Guía de uso")
        self.guide_btn.setMinimumHeight(60)
        self.guide_btn.clicked.connect(self.on_guide_clicked)
        layout.addWidget(self.guide_btn)

        self.history_btn = QPushButton("📋 Historial")
        self.history_btn.setMinimumHeight(60)
        self.history_btn.clicked.connect(self.on_history_clicked)
        layout.addWidget(self.history_btn)

        self.settings_btn = QPushButton("⚙️ Configuración")
        self.settings_btn.setMinimumHeight(60)
        self.settings_btn.clicked.connect(self.on_settings_clicked)
        layout.addWidget(self.settings_btn)

        # Separador antes de logout
        layout.addSpacing(10)
        separator2 = QLabel()
        separator2.setStyleSheet("background-color: #3b5998; max-height: 2px;")
        layout.addWidget(separator2)
        layout.addSpacing(10)

        self.logout_btn = QPushButton("🚪 Cerrar sesión")
        self.logout_btn.setMinimumHeight(60)
        self.logout_btn.clicked.connect(self.on_logout_clicked)
        self.logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border: none;
                padding: 20px 25px;
                text-align: left;
                font-size: 14pt;
                font-weight: bold;
                border-radius: 5px;
                margin: 5px 10px;
            }
            QPushButton:hover {
                background-color: #b91c1c;
            }
            QPushButton:pressed {
                background-color: #991b1b;
            }
        """)
        layout.addWidget(self.logout_btn)

        layout.addStretch()

        self.setLayout(layout)
        self.setFixedWidth(self.menu_width)
        self.hide()

    def setup_animation(self):
        """Configura la animación de deslizamiento"""
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

    def toggle_menu(self):
        """Abre o cierra el menú con animación"""
        if self.is_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        """Abre el menú"""
        if self.is_open:
            return

        self.is_open = True

        # Ajustar altura al padre
        if self.parent():
            parent_height = self.parent().height()
            self.setFixedHeight(parent_height)

        self.show()
        self.raise_()  # Traer al frente

        # Animar desde fuera hacia adentro
        start_x = -self.menu_width
        end_x = 0

        start_geometry = QRect(start_x, 0, self.menu_width, self.height())
        end_geometry = QRect(end_x, 0, self.menu_width, self.height())

        self.animation.setStartValue(start_geometry)
        self.animation.setEndValue(end_geometry)
        self.animation.start()

        self.menu_toggled.emit(True)

    def close_menu(self):
        """Cierra el menú"""
        if not self.is_open:
            return

        self.is_open = False

        # Ajustar altura al padre antes de cerrar
        if self.parent():
            parent_height = self.parent().height()
            self.setFixedHeight(parent_height)

        # Animar desde adentro hacia afuera
        start_x = 0
        end_x = -self.menu_width

        start_geometry = QRect(start_x, 0, self.menu_width, self.height())
        end_geometry = QRect(end_x, 0, self.menu_width, self.height())

        self.animation.setStartValue(start_geometry)
        self.animation.setEndValue(end_geometry)
        self.animation.start()

        # Esperar a que termine la animación antes de hide
        QTimer.singleShot(300, self.hide)

        self.menu_toggled.emit(False)

    def on_guide_clicked(self):
        """Maneja click en Guía de uso"""
        self.close_menu()
        self.guide_clicked.emit()

    def on_history_clicked(self):
        """Maneja click en Historial"""
        self.close_menu()
        self.history_clicked.emit()

    def on_settings_clicked(self):
        """Maneja click en Configuración"""
        self.close_menu()
        self.settings_clicked.emit()

    def on_logout_clicked(self):
        """Maneja click en Cerrar sesión"""
        self.close_menu()
        self.logout_clicked.emit()

    def update_height(self):
        """Actualiza la altura del menú según el padre"""
        if self.parent():
            parent_height = self.parent().height()
            self.setFixedHeight(parent_height)

            # Si está abierto, actualizar la geometría
            if self.is_open:
                self.setGeometry(0, 0, self.menu_width, parent_height)
