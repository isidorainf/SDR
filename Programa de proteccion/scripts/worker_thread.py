from PySide6.QtCore import QThread, Signal
import sys
import os
import time
import ssl
import urllib.request

# Parche para evitar errores de SSL al descargar modelos por primera vez
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Sistema-de-detecci-n-y-recomendaci-n-main'))

from detector import cargar_palabras_riesgo, detectar_riesgo, normalizar_texto
from captura import capturar_y_extraer
from LLM import cadena_mitigacion
from analizador_afectivo import analizar_intencion
from alert_logger import log_dangerous_message

class MonitoringWorker(QThread):
    """Worker thread que ejecuta el ciclo de monitoreo"""
    
    message_signal = Signal(dict)  
    error_signal = Signal(str)     
    status_signal = Signal(str)    
    
    def __init__(self):
        super().__init__()
        self.is_running = False
        self.palabras_riesgo = None
        self.ultimo_texto = ""
        
    def run(self):
        try:
            self.is_running = True
            self.status_signal.emit("Monitoreo iniciado")
            
            self.status_signal.emit("Cargando palabras de riesgo...")
            self.palabras_riesgo = cargar_palabras_riesgo()
            
            self.status_signal.emit(f"Monitoreo activo - {sum(len(p) for p in self.palabras_riesgo.values())} palabras cargadas")
            
            while self.is_running:
                try:
                    texto_extraido = capturar_y_extraer()
                    texto_limpio = normalizar_texto(texto_extraido)
                    
                    self.message_signal.emit({
                        'tipo': 'captura',
                        'contenido': texto_extraido[:200] + "..." if len(texto_extraido) > 200 else texto_extraido
                    })
                    
                    alertas = detectar_riesgo(texto_limpio, self.palabras_riesgo)
                    
                    intencion = analizar_intencion(texto_limpio)
                    
                    if alertas and texto_limpio != self.ultimo_texto and len(texto_limpio) > 10:
                        self.ultimo_texto = texto_limpio
                        
                        # Clasificar nivel de alerta basado en cantidad y tipos
                        nivel_alerta = self.clasificar_alerta(alertas)
                        
                        # Obtener explicación breve
                        razon_breve = self.obtener_razon_alerta(alertas, intencion)
                        
                        # REGISTRAR EN ARCHIVO
                        log_dangerous_message(
                            level=nivel_alerta,
                            content=f"Texto capturado: {texto_extraido}\n\nIntención detectada: {intencion}",
                            reason=razon_breve
                        )
                        
                        alertas_formateadas = "\n".join([f"- {tipo}: {palabra}" for tipo, palabra in alertas])
                        self.message_signal.emit({
                            'tipo': 'alerta',
                            'contenido': f"Alertas detectadas [{nivel_alerta.upper()}]:\n{alertas_formateadas}\n\nIntención: {intencion}"
                        })
                        
                        try:
                            respuesta = cadena_mitigacion.invoke({
                                "texto": texto_limpio,
                                "alertas": alertas_formateadas,
                                "intencion": intencion
                            })
                            
                            respuesta = str(respuesta).strip()
                            
                            self.message_signal.emit({
                                'tipo': 'mitigacion',
                                'contenido': respuesta
                            })
                            
                        except Exception as e:
                            self.error_signal.emit(f"Error en LLM: {str(e)}")
                    
                    time.sleep(5)
                    
                except Exception as e:
                    self.error_signal.emit(f"Error en ciclo de monitoreo: {str(e)}")
                    time.sleep(5)
        
        except Exception as e:
            self.error_signal.emit(f"Error fatal en monitoreo: {str(e)}")
            self.is_running = False
        
        finally:
            self.status_signal.emit("Monitoreo detenido")
    
    def stop(self):
        """Detiene el ciclo de monitoreo"""
        self.is_running = False
        self.wait()
    
    def clasificar_alerta(self, alertas):
        """
        Clasifica el nivel de alerta basado en la cantidad y tipos de alertas
        
        Args:
            alertas (list): Lista de tuplas (tipo, palabra)
        
        Returns:
            str: 'bajo', 'medio' o 'crítico'
        """
        if not alertas:
            return 'bajo'
        
        # Contar por tipo
        tipos = [tipo for tipo, _ in alertas]
        num_alertas = len(alertas)
        
        # Lógica de clasificación
        if num_alertas >= 3 or len(set(tipos)) >= 3:
            return 'crítico'
        elif num_alertas >= 2 or len(set(tipos)) >= 2:
            return 'medio'
        else:
            return 'bajo'
    
    def obtener_razon_alerta(self, alertas, intencion):
        """
        Obtiene una explicación breve de por qué se considera peligroso el mensaje
        
        Args:
            alertas (list): Lista de tuplas (tipo, palabra)
            intencion (str): Intención detectada por el analizador afectivo
        
        Returns:
            str: Explicación breve
        """
        if not alertas:
            return "Comportamiento sospechoso detectado"
        
        tipos = set(tipo for tipo, _ in alertas)
        tipos_list = ', '.join(tipos)
        
        return f"Contenido con categorías de riesgo: {tipos_list}"
