from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextCursor, QFont, QColor
from datetime import datetime


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel("📋 Reportes del Monitoreo")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Área de chat
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Segoe UI', Arial;
                font-size: 10pt;
            }
        """)
        layout.addWidget(self.chat_display)
        
        self.setLayout(layout)
    
    def add_message(self, tipo, contenido):
        timestamp = datetime.now().strftime("%H:%M:%S")
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        if tipo == 'captura':
            cursor.insertHtml(f"""
                <div style="margin: 5px 0; padding: 8px; background-color: #e3f2fd; border-left: 4px solid #2196F3; border-radius: 3px;">
                    <span style="color: #666; font-size: 9pt;"><b>[{timestamp}]</b></span>
                    <span style="color: #1976D2; font-weight: bold;"> 📸 Texto capturado:</span><br>
                    <span style="color: #555; font-size: 10pt;">{contenido}</span>
                </div>
            """)
        
        elif tipo == 'alerta':
            cursor.insertHtml(f"""
                <div style="margin: 5px 0; padding: 8px; background-color: #fff3e0; border-left: 4px solid #FF9800; border-radius: 3px;">
                    <span style="color: #666; font-size: 9pt;"><b>[{timestamp}]</b></span>
                    <span style="color: #E65100; font-weight: bold;"> ⚠️ Alerta:</span><br>
                    <span style="color: #555; font-size: 10pt; white-space: pre-wrap;">{contenido}</span>
                </div>
            """)
        
        elif tipo == 'mitigacion':
            cursor.insertHtml(f"""
                <div style="margin: 5px 0; padding: 8px; background-color: #f3e5f5; border-left: 4px solid #9C27B0; border-radius: 3px;">
                    <span style="color: #666; font-size: 9pt;"><b>[{timestamp}]</b></span>
                    <span style="color: #6A1B9A; font-weight: bold;"> 🤖 Recomendación del Sistema:</span><br>
                    <span style="color: #555; font-size: 10pt; white-space: pre-wrap;">{contenido}</span>
                </div>
            """)
        
        elif tipo == 'error':
            cursor.insertHtml(f"""
                <div style="margin: 5px 0; padding: 8px; background-color: #ffebee; border-left: 4px solid #f44336; border-radius: 3px;">
                    <span style="color: #666; font-size: 9pt;"><b>[{timestamp}]</b></span>
                    <span style="color: #C62828; font-weight: bold;"> ❌ Error:</span><br>
                    <span style="color: #555; font-size: 10pt;">{contenido}</span>
                </div>
            """)
        
        elif tipo == 'estado':
            cursor.insertHtml(f"""
                <div style="margin: 5px 0; padding: 8px; background-color: #e8f5e9; border-left: 4px solid #4CAF50; border-radius: 3px;">
                    <span style="color: #666; font-size: 9pt;"><b>[{timestamp}]</b></span>
                    <span style="color: #2E7D32; font-weight: bold;"> ℹ️ Estado:</span><br>
                    <span style="color: #555; font-size: 10pt;">{contenido}</span>
                </div>
            """)
        
        self.chat_display.setTextCursor(cursor)
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def clear_chat(self):
        """Limpia el chat"""
        self.chat_display.clear()
