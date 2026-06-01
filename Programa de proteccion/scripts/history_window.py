"""
Ventana de historial que muestra las alertas capturadas.
Permite ver detalles, eliminar y descargar alertas.
"""
import os
import shutil
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from alert_logger import read_all_alerts, parse_alert_file, delete_alert

class HistoryWindow(QWidget):
    back_clicked = Signal()
    
    def __init__(self, parent=None, main_app=None):
        super().__init__()
        self.main_app = main_app
        self.init_ui()
        self.load_alerts()
    
    def init_ui(self):
        self.setWindowTitle("SDR - Historial de Alertas")
        self.setFixedSize(900, 600)
        
        # <--- SOLUCIÓN AL FONDO SUPERPUESTO
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        self.setStyleSheet("""
            QWidget { 
                background-color: #f4f6f9; 
            }
            QLabel#main_title {
                color: white;
                font-size: 26px;
                font-weight: bold;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8b5cf6, stop:1 #06b6d4);
                padding: 15px;
                border-radius: 8px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 5px;
                gridline-color: #e2e8f0;
                font-size: 14px;
                selection-background-color: #e2e8f0; /* Color suave al seleccionar */
                selection-color: #000000;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #e2e8f0;
            }
            QTableWidget::item:selected {
                background-color: #f1f5f9; 
                color: #000000;
            }
            QHeaderView::section {
                background-color: #6366f1;
                color: white;
                font-weight: bold;
                font-size: 15px;
                padding: 10px;
                border: none;
            }
            QPushButton.action_btn {
                background-color: #0284c7;
                color: white;
                border-radius: 18px;
                padding: 10px 40px;
                font-weight: bold;
                font-size: 15px;
            }
            QPushButton.action_btn:hover { 
                background-color: #0369a1; 
            }
            QPushButton.icon_btn {
                background-color: transparent;
                font-size: 22px;
                border: none;
            }
            QPushButton.icon_btn:hover { 
                background-color: #e2e8f0; 
                border-radius: 4px; 
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("Historial de Alertas")
        title.setObjectName("main_title")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # TABLA (Sin las barras de búsqueda inútiles)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Fecha", "Alerta", "Aplicación", "Infracción", "Acciones"])
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch) # Infracción toma el espacio restante
        
        # <--- SOLUCIÓN AL TEXTO CORTADO
        self.table.setWordWrap(True)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        layout.addWidget(self.table)
        
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("Volver al Dashboard")
        btn_back.setProperty("class", "action_btn")
        btn_back.clicked.connect(self.go_back)
        btn_layout.addWidget(btn_back, alignment=Qt.AlignCenter)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def load_alerts(self):
        alerts = read_all_alerts()
        self.table.setRowCount(0)
        
        if not alerts:
            return
        
        for filename, filepath in alerts:
            alert_data = parse_alert_file(filepath)
            
            if alert_data:
                row = self.table.rowCount()
                self.table.insertRow(row)
                
                item_fecha = QTableWidgetItem(alert_data.get('fecha', 'N/A'))
                item_fecha.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 0, item_fecha)
                
                item_nivel = QTableWidgetItem(alert_data.get('level', 'N/A').upper())
                item_nivel.setTextAlignment(Qt.AlignCenter)
                font = QFont(); font.setBold(True)
                item_nivel.setFont(font)
                self.table.setItem(row, 1, item_nivel)
                
                item_app = QTableWidgetItem(alert_data.get('application', 'Desconocida'))
                item_app.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, 2, item_app)
                
                # El texto largo ahora se ajustará automáticamente hacia abajo
                item_reason = QTableWidgetItem(alert_data.get('reason', 'Sin detalles'))
                self.table.setItem(row, 3, item_reason)
                
                action_widget = QWidget()
                action_layout = QHBoxLayout(action_widget)
                action_layout.setContentsMargins(0, 5, 0, 5)
                action_layout.setSpacing(15)
                
                btn_del = QPushButton("🗑️")
                btn_del.setProperty("class", "icon_btn")
                btn_del.setToolTip("Eliminar")
                btn_del.clicked.connect(lambda checked, f=filename: self.delete_alert(f))
                
                btn_down = QPushButton("⬇️")
                btn_down.setProperty("class", "icon_btn")
                btn_down.setToolTip("Descargar Reporte")
                # <--- NUEVA LÓGICA: Botón de descarga activado
                btn_down.clicked.connect(lambda checked, path=filepath: self.download_alert(path))
                
                action_layout.addWidget(btn_del)
                action_layout.addWidget(btn_down)
                
                self.table.setCellWidget(row, 4, action_widget)
    
    def download_alert(self, filepath):
        """Permite al usuario guardar el archivo .txt en otra ubicación (ej. Escritorio)"""
        if not os.path.exists(filepath):
            QMessageBox.warning(self, "Error", "El archivo de alerta ya no existe.")
            return
            
        default_name = os.path.basename(filepath)
        save_path, _ = QFileDialog.getSaveFileName(self, "Descargar Reporte de Alerta", default_name, "Text Files (*.txt)")
        
        if save_path:
            try:
                shutil.copy(filepath, save_path)
                QMessageBox.information(self, "Éxito", f"Reporte guardado correctamente en:\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo: {str(e)}")

    def delete_alert(self, filename):
        reply = QMessageBox.question(self, "Confirmar", "¿Eliminar esta alerta del historial?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if delete_alert(filename):
                self.load_alerts()
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el archivo.")
    
    def go_back(self):
        self.back_clicked.emit()
        self.close()