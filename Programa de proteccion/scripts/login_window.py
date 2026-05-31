from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from storage import password_exists, save_password, load_password
from dashboard_window import DashboardWindow


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SDR - Inicio de Sesión")
        self.setFixedSize(450, 350)  # Tamaño fijo para que luzca como una app moderna

        # Estilo global de la ventana
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f6f9;
            }
            QLabel#logo {
                font-size: 60px;
            }
            QLabel#title {
                color: #1e3a8a;
                font-size: 26px;
                font-weight: bold;
            }
            QLabel#subtitle {
                color: #334155;
                font-size: 13px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #cbd5e1;
                border: none;
                border-radius: 18px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QLineEdit:focus {
                background-color: #e2e8f0;
                border: 2px solid #3b82f6;
            }
            QPushButton {
                background-color: #0284c7;
                color: white;
                border: none;
                border-radius: 18px;
                padding: 10px 0px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0369a1;
            }
            QPushButton:pressed {
                background-color: #075985;
            }
        """)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        # Layout principal centrado
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(50, 20, 50, 20)

        # Logo (Simulado con Emojis según el Mockup)
        self.logo = QLabel("🛡️👁️")
        self.logo.setObjectName("logo")
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        # Título principal
        self.title = QLabel("Bienvenido a SDR")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # Subtítulo dinámico
        self.label = QLabel()
        self.label.setObjectName("subtitle")
        self.label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label)

        # Input de contraseña
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("••••••••")
        self.password_input.setFixedSize(250, 36)
        
        # Centrar el input
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        self.layout.addLayout(input_layout)

        # Espaciador antes del botón
        self.layout.addSpacing(10)

        # Botón dinámico
        self.button = QPushButton()
        self.button.setFixedSize(140, 36)
        self.button.clicked.connect(self.handle_button)
        
        # Centrar el botón
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.button, alignment=Qt.AlignCenter)
        self.layout.addLayout(btn_layout)

        self.central.setLayout(self.layout)

        # Lógica de creación o login
        if password_exists():
            self.mode = "login"
            self.label.setText("Ingrese contraseña")
            self.button.setText("Conectar")
        else:
            self.mode = "create"
            self.label.setText("Cree una contraseña segura")
            self.button.setText("Guardar")

    def handle_button(self):
        password = self.password_input.text()

        if self.mode == "create":
            if password == "":
                QMessageBox.warning(self, "Error", "La contraseña no puede estar vacía")
                return

            save_password(password)
            QMessageBox.information(self, "Éxito", "Contraseña guardada correctamente")
            self.open_main()

        else:
            saved_password = load_password()
            if password == saved_password:
                self.open_main()
            else:
                QMessageBox.warning(self, "Error", "Contraseña incorrecta")
                self.password_input.clear()

    def open_main(self):
        self.main_window = DashboardWindow()
        self.main_window.show()
        self.close()