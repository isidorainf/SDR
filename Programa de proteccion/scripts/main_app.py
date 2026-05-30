from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QLineEdit,
    QDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from chat_widget import ChatWidget
from worker_thread import MonitoringWorker
from side_menu import SideMenu
from history_window import HistoryWindow
from settings_page import SettingsPage
import os


class PasswordDialog(QDialog):
    """Dialogo para solicitar contrasena al cerrar"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmar cierre")
        self.setFixedSize(350, 150)
        self.setModal(True)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
                font-size: 11pt;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 11pt;
            }
            QPushButton {
                padding: 8px 20px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 10pt;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Mensaje
        msg_label = QLabel("Ingrese la contrasena para cerrar:")
        msg_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(msg_label)

        # Campo de contrasena
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Contrasena")
        layout.addWidget(self.password_input)

        # Botones
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet("background-color: #999; color: white;")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        self.accept_btn = QPushButton("Aceptar")
        self.accept_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        self.accept_btn.clicked.connect(self.verify_password)
        btn_layout.addWidget(self.accept_btn)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def verify_password(self):
        """Verifica la contrasena"""
        password_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'Proteccion', 'password.txt')
        try:
            with open(password_file, 'r') as f:
                stored_password = f.read().strip()

            if self.password_input.text() == stored_password:
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Contrasena incorrecta")
                self.password_input.clear()
        except:
            # Si no existe archivo, aceptar cualquier contrasena
            self.accept()


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None
        self.is_monitoring = False
        self.side_menu = None
        self.history_window = None
        self.settings_window = None

        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz principal"""
        self.setWindowTitle("Protección para Menores - Sistema de Detección")
        self.setGeometry(100, 100, 900, 700)

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        header_layout = QHBoxLayout()

        title = QLabel("🛡️ Sistema de Monitoreo y Protección")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)

        # Boton de tuerca (menu)
        self.menu_btn = QPushButton("⚙")
        self.menu_btn.setFixedSize(40, 40)
        self.menu_btn.clicked.connect(self.toggle_side_menu)
        self.menu_btn.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 18pt;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        header_layout.addWidget(self.menu_btn)

        header_layout.addStretch()

        self.status_label = QLabel("Estado: Inactivo")
        status_font = QFont()
        status_font.setPointSize(10)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #999;")
        header_layout.addWidget(self.status_label)

        main_layout.addLayout(header_layout)

        # Menu lateral
        self.side_menu = SideMenu(self)
        self.side_menu.guide_clicked.connect(self.on_guide_clicked)
        self.side_menu.history_clicked.connect(self.on_history_clicked)
        self.side_menu.settings_clicked.connect(self.on_settings_clicked)
        self.side_menu.logout_clicked.connect(self.on_logout_clicked)

        button_layout = QHBoxLayout()

        self.start_button = QPushButton("▶️ Iniciar Monitoreo")
        self.start_button.setMinimumHeight(35)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11pt;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.start_button.clicked.connect(self.start_monitoring)
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("⏹️ Detener Monitoreo")
        self.stop_button.setMinimumHeight(35)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11pt;
                padding: 5px;
            }
            QPushButton:hover:!disabled {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #ba0000;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        self.stop_button.clicked.connect(self.stop_monitoring)
        button_layout.addWidget(self.stop_button)

        button_layout.addStretch()

        self.clear_button = QPushButton("🗑️ Limpiar Historial")
        self.clear_button.setMinimumHeight(35)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11pt;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
        """)
        self.clear_button.clicked.connect(self.clear_chat)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

        self.chat_widget = ChatWidget()
        main_layout.addWidget(self.chat_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def start_monitoring(self):
        """Inicia el monitoreo"""
        try:
            self.chat_widget.add_message('estado', 'Iniciando monitoreo...')

            self.worker = MonitoringWorker()

            self.worker.message_signal.connect(self.on_worker_message)
            self.worker.error_signal.connect(self.on_worker_error)
            self.worker.status_signal.connect(self.on_worker_status)

            self.worker.start()

            self.is_monitoring = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.status_label.setText("Estado: 🟢 Monitoreo Activo")
            self.status_label.setStyleSheet("color: #4CAF50; font-weight: bold;")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo iniciar el monitoreo: {str(e)}")
            self.chat_widget.add_message('error', str(e))

    def stop_monitoring(self):
        """Detiene el monitoreo"""
        if self.worker:
            self.chat_widget.add_message('estado', 'Deteniendo monitoreo...')
            self.worker.stop()

            self.is_monitoring = False
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.status_label.setText("Estado: 🔴 Inactivo")
            self.status_label.setStyleSheet("color: #999;")

    def clear_chat(self):
        """Limpia el historial del chat"""
        self.chat_widget.clear_chat()

    def on_worker_message(self, message_dict):
        """Maneja mensajes del worker"""
        tipo = message_dict.get('tipo')
        contenido = message_dict.get('contenido')
        self.chat_widget.add_message(tipo, contenido)

    def on_worker_error(self, error_msg):
        """Maneja errores del worker"""
        self.chat_widget.add_message('error', error_msg)

    def on_worker_status(self, status_msg):
        """Maneja cambios de estado del worker"""
        self.chat_widget.add_message('estado', status_msg)

    def toggle_side_menu(self):
        """Abre o cierra el menu lateral"""
        if self.side_menu.is_open:
            self.side_menu.close_menu()
        else:
            # Posicionar menu en la esquina superior izquierda
            self.side_menu.setGeometry(0, 0, self.side_menu.menu_width, self.height())
            self.side_menu.open_menu()

    def on_guide_clicked(self):
        """Maneja click en Guia de uso"""
        QMessageBox.information(self, "Guia de uso", "Esta es la guia de uso de la aplicacion.")

    def on_history_clicked(self):
        """Abre la ventana de historial"""
        self.hide()
        self.history_window = HistoryWindow(self)
        self.history_window.show()

    def on_settings_clicked(self):
        """Abre la ventana de configuración"""
        self.hide()
        self.settings_window = SettingsPage(parent=None, main_app=self)
        self.settings_window.back_clicked.connect(self.on_settings_back)
        self.settings_window.show()

    def on_settings_back(self):
        """Maneja el retorno desde la ventana de configuración"""
        self.show()
        if self.settings_window:
            self.settings_window.close()
            self.settings_window = None

    def on_logout_clicked(self):
        """Maneja click en Cerrar sesion"""
        reply = QMessageBox.question(
            self, "Cerrar sesion", "Esta seguro de que desea cerrar sesion?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.close()

    def closeEvent(self, event):
        """Se llama cuando se intenta cerrar la aplicacion"""
        # Detener monitoreo si esta activo
        if self.is_monitoring:
            self.stop_monitoring()

        # Solicitar contrasena
        dialog = PasswordDialog(self)
        if dialog.exec() == QDialog.Accepted:
            event.accept()
        else:
            event.ignore()