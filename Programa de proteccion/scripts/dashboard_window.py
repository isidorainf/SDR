"""
Ventana principal del dashboard después del login.
Muestra información del usuario, monitoreo y alertas.
"""
import socket
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
    QInputDialog,
    QLineEdit
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from chat_widget import ChatWidget
from worker_thread import MonitoringWorker
from timestamp_manager import get_minutes_since_last_analysis, format_minutes_to_readable, save_last_analysis_time
from side_menu import SideMenu
from history_window import HistoryWindow
from settings_page import SettingsPage
from storage import load_password


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = None
        self.is_monitoring = False
        self.history_window = None
        self.settings_window = None
        self.skip_password_check = False  # Bandera para evitar doble validación

        self.setWindowTitle("Panel de Control - Protección para Menores")
        self.setGeometry(100, 100, 1000, 750)

        self.init_ui()
        self.setup_side_menu()
        self.start_time_update_timer()

    def init_ui(self):
        """Inicializa la interfaz del dashboard"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # ==================== HEADER ====================
        header_layout = QVBoxLayout()

        # Fila superior con botón de tuerca y título
        top_row_layout = QHBoxLayout()

        # Botón de tuerca (settings)
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setMaximumWidth(50)
        self.settings_btn.setMaximumHeight(50)
        self.settings_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 25px;
                font-size: 20pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
        """)
        self.settings_btn.clicked.connect(self.toggle_side_menu)
        top_row_layout.addWidget(self.settings_btn)

        title = QLabel("Panel de control")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        top_row_layout.addWidget(title, 1)

        # Espacio para balancear
        top_row_layout.addSpacing(50)

        header_layout.addLayout(top_row_layout)

        # Información del usuario y último análisis
        info_layout = QHBoxLayout()

        pc_name = socket.gethostname()
        user_label = QLabel(f"👤 Usuario monitoreado: <b>{pc_name}</b>")
        user_font = QFont()
        user_font.setPointSize(11)
        user_label.setFont(user_font)
        info_layout.addWidget(user_label)

        info_layout.addStretch()

        self.analysis_label = QLabel()
        analysis_font = QFont()
        analysis_font.setPointSize(11)
        self.analysis_label.setFont(analysis_font)
        self.update_analysis_time()
        info_layout.addWidget(self.analysis_label)

        header_layout.addLayout(info_layout)
        main_layout.addLayout(header_layout)

        # ==================== MAIN CONTENT ====================
        content_layout = QHBoxLayout()

        # Panel derecho: Botones de control
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)

        # Botón iniciar monitoreo
        self.start_button = QPushButton("▶️ Comenzar Monitoreo")
        self.start_button.setMinimumHeight(50)
        self.start_button.setMinimumWidth(200)
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12pt;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.start_button.clicked.connect(self.start_monitoring)
        controls_layout.addWidget(self.start_button)

        # Botón detener monitoreo
        self.stop_button = QPushButton("⏹️ Detener Monitoreo")
        self.stop_button.setMinimumHeight(50)
        self.stop_button.setMinimumWidth(200)
        self.stop_button.setEnabled(False)
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12pt;
                padding: 10px;
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
        controls_layout.addWidget(self.stop_button)

        controls_layout.addSpacing(20)

        # Botón Detalles
        self.details_button = QPushButton("📊 Detalles")
        self.details_button.setMinimumHeight(40)
        self.details_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
            QPushButton:pressed {
                background-color: #0056b3;
            }
        """)
        self.details_button.clicked.connect(self.show_details)
        controls_layout.addWidget(self.details_button)

        # Botón Manejo de Alertas
        self.alerts_button = QPushButton("⚠️ Manejo de Alertas")
        self.alerts_button.setMinimumHeight(40)
        self.alerts_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 11pt;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
            QPushButton:pressed {
                background-color: #cc7700;
            }
        """)
        self.alerts_button.clicked.connect(self.manage_alerts)
        controls_layout.addWidget(self.alerts_button)

        controls_layout.addStretch()

        content_layout.addLayout(controls_layout, 0)

        # Panel izquierdo: Chat
        self.chat_widget = ChatWidget()
        content_layout.addWidget(self.chat_widget, 1)

        main_layout.addLayout(content_layout, 1)

        # Estado
        self.status_label = QLabel("Estado: 🔴 Inactivo")
        status_font = QFont()
        status_font.setPointSize(10)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #999;")
        main_layout.addWidget(self.status_label)

        central_widget.setLayout(main_layout)

    def start_time_update_timer(self):
        """Inicia un timer para actualizar el tiempo cada minuto"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_analysis_time)
        self.timer.start(60000)  # Actualizar cada 60 segundos

    def update_analysis_time(self):
        """Actualiza la etiqueta de tiempo desde último análisis"""
        minutes = get_minutes_since_last_analysis()
        readable_time = format_minutes_to_readable(minutes)
        self.analysis_label.setText(f"⏱️ Minutos desde último análisis: <b>{readable_time}</b>")

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

    def show_details(self):
        """Muestra detalles (a implementar)"""
        QMessageBox.information(
            self,
            "Detalles",
            "Funcionalidad de detalles próximamente disponible."
        )

    def manage_alerts(self):
        """Gestiona alertas (a implementar)"""
        QMessageBox.information(
            self,
            "Manejo de Alertas",
            "Funcionalidad de manejo de alertas próximamente disponible."
        )

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

    def closeEvent(self, event):
        """Intercepta el cierre de la ventana - Bloquea la X, solo permite cerrar desde logout"""
        # Si ya se validó la contraseña (desde logout), permitir cierre
        if self.skip_password_check:
            if self.worker:
                self.worker.stop()
            save_last_analysis_time()
            event.accept()
            return

        # Bloquear el cierre con la X - mostrar mensaje
        QMessageBox.warning(
            self,
            "Acción no permitida",
            "No puedes cerrar la aplicación con el botón X.\n\nPara cerrar la sesión, usa el menú lateral (⚙️) y selecciona 'Cerrar sesión'."
        )
        event.ignore()

    def setup_side_menu(self):
        """Configura el menú lateral"""
        self.side_menu = SideMenu(self)
        self.side_menu.history_clicked.connect(self.show_history)
        self.side_menu.guide_clicked.connect(self.show_guide)
        self.side_menu.settings_clicked.connect(self.show_settings)
        self.side_menu.logout_clicked.connect(self.logout)

    def toggle_side_menu(self):
        """Abre o cierra el menú lateral"""
        self.side_menu.toggle_menu()

    def show_history(self):
        """Muestra la ventana de historial"""
        if self.history_window is None or not self.history_window.isVisible():
            self.history_window = HistoryWindow(self)
            self.history_window.show()
        else:
            self.history_window.raise_()
            self.history_window.activateWindow()

    def show_guide(self):
        """Muestra la guía de uso (placeholder)"""
        QMessageBox.information(
            self,
            "Guía de uso",
            "Guía de uso - Próximamente disponible"
        )

    def show_settings(self):
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

    def logout(self):
        """Cierra sesión y vuelve al login"""
        reply = QMessageBox.question(
            self,
            "Cerrar sesión",
            "¿Estás seguro de que quieres cerrar la sesión?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Pedir contraseña antes de cerrar sesión
            password, ok = QInputDialog.getText(
                self,
                "Confirmación",
                "Ingresa tu contraseña para cerrar la sesión:",
                QLineEdit.EchoMode.Password
            )

            if not ok:
                # Usuario presionó Cancelar
                return

            # Validar contraseña
            saved_password = load_password()
            if password != saved_password:
                # Contraseña incorrecta
                QMessageBox.warning(
                    self,
                    "Error",
                    "Contraseña incorrecta. No se cerrará la sesión."
                )
                return

            # Contraseña correcta, proceder con el cierre
            if self.worker:
                self.worker.stop()

            save_last_analysis_time()

            # Volver a LoginWindow
            from login_window import LoginWindow
            self.login_window = LoginWindow()
            self.login_window.show()

            # Cerrar sin volver a pedir contraseña
            self.skip_password_check = True
            self.close()

    def resizeEvent(self, event):
        """Maneja el redimensionamiento de la ventana"""
        super().resizeEvent(event)
        if hasattr(self, 'side_menu'):
            self.side_menu.update_height()
