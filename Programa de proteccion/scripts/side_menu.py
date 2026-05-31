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
    QFrame
)
from PySide6.QtCore import Qt, Signal, QTimer, QRect, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont

class SideMenu(QWidget):
    """Menú lateral deslizable idéntico al mockup (Figura 11)"""

    guide_clicked = Signal()
    history_clicked = Signal()
    settings_clicked = Signal()
    logout_clicked = Signal()
    menu_toggled = Signal(bool) 

    def __init__(self, parent=None):
        super().__init__(parent)

        self.is_open = False
        self.menu_width = 280 

        self.init_ui()
        self.setup_animation()

        # Configurar como widget flotante sobre el dashboard
        self.setWindowFlags(Qt.Widget)
        
        if parent:
            self.setFixedHeight(parent.height())
            self.move(-self.menu_width, 0) # Iniciar oculto fuera de la pantalla

    def init_ui(self):
        
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("menu_container")

        # Contenedor principal con borde derecho para dar efecto de "cajón"
        self.setStyleSheet("""
            QWidget#menu_container {
                background-color: #bae6fd; /* Celeste sólido que tapará el fondo */
                border-right: 3px solid #0284c7;
            }
            QLabel#menu_title {
                color: #000000;
                font-weight: bold;
                font-size: 22px;
                text-decoration: underline;
            }
            QPushButton.menu_btn {
                background-color: #f0f9ff;
                color: #000000;
                border: 2px solid #0284c7;
                border-radius: 20px;
                padding: 12px 20px;
                text-align: left;
                font-size: 15px;
                font-weight: bold;
                margin: 5px 15px;
            }
            QPushButton.menu_btn:hover {
                background-color: #e0f2fe;
            }
            QPushButton#logout_btn {
                background-color: #fca5a5;
                border: 2px solid #dc2626;
            }
            QPushButton#logout_btn:hover {
                background-color: #f87171;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 30)
        layout.setSpacing(10)

        # Encabezado "MENÚ"
        header_layout = QHBoxLayout()
        title = QLabel("MENÚ")
        title.setObjectName("menu_title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title)
        
        # Botón sutil de cierre
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.clicked.connect(self.toggle_menu)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #000; font-size: 18px; font-weight: bold; border: none;
            }
            QPushButton:hover { color: #dc2626; }
        """)
        header_layout.addWidget(close_btn, alignment=Qt.AlignRight)
        
        layout.addLayout(header_layout)
        layout.addSpacing(30)

        # Botones de navegación
        self.guide_btn = QPushButton("📖 Guía de uso")
        self.guide_btn.setProperty("class", "menu_btn")
        self.guide_btn.clicked.connect(self.on_guide_clicked)
        layout.addWidget(self.guide_btn)

        self.history_btn = QPushButton("📋 Historial")
        self.history_btn.setProperty("class", "menu_btn")
        self.history_btn.clicked.connect(self.on_history_clicked)
        layout.addWidget(self.history_btn)

        self.settings_btn = QPushButton("⚙️ Configuración")
        self.settings_btn.setProperty("class", "menu_btn")
        self.settings_btn.clicked.connect(self.on_settings_clicked)
        layout.addWidget(self.settings_btn)

        layout.addStretch()

        # Botón de Logout abajo
        self.logout_btn = QPushButton("🚪 Cerrar Sesión")
        self.logout_btn.setProperty("class", "menu_btn")
        self.logout_btn.setObjectName("logout_btn")
        self.logout_btn.clicked.connect(self.on_logout_clicked)
        layout.addWidget(self.logout_btn)

        self.setLayout(layout)
        self.setFixedWidth(self.menu_width)

    def setup_animation(self):
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(250)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def toggle_menu(self):
        if self.is_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        if self.is_open: return
        self.is_open = True

        if self.parent():
            self.setFixedHeight(self.parent().height())

        self.raise_()
        self.show()

        start_geometry = QRect(-self.menu_width, 0, self.menu_width, self.height())
        end_geometry = QRect(0, 0, self.menu_width, self.height())

        self.animation.setStartValue(start_geometry)
        self.animation.setEndValue(end_geometry)
        self.animation.start()
        self.menu_toggled.emit(True)

    def close_menu(self):
        if not self.is_open: return
        self.is_open = False

        if self.parent():
            self.setFixedHeight(self.parent().height())

        start_geometry = QRect(0, 0, self.menu_width, self.height())
        end_geometry = QRect(-self.menu_width, 0, self.menu_width, self.height())

        self.animation.setStartValue(start_geometry)
        self.animation.setEndValue(end_geometry)
        self.animation.start()
        self.menu_toggled.emit(False)

    def on_guide_clicked(self):
        self.close_menu()
        self.guide_clicked.emit()

    def on_history_clicked(self):
        self.close_menu()
        self.history_clicked.emit()

    def on_settings_clicked(self):
        self.close_menu()
        self.settings_clicked.emit()

    def on_logout_clicked(self):
        self.close_menu()
        self.logout_clicked.emit()

    def update_height(self):
        if self.parent():
            self.setFixedHeight(self.parent().height())
            if self.is_open:
                self.setGeometry(0, 0, self.menu_width, self.height())
            else:
                self.setGeometry(-self.menu_width, 0, self.menu_width, self.height())