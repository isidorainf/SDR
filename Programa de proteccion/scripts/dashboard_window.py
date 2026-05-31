"""
Ventana principal del dashboard.
Muestra información del usuario, contadores semafóricos y monitoreo.
"""
import socket
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QMessageBox, QDialog, QLineEdit, QFrame
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from worker_thread import MonitoringWorker
from timestamp_manager import get_minutes_since_last_analysis, format_minutes_to_readable, save_last_analysis_time
from side_menu import SideMenu
from history_window import HistoryWindow
from settings_page import SettingsPage
from storage import load_password
from guide_window import GuideWindow
from alert_logger import read_all_alerts, parse_alert_file

class LogoutDialog(QDialog):
    """Diálogo personalizado para cerrar sesión idéntico al mockup"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SDR - Cerrar Sesión")
        self.setFixedSize(400, 300)
        
        self.setStyleSheet("""
            QDialog { background-color: #f4f6f9; }
            QLabel#logo { font-size: 50px; }
            QLabel#title { color: #000000; font-size: 24px; font-weight: bold; }
            QLabel#subtitle { color: #475569; font-size: 12px; }
            QLabel#input_label { color: #000000; font-weight: bold; font-size: 13px; }
            QLineEdit { background-color: #cbd5e1; border: none; border-radius: 18px; padding: 8px 15px; font-size: 14px; }
            QPushButton { background-color: #0284c7; color: white; border: none; border-radius: 15px; padding: 8px 0px; font-size: 14px; font-weight: bold; }
            QPushButton:hover { background-color: #0369a1; }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)

        logo = QLabel("🛡️👁️")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        title = QLabel("Cerrar Sesión")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("Por seguridad debe ingresar su contraseña")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        layout.addSpacing(10)

        input_label = QLabel("Contraseña")
        input_label.setObjectName("input_label")
        input_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(input_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedSize(200, 36)
        
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)
        layout.addLayout(input_layout)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setFixedSize(80, 30)
        self.btn_ok.clicked.connect(self.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_ok, alignment=Qt.AlignCenter)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def get_password(self):
        return self.password_input.text()


class DashboardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.is_monitoring = False
        self.skip_password_check = False
        
        self.setWindowTitle("SDR - Panel de Control")
        self.setFixedSize(900, 600)
        
        # EL ORDEN CORRECTO ESTÁ AQUÍ
        self.init_ui()                 # 1. Dibuja la interfaz (incluyendo los óvalos)
        self.setup_side_menu()         # 2. Prepara el menú
        self.start_time_update_timer() # 3. Inicia el reloj
        self.update_analysis_time()    # 4. Actualiza los textos y números YA DIBUJADOS

    def init_ui(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #f4f6f9; }
            QLabel#main_title { color: white; font-size: 26px; font-weight: bold; background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #0ea5e9); padding: 10px; border-radius: 8px; }
            QLabel#status_indicator { color: #16a34a; font-weight: bold; font-size: 16px; }
            QLabel.info_text { color: #334155; font-size: 15px; }
            QLabel#resumen_title { color: #0f172a; font-weight: bold; font-size: 18px; background-color: #bae6fd; padding: 5px 15px; border-radius: 10px; }
            
            /* Estilos de los Óvalos de Contadores */
            QFrame#frame_counters { background-color: #e0f2fe; border-radius: 15px; }
            QFrame.oval { border-radius: 50px; }
            QFrame#oval_bajo { background-color: #bbf7d0; border: 3px solid #22c55e; }
            QFrame#oval_medio { background-color: #fef08a; border: 3px solid #eab308; }
            QFrame#oval_critico { background-color: #fecaca; border: 3px solid #ef4444; }
            
            QLabel.oval_title { color: #000000; font-weight: bold; font-size: 16px; }
            QLabel.oval_val { color: #000000; font-weight: bold; font-size: 28px; }
            
            /* Botones de Acción */
            QPushButton.action_btn { background-color: #0284c7; color: white; border-radius: 20px; padding: 10px 30px; font-weight: bold; font-size: 15px; }
            QPushButton.action_btn:hover { background-color: #0369a1; }
            QPushButton#toggle_btn { background-color: #10b981; color: white; border-radius: 20px; padding: 10px 30px; font-weight: bold; font-size: 15px; }
            QPushButton#toggle_btn:hover { background-color: #059669; }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # --- HEADER ---
        header_layout = QHBoxLayout()
        
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setFixedSize(50, 50)
        self.settings_btn.setStyleSheet("QPushButton { background-color: transparent; font-size: 24px; border: none; } QPushButton:hover { background-color: #e2e8f0; border-radius: 25px; }")
        self.settings_btn.clicked.connect(self.toggle_side_menu)
        header_layout.addWidget(self.settings_btn)

        title = QLabel("Panel de Control")
        title.setObjectName("main_title")
        title.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title, 1)
        header_layout.addSpacing(50) # Balance
        main_layout.addLayout(header_layout)

        # --- ESTADO Y USUARIO ---
        self.status_label = QLabel("🔴 Protección Desactivada")
        self.status_label.setObjectName("status_indicator")
        self.status_label.setStyleSheet("color: #dc2626;") 
        self.status_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.status_label)

        info_layout = QHBoxLayout()
        pc_name = socket.gethostname()
        user_label = QLabel(f"Usuario Monitoreado: <b>{pc_name}</b>")
        user_label.setProperty("class", "info_text")
        
        self.analysis_label = QLabel()
        self.analysis_label.setProperty("class", "info_text")
        
        info_layout.addWidget(user_label, alignment=Qt.AlignLeft)
        info_layout.addWidget(self.analysis_label, alignment=Qt.AlignRight)
        main_layout.addLayout(info_layout)

        # --- RESUMEN DE ALERTAS (Óvalos) ---
        resumen_layout = QVBoxLayout()
        resumen_title = QLabel("Resumen de Alertas")
        resumen_title.setObjectName("resumen_title")
        resumen_layout.addWidget(resumen_title, alignment=Qt.AlignLeft)

        frame_counters = QFrame()
        frame_counters.setObjectName("frame_counters")
        counters_layout = QHBoxLayout(frame_counters)
        counters_layout.setContentsMargins(30, 20, 30, 20)
        counters_layout.setSpacing(40)

        self.lbl_bajo = self.create_oval("BAJO", "oval_bajo", counters_layout)
        self.lbl_medio = self.create_oval("MEDIO", "oval_medio", counters_layout)
        self.lbl_critico = self.create_oval("CRÍTICO", "oval_critico", counters_layout)

        resumen_layout.addWidget(frame_counters)
        main_layout.addLayout(resumen_layout)

        main_layout.addStretch()

        # --- BOTONES INFERIORES ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)

        self.toggle_btn = QPushButton("▶️ Activar Protección")
        self.toggle_btn.setObjectName("toggle_btn")
        self.toggle_btn.clicked.connect(self.toggle_monitoring)
        btn_layout.addWidget(self.toggle_btn)

        btn_detalles = QPushButton("Historial de Incidentes")
        btn_detalles.setProperty("class", "action_btn")
        btn_detalles.clicked.connect(self.show_history)
        btn_layout.addWidget(btn_detalles)

        btn_manejo = QPushButton("Manejo Alertas")
        btn_manejo.setProperty("class", "action_btn")
        btn_manejo.clicked.connect(self.manage_alerts)
        btn_layout.addWidget(btn_manejo)

        main_layout.addLayout(btn_layout)

    def create_oval(self, title_text, obj_name, parent_layout):
        """Crea el diseño de un óvalo con su número"""
        oval = QFrame()
        oval.setObjectName(obj_name)
        oval.setProperty("class", "oval")
        oval.setFixedSize(140, 100)
        
        layout = QVBoxLayout(oval)
        layout.setAlignment(Qt.AlignCenter)
        
        lbl_title = QLabel(title_text)
        lbl_title.setProperty("class", "oval_title")
        lbl_title.setAlignment(Qt.AlignCenter)
        
        lbl_val = QLabel("0")
        lbl_val.setProperty("class", "oval_val")
        lbl_val.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_val)
        parent_layout.addWidget(oval)
        
        return lbl_val

    def update_counters(self):
        """Lee la carpeta alertas y suma los contadores"""
        alerts = read_all_alerts()
        c_bajo = c_medio = c_critico = 0
        
        for _, filepath in alerts:
            data = parse_alert_file(filepath)
            if data:
                lvl = data.get('level', '').lower()
                if 'bajo' in lvl or 'low' in lvl: c_bajo += 1
                elif 'medio' in lvl or 'medium' in lvl: c_medio += 1
                elif 'critico' in lvl or 'critical' in lvl: c_critico += 1
                
        self.lbl_bajo.setText(str(c_bajo))
        self.lbl_medio.setText(str(c_medio))
        self.lbl_critico.setText(str(c_critico))

    def start_time_update_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_analysis_time)
        self.timer.start(60000)

    def update_analysis_time(self):
        minutes = get_minutes_since_last_analysis()
        readable_time = format_minutes_to_readable(minutes)
        self.analysis_label.setText(f"Último Análisis: <u>{readable_time}</u>")
        self.update_counters()

    def toggle_monitoring(self):
        """Enciende o apaga el Worker de IA"""
        if not self.is_monitoring:
            try:
                self.worker = MonitoringWorker()
                self.worker.message_signal.connect(self.on_worker_event)
                self.worker.start()
                
                self.is_monitoring = True
                self.toggle_btn.setText("⏹️ Desactivar Protección")
                self.toggle_btn.setStyleSheet("background-color: #ef4444;") 
                self.status_label.setText("🟢 Protección Activada")
                self.status_label.setStyleSheet("color: #16a34a;")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo iniciar el monitoreo: {str(e)}")
        else:
            if self.worker:
                self.worker.stop()
            self.is_monitoring = False
            self.toggle_btn.setText("▶️ Activar Protección")
            self.toggle_btn.setStyleSheet("background-color: #10b981;") 
            self.status_label.setText("🔴 Protección Desactivada")
            self.status_label.setStyleSheet("color: #dc2626;")

    def on_worker_event(self, message_dict):
        """Si el worker avisa que detectó una alerta, sumamos los contadores"""
        if message_dict.get('tipo') == 'alerta':
            self.update_counters()

    def manage_alerts(self):
        QMessageBox.information(self, "Manejo de Alertas", "Funcionalidad de manejo de alertas se implementará en la próxima fase.")

    def closeEvent(self, event):
        if self.skip_password_check:
            if self.worker: self.worker.stop()
            save_last_analysis_time()
            event.accept()
            return

        QMessageBox.warning(self, "Acción no permitida", "Para cerrar la aplicación de forma segura, usa el Menú lateral (⚙️) y selecciona 'Cerrar sesión'.")
        event.ignore()

    def setup_side_menu(self):
        self.side_menu = SideMenu(self)
        self.side_menu.history_clicked.connect(self.show_history)
        self.side_menu.guide_clicked.connect(self.show_guide)
        self.side_menu.settings_clicked.connect(self.show_settings)
        self.side_menu.logout_clicked.connect(self.logout)

    def toggle_side_menu(self):
        self.side_menu.toggle_menu()

    def show_history(self):
        self.hide()
        self.history_window = HistoryWindow(parent=None, main_app=self)
        self.history_window.back_clicked.connect(self.on_history_back)
        self.history_window.show()

    def on_history_back(self):
        self.show()
        if hasattr(self, 'history_window') and self.history_window:
            self.history_window.close()
            self.history_window = None
            self.update_counters() 

    def show_guide(self):
        self.hide()
        self.guide_window = GuideWindow(parent=None, main_app=self)
        self.guide_window.back_clicked.connect(self.on_guide_back)
        self.guide_window.show()

    def on_guide_back(self):
        self.show()
        if hasattr(self, 'guide_window') and self.guide_window:
            self.guide_window.close()
            self.guide_window = None

    def show_settings(self):
        self.hide()
        self.settings_window = SettingsPage(parent=None, main_app=self)
        self.settings_window.back_clicked.connect(self.on_settings_back)
        self.settings_window.show()

    def on_settings_back(self):
        self.show()
        if hasattr(self, 'settings_window') and self.settings_window:
            self.settings_window.close()
            self.settings_window = None

    def logout(self):
        reply = QMessageBox.question(self, "Cerrar sesión", "¿Estás seguro de que quieres cerrar la sesión?", QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            dialog = LogoutDialog(self)
            if dialog.exec() == QDialog.Accepted:
                password = dialog.get_password()
                
                saved_password = load_password()
                if password != saved_password:
                    QMessageBox.warning(self, "Error", "Contraseña incorrecta. No se cerrará la sesión.")
                    return

                if self.worker: self.worker.stop()
                save_last_analysis_time()

                from login_window import LoginWindow
                self.login_window = LoginWindow()
                self.login_window.show()

                self.skip_password_check = True
                self.close()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'side_menu'):
            self.side_menu.update_height()