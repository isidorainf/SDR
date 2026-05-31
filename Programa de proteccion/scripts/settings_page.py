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
    QSpinBox,
    QMessageBox
)
from PySide6.QtCore import Qt, Signal
from settings_manager import load_settings, save_settings


class SettingsPage(QWidget):
    """Página de configuración idéntica al mockup de la Figura 16"""

    back_clicked = Signal()  # Señal para volver atrás

    def __init__(self, parent=None, main_app=None):
        super().__init__(parent)
        self.main_app = main_app
        self.settings = load_settings()
        
        # Variables de estado temporal antes de guardar
        self.temp_protection = True
        self.temp_auto_start = self.settings.get("auto_start", False)
        
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de configuración"""
        self.setWindowTitle("SDR - Configuración")
        self.setFixedSize(600, 450)

        # Estilo global idéntico al mockup
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f6f9;
            }
            QLabel#main_title {
                color: #000000;
                font-size: 24px;
                font-weight: bold;
            }
            QLabel.setting_label {
                color: #333333;
                font-size: 14px;
            }
            QPushButton.setting_btn {
                background-color: #38bdf8;
                color: #000000;
                font-weight: bold;
                border: none;
                border-radius: 15px;
                padding: 6px 12px;
                font-size: 14px;
            }
            QPushButton.setting_btn:hover {
                background-color: #0ea5e9;
            }
            QSpinBox {
                background-color: #38bdf8;
                color: #000000;
                font-weight: bold;
                border: none;
                border-radius: 15px;
                padding: 6px 12px;
                font-size: 14px;
            }
            QPushButton.action_btn {
                background-color: #0284c7;
                color: white;
                border: none;
                border-radius: 18px;
                padding: 8px 25px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton.action_btn:hover {
                background-color: #0369a1;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 30, 40, 30)

        # 1. Título
        title = QLabel("Configuración")
        title.setObjectName("main_title")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        main_layout.addSpacing(20)

        # Contenedor para las filas de configuración
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)

        # 2. Filas de Configuración (Label Izquierda - Botón Derecha)
        self.btn_protection = self.create_setting_row(form_layout, "Estado Protección", "Activado" if self.temp_protection else "Desactivado")
        self.btn_protection.clicked.connect(self.toggle_protection)

        self.btn_auto_start = self.create_setting_row(form_layout, "Inicio Automático", "Activado" if self.temp_auto_start else "Desactivado")
        self.btn_auto_start.clicked.connect(self.toggle_auto_start)

        # Fila especial para el Intervalo (usa QSpinBox en lugar de botón)
        interval_row = QHBoxLayout()
        interval_label = QLabel("Intervalo de Captura (seg)")
        interval_label.setProperty("class", "setting_label")
        interval_row.addWidget(interval_label)
        
        interval_row.addStretch()
        
        self.spin_interval = QSpinBox()
        self.spin_interval.setRange(5, 3600)  # Mínimo 5 seg, Máximo 1 hora
        self.spin_interval.setValue(self.settings.get("capture_interval", 10))
        self.spin_interval.setFixedSize(120, 32)
        self.spin_interval.setAlignment(Qt.AlignCenter)
        interval_row.addWidget(self.spin_interval)
        form_layout.addLayout(interval_row)

        self.btn_words = self.create_setting_row(form_layout, "Palabras a detectar", "Editar")
        self.btn_words.clicked.connect(self.placeholder_action)

        self.btn_password = self.create_setting_row(form_layout, "Cambio de contraseña", "Cambiar")
        self.btn_password.clicked.connect(self.placeholder_action)

        main_layout.addLayout(form_layout)
        main_layout.addSpacing(30)

        # 3. Botones de Acción Final (Guardar y Volver)
        action_layout = QHBoxLayout()
        action_layout.setAlignment(Qt.AlignCenter)
        action_layout.setSpacing(20)

        btn_save = QPushButton("Guardar")
        btn_save.setProperty("class", "action_btn")
        btn_save.setFixedSize(120, 36)
        btn_save.clicked.connect(self.save_and_exit)
        action_layout.addWidget(btn_save)

        btn_back = QPushButton("Volver")
        btn_back.setProperty("class", "action_btn")
        btn_back.setFixedSize(120, 36)
        btn_back.clicked.connect(self.on_back_clicked)
        action_layout.addWidget(btn_back)

        main_layout.addLayout(action_layout)

        self.setLayout(main_layout)

    def create_setting_row(self, layout, label_text, button_text):
        """Función auxiliar para crear las filas del formulario"""
        row = QHBoxLayout()
        
        label = QLabel(label_text)
        label.setProperty("class", "setting_label")
        row.addWidget(label)
        
        row.addStretch()
        
        btn = QPushButton(button_text)
        btn.setProperty("class", "setting_btn")
        btn.setFixedSize(120, 32)
        row.addWidget(btn)
        
        layout.addLayout(row)
        return btn

    def toggle_protection(self):
        self.temp_protection = not self.temp_protection
        self.btn_protection.setText("Activado" if self.temp_protection else "Desactivado")

    def toggle_auto_start(self):
        self.temp_auto_start = not self.temp_auto_start
        self.btn_auto_start.setText("Activado" if self.temp_auto_start else "Desactivado")

    def placeholder_action(self):
        QMessageBox.information(self, "Aviso", "Esta funcionalidad se integrará en la siguiente fase.")

    def save_and_exit(self):
        """Guarda la configuración en el JSON y vuelve al Dashboard"""
        self.settings["auto_start"] = self.temp_auto_start
        self.settings["capture_interval"] = self.spin_interval.value()
        
        save_settings(self.settings)
        
        QMessageBox.information(self, "Éxito", "Configuración guardada correctamente.")
        self.on_back_clicked()

    def on_back_clicked(self):
        """Cierra la ventana y emite la señal para mostrar el Dashboard"""
        self.back_clicked.emit()
        self.close()