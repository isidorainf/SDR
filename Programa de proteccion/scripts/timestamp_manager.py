"""
Gestor de timestamps para registrar el último análisis.
Calcula el tiempo transcurrido desde la última ejecución.
"""
import os
from datetime import datetime
from config import LOCAL_DATA_DIR


LAST_ANALYSIS_FILE = os.path.join(LOCAL_DATA_DIR, 'last_analysis.txt')


def save_last_analysis_time():
    """Guarda la hora actual del sistema en el archivo de análisis"""
    try:
        os.makedirs(LOCAL_DATA_DIR, exist_ok=True)
        with open(LAST_ANALYSIS_FILE, 'w') as f:
            f.write(datetime.now().isoformat())
    except Exception as e:
        print(f"Error guardando timestamp: {e}")


def get_minutes_since_last_analysis():
    """
    Calcula los minutos que han pasado desde el último análisis.
    Si el archivo no existe, retorna 0.
    """
    if not os.path.exists(LAST_ANALYSIS_FILE):
        return 0
    
    try:
        with open(LAST_ANALYSIS_FILE, 'r') as f:
            last_time_str = f.read().strip()
        
        if not last_time_str:
            return 0
        
        last_time = datetime.fromisoformat(last_time_str)
        current_time = datetime.now()
        
        time_diff = current_time - last_time
        minutes_elapsed = int(time_diff.total_seconds() / 60)
        
        return minutes_elapsed
    except Exception as e:
        print(f"Error leyendo timestamp: {e}")
        return 0


def format_minutes_to_readable(minutes):
    """
    Convierte minutos a formato legible.
    Ej: 125 minutos -> "2h 5m"
    """
    if minutes == 0:
        return "Justo ahora"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if hours == 0:
        return f"{remaining_minutes}m"
    elif remaining_minutes == 0:
        return f"{hours}h"
    else:
        return f"{hours}h {remaining_minutes}m"
