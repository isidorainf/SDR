"""
Configuración de la aplicación integrada.
Centraliza paths, constantes y configuración global.
"""
import os
import sys

# Directorios
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, 'scripts')

# Asegurar que los directorios existan en el path
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

# Configuración de la aplicación
APP_NAME = "Protección para Menores"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema de Detección y Recomendación de Contenido Peligroso"

# Configuración de UI
UI_STYLE = "Fusion"
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT_WIDTH = 900
WINDOW_DEFAULT_HEIGHT = 700

# Configuración de monitoreo
MONITOR_INDEX = 1  # Monitor principal (0 es la información general)
CAPTURE_INTERVAL = 5  # segundos entre capturas
OCR_LANGUAGES = ['es', 'en']

# Configuración de MongoDB
MONGO_URI = "mongodb+srv://admin:notoxicity67@cluster0.k7uvdoa.mongodb.net/?appName=Cluster0"
MONGO_DB = "palabras_sensibles"
MONGO_COLLECTION = "palabras_riesgo"

# Configuración del LLM
LLM_MODEL = "Qwen/Qwen2.5-3B-Instruct"
LLM_MAX_TOKENS = 256
LLM_TEMPERATURE = 0.01
LLM_TOP_P = 0.9

# Configuración de detección de toxicidad
TOXICITY_MODEL = "multilingual"
THREAT_THRESHOLD = 0.5
INSULT_THRESHOLD = 0.6
HATE_THRESHOLD = 0.6
OBSCENE_THRESHOLD = 0.6

# Rutas de archivos
PALABRAS_RIESGO_PATH = os.path.join(SCRIPTS_DIR, 'palabras_riesgo.json')

# Rutas locales en la carpeta del proyecto (no en Desktop)
LOCAL_DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
PROTECTION_FOLDER = os.path.join(LOCAL_DATA_DIR, 'Protección')
CAPTURAS_PATH = os.path.join(LOCAL_DATA_DIR, 'capturas')

# Ruta de almacenamiento alternativa (si se necesita)
STORAGE_PATH = os.path.expanduser('~/.protector_app')

# Logging
DEBUG = True
LOG_LEVEL = "DEBUG" if DEBUG else "INFO"

# Validar rutas
def validate_paths():
    """Valida que las rutas necesarias existan"""
    missing = []
    
    if not os.path.exists(SCRIPTS_DIR):
        missing.append(f"scripts: {SCRIPTS_DIR}")
    
    if missing:
        print("⚠️  Rutas no encontradas:")
        for path in missing:
            print(f"  - {path}")
        return False
    
    return True

# Crear directorios de almacenamiento si no existen
os.makedirs(LOCAL_DATA_DIR, exist_ok=True)
os.makedirs(PROTECTION_FOLDER, exist_ok=True)
os.makedirs(CAPTURAS_PATH, exist_ok=True)
os.makedirs(STORAGE_PATH, exist_ok=True)

# Debug info
if DEBUG:
    print("=" * 60)
    print("CONFIGURACIÓN DE APLICACIÓN")
    print("=" * 60)
    print(f"Aplicación: {APP_NAME} v{APP_VERSION}")
    print(f"Raíz del proyecto: {PROJECT_ROOT}")
    print(f"Scripts: {SCRIPTS_DIR}")
    print(f"Carpeta de datos: {LOCAL_DATA_DIR}")
    print(f"Contraseña: {PROTECTION_FOLDER}")
    print(f"Capturas: {CAPTURAS_PATH}")
    print("=" * 60)
