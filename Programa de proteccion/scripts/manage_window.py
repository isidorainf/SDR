"""
Ventana de Manejo de Alertas (Detalle).
Visualización del texto específico y recomendaciones para intervenir.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt

class ManageWindow(QWidget):
    def __init__(self, alerts_list, start_index, previous_window=None):
        super().__init__()
        self.alerts_list = alerts_list
        self.current_index = start_index
        self.previous_window = previous_window
        
        self.init_ui()
        self.load_alert(self.current_index)

    def init_ui(self):
        self.setWindowTitle("SDR - Manejo de Alertas")
        self.setFixedSize(900, 600)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget { background-color: #f8fafc; }
            
            /* HEADER */
            QFrame#header_box {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f59e0b, stop:1 #ef4444);
                border-radius: 10px;
            }
            QLabel#main_title, QLabel#header_icon {
                background-color: transparent; /* <--- Esto elimina el parche blanco */
                color: white; 
                font-size: 28px; 
                font-weight: bold; 
            }
            
            /* ALERTA TITULO */
            QLabel#alert_title {
                background-color: #fecaca; /* Rojo clarito de fondo */
                color: #991b1b;            /* Texto rojo oscuro */
                font-size: 22px; font-weight: bold;
                border-radius: 15px; padding: 10px;
                border: 2px solid #ef4444;
            }
            
            /* TEXTO DETECTADO */
            QLabel#detected_text {
                background-color: #7f1d1d; /* Rojo muy oscuro */
                color: white;
                font-size: 16px; font-style: italic;
                border-radius: 15px; padding: 15px;
            }
            
            /* PESTAÑA MEDIDAS */
            QLabel#tab_medidas {
                background-color: #f59e0b; /* Naranja intenso */
                color: white;
                font-size: 16px; font-weight: bold; font-style: italic;
                padding: 8px 20px; 
                border-top-left-radius: 10px; 
                border-top-right-radius: 10px;
            }
            
            /* CAJA MEDIDAS */
            QFrame#box_medidas {
                background-color: #fef3c7; /* Naranja/amarillo muy clarito */
                border: 2px solid #f59e0b;
                border-radius: 10px;
                border-top-left-radius: 0px; 
                padding: 20px;
            }
            QLabel#medidas_content { 
                background-color: transparent; /* <--- Elimina el parche blanco */
                color: #1c1917;                /* Texto oscuro para que se lea perfecto */
                font-size: 16px; 
            }
            
            /* BOTONES NAVEGACIÓN */
            QPushButton.nav_btn {
                background-color: #0284c7; color: white; border-radius: 20px;
                padding: 10px 30px; font-weight: bold; font-size: 15px;
            }
            QPushButton.nav_btn:hover:!disabled { background-color: #0369a1; }
            QPushButton.nav_btn:disabled { background-color: #cbd5e1; color: #94a3b8; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(15)

        # Header Gradiente
        header_box = QFrame()
        header_box.setObjectName("header_box")
        hl = QHBoxLayout(header_box)
        hl.setContentsMargins(15, 10, 15, 10)
        icon = QLabel("📄")
        icon.setObjectName("header_icon")  # Aplicamos la transparencia al icono
        icon.setStyleSheet("font-size: 28px;")
        title = QLabel("Manejo Alertas")
        title.setObjectName("main_title")  # Aplicamos la transparencia al título
        title.setAlignment(Qt.AlignCenter)
        hl.addWidget(icon)
        hl.addWidget(title, 1)
        main_layout.addWidget(header_box)

        # Título de la Alerta
        self.lbl_alert_title = QLabel()
        self.lbl_alert_title.setObjectName("alert_title")
        self.lbl_alert_title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.lbl_alert_title)

        # Texto Detectado
        self.lbl_detected_text = QLabel()
        self.lbl_detected_text.setObjectName("detected_text")
        self.lbl_detected_text.setAlignment(Qt.AlignCenter)
        self.lbl_detected_text.setWordWrap(True)
        main_layout.addWidget(self.lbl_detected_text)

        main_layout.addSpacing(10)

        # Pestaña Medidas
        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(20, 0, 0, 0)
        lbl_tab = QLabel("Medidas de Mitigación")
        lbl_tab.setObjectName("tab_medidas")
        tab_layout.addWidget(lbl_tab)
        tab_layout.addStretch()
        main_layout.addLayout(tab_layout)

        # Caja de Medidas
        box_medidas = QFrame()
        box_medidas.setObjectName("box_medidas")
        ml = QVBoxLayout(box_medidas)
        self.lbl_medidas_content = QLabel()
        self.lbl_medidas_content.setObjectName("medidas_content")
        self.lbl_medidas_content.setWordWrap(True)
        ml.addWidget(self.lbl_medidas_content)
        main_layout.addWidget(box_medidas, 1)

        # Navegación Inferior
        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton("⬅️ Anterior")
        self.btn_prev.setProperty("class", "nav_btn")
        self.btn_prev.clicked.connect(self.go_prev)
        
        self.btn_volver = QPushButton("Volver a Lista")
        self.btn_volver.setProperty("class", "nav_btn")
        self.btn_volver.clicked.connect(self.go_back)
        
        self.btn_next = QPushButton("Siguiente ➡️")
        self.btn_next.setProperty("class", "nav_btn")
        self.btn_next.clicked.connect(self.go_next)

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_volver)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_next)
        
        main_layout.addLayout(nav_layout)

    def load_alert(self, index):
        if not self.alerts_list or index < 0 or index >= len(self.alerts_list):
            return

        alert = self.alerts_list[index]
        lvl = alert.get('level', 'DESCONOCIDO').upper()
        reason = alert.get('reason', 'Sin motivo específico')
        raw_content = alert.get('content', '')

        # Separar el texto capturado de la intención de forma inteligente
        texto_capturado = raw_content
        intencion = "Recomendación: Intervenir y conversar con el menor."
        
        if "Intención detectada:" in raw_content:
            parts = raw_content.split("Intención detectada:")
            texto_capturado = parts[0].replace("Texto capturado:", "").strip()
            intencion = parts[1].strip()
        elif "Texto capturado:" in raw_content:
            texto_capturado = raw_content.replace("Texto capturado:", "").strip()

        # Actualizar UI
        self.lbl_alert_title.setText(f"⚠️ {lvl}: {reason}")
        self.lbl_detected_text.setText(f'Texto detectado: "{texto_capturado}"')
        
        medidas_html = f"""
        <b>Aplicación:</b> {alert.get('application', 'Sistema')}<br><br>
        • <b>Acción inmediata:</b> Revisar el contexto del texto capturado.<br>
        • <b>Análisis IA:</b> {intencion}
        """
        self.lbl_medidas_content.setText(medidas_html)

        # Control de botones
        self.btn_prev.setEnabled(index > 0)
        self.btn_next.setEnabled(index < len(self.alerts_list) - 1)

    def go_prev(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.load_alert(self.current_index)

    def go_next(self):
        if self.current_index < len(self.alerts_list) - 1:
            self.current_index += 1
            self.load_alert(self.current_index)

    def go_back(self):
        if self.previous_window:
            self.previous_window.show()
        self.close()