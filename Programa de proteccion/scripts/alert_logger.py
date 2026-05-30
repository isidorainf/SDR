"""
Gestor de logs de alertas de seguridad.
Almacena cada alerta en un archivo .txt con timestamp, nivel y razón.
"""
import os
from datetime import datetime
from config import LOCAL_DATA_DIR


ALERTAS_DIR = os.path.join(LOCAL_DATA_DIR, 'alertas')


def ensure_alertas_dir():
    """Crea la carpeta de alertas si no existe"""
    os.makedirs(ALERTAS_DIR, exist_ok=True)


def log_dangerous_message(level, content, reason):
    """
    Registra un mensaje peligroso en un archivo .txt
    
    Args:
        level (str): Nivel de alerta (bajo, medio, crítico)
        content (str): Contenido del mensaje peligroso
        reason (str): Explicación de por qué se considera peligroso
    
    Returns:
        str: Ruta del archivo creado, o None si hay error
    """
    try:
        ensure_alertas_dir()
        
        # Crear nombre de archivo con timestamp
        now = datetime.now()
        timestamp = now.strftime("%Y-%m-%d_%H%M%S")
        level_lower = level.lower()
        filename = f"{timestamp}_{level_lower}.txt"
        filepath = os.path.join(ALERTAS_DIR, filename)
        
        # Formato: Primera línea con metadata
        iso_timestamp = now.isoformat()
        header = f"{iso_timestamp} | {level.upper()} | {reason}\n"
        header += "-" * 80 + "\n"
        
        # Escribir archivo
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(header)
            f.write(content)
        
        return filepath
    
    except Exception as e:
        print(f"Error guardando alerta: {e}")
        return None


def read_all_alerts():
    """
    Lee todos los archivos de alertas
    
    Returns:
        list: Lista de tuplas (filename, filepath)
    """
    try:
        ensure_alertas_dir()
        
        if not os.path.exists(ALERTAS_DIR):
            return []
        
        alerts = []
        for filename in sorted(os.listdir(ALERTAS_DIR), reverse=True):
            if filename.endswith('.txt'):
                filepath = os.path.join(ALERTAS_DIR, filename)
                alerts.append((filename, filepath))
        
        return alerts
    
    except Exception as e:
        print(f"Error leyendo alertas: {e}")
        return []


def delete_alert(filename):
    """
    Elimina un archivo de alerta
    
    Args:
        filename (str): Nombre del archivo a eliminar
    
    Returns:
        bool: True si se eliminó, False si error
    """
    try:
        filepath = os.path.join(ALERTAS_DIR, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error eliminando alerta: {e}")
        return False


def parse_alert_file(filepath):
    """
    Parsea un archivo de alerta y extrae información estructurada
    
    Args:
        filepath (str): Ruta del archivo de alerta
    
    Returns:
        dict: Diccionario con {timestamp, level, reason, content, application}
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Primera línea contiene: timestamp | LEVEL | reason
        if lines:
            header = lines[0]
            parts = header.split(' | ')
            
            if len(parts) >= 3:
                timestamp_str = parts[0].strip()
                level = parts[1].strip()
                reason = parts[2].strip()
                
                # Convertir timestamp ISO a datetime
                try:
                    timestamp_obj = datetime.fromisoformat(timestamp_str)
                    fecha_formatted = timestamp_obj.strftime("%Y-%m-%d %H:%M:%S")
                except:
                    fecha_formatted = timestamp_str
                
                # El contenido del mensaje es todo después de la línea separadora
                content_start = content.find('-' * 10)  # Buscar línea separadora
                message_content = ""
                if content_start != -1:
                    message_content = content[content_start + 81:].strip()  # 81 = 80 guiones + \n
                
                return {
                    'timestamp': timestamp_str,
                    'fecha': fecha_formatted,
                    'level': level,
                    'reason': reason,
                    'content': message_content,
                    'application': '[No disponible]'  # Placeholder
                }
        
        return None
    
    except Exception as e:
        print(f"Error parseando alerta {filepath}: {e}")
        return None


def get_alert_level_icon(level):
    """Retorna un icono emoji para el nivel de alerta"""
    level_lower = level.lower()
    
    if 'critico' in level_lower or 'critical' in level_lower:
        return '🔴'
    elif 'medio' in level_lower or 'medium' in level_lower:
        return '🟡'
    elif 'bajo' in level_lower or 'low' in level_lower:
        return '🟢'
    else:
        return '⚪'
