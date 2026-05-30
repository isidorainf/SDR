"""
Ventana de historial que muestra las alertas capturadas.
Permite ver detalles, eliminar y (próximamente) descargar alertas.
"""
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QMessageBox,
    QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from alert_logger import read_all_alerts, parse_alert_file, delete_alert, get_alert_level_icon


class HistoryWindow(QMainWindow):
    """Ventana de historial de alertas"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.parent_window = parent
        self.setWindowTitle("Historial de Alertas")
        self.setGeometry(100, 100, 1000, 700)
        
        self.init_ui()
        self.load_alerts()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Encabezado con botón de volver
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Volver")
        back_btn.setMaximumWidth(100)
        back_btn.clicked.connect(self.go_back)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        header_layout.addWidget(back_btn)
        
        title = QLabel("📋 Historial de Alertas")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        main_layout.addLayout(header_layout)
        
        # Área de scroll para las alertas
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
        """)
        
        self.alerts_container = QWidget()
        self.alerts_layout = QVBoxLayout()
        self.alerts_layout.setSpacing(15)
        self.alerts_container.setLayout(self.alerts_layout)
        
        scroll.setWidget(self.alerts_container)
        main_layout.addWidget(scroll, 1)
        
        # Label para cuando no hay alertas
        self.empty_label = QLabel("No hay alertas registradas")
        empty_font = QFont()
        empty_font.setPointSize(12)
        self.empty_label.setFont(empty_font)
        self.empty_label.setStyleSheet("color: #999; text-align: center;")
        self.empty_label.setAlignment(Qt.AlignCenter)
        
        central_widget.setLayout(main_layout)
    
    def load_alerts(self):
        """Carga y muestra las alertas"""
        alerts = read_all_alerts()
        
        if not alerts:
            # Mostrar mensaje de vacío
            self.alerts_layout.addWidget(self.empty_label)
            self.alerts_layout.addStretch()
            return
        
        # Mostrar cada alerta
        for filename, filepath in alerts:
            alert_data = parse_alert_file(filepath)
            
            if alert_data:
                alert_widget = self.create_alert_item(alert_data, filename)
                self.alerts_layout.addWidget(alert_widget)
        
        self.alerts_layout.addStretch()
    
    def create_alert_item(self, alert_data, filename):
        """Crea un widget para mostrar una alerta"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Fila 1: Fecha y Nivel
        header_layout = QHBoxLayout()
        
        icon = get_alert_level_icon(alert_data['level'])
        fecha_label = QLabel(f"{icon} {alert_data['fecha']} | {alert_data['level'].upper()}")
        fecha_font = QFont()
        fecha_font.setPointSize(11)
        fecha_font.setBold(True)
        fecha_label.setFont(fecha_font)
        
        header_layout.addWidget(fecha_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Fila 2: Aplicación
        app_layout = QHBoxLayout()
        app_label = QLabel("Aplicación:")
        app_font = QFont()
        app_font.setPointSize(10)
        app_label.setFont(app_font)
        app_label.setStyleSheet("color: #666;")
        
        app_value = QLabel(alert_data['application'])
        app_value_font = QFont()
        app_value_font.setPointSize(10)
        app_value.setFont(app_value_font)
        
        app_layout.addWidget(app_label)
        app_layout.addWidget(app_value)
        app_layout.addStretch()
        
        layout.addLayout(app_layout)
        
        # Fila 3: Infracción
        infraction_layout = QHBoxLayout()
        infraction_label = QLabel("Infracción:")
        infraction_font = QFont()
        infraction_font.setPointSize(10)
        infraction_label.setFont(infraction_font)
        infraction_label.setStyleSheet("color: #666;")
        
        infraction_value = QLabel(alert_data['reason'])
        infraction_value_font = QFont()
        infraction_value_font.setPointSize(10)
        infraction_value.setFont(infraction_value_font)
        infraction_value.setStyleSheet("color: #d32f2f; font-weight: bold;")
        infraction_value.setWordWrap(True)
        
        infraction_layout.addWidget(infraction_label)
        infraction_layout.addWidget(infraction_value)
        infraction_layout.addStretch()
        
        layout.addLayout(infraction_layout)
        
        # Fila 4: Acciones
        actions_layout = QHBoxLayout()
        actions_layout.addStretch()
        
        delete_btn = QPushButton("🗑️ Eliminar")
        delete_btn.setMaximumWidth(120)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_alert(filename))
        
        download_btn = QPushButton("⬇️ Descargar")
        download_btn.setMaximumWidth(120)
        download_btn.setEnabled(False)  # Deshabilitado por ahora
        download_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 12px;
                font-weight: bold;
            }
            QPushButton:hover:!disabled {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #ccc;
            }
        """)
        
        actions_layout.addWidget(delete_btn)
        actions_layout.addWidget(download_btn)
        
        layout.addLayout(actions_layout)
        
        frame.setLayout(layout)
        return frame
    
    def delete_alert(self, filename):
        """Elimina una alerta"""
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Estás seguro de que quieres eliminar esta alerta?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if delete_alert(filename):
                QMessageBox.information(self, "Éxito", "Alerta eliminada correctamente")
                # Recargar la ventana
                self.refresh_alerts()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar la alerta")
    
    def refresh_alerts(self):
        """Recarga las alertas"""
        # Limpiar layout actual
        while self.alerts_layout.count():
            item = self.alerts_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Recargar
        self.load_alerts()
    
    def go_back(self):
        """Vuelve a la ventana anterior"""
        self.close()
        if self.parent_window:
            self.parent_window.show()
