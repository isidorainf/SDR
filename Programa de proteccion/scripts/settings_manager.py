"""
Gestor de configuración persistente.
Guarda y carga las preferencias del usuario en un archivo JSON.
"""
import os
import json

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import LOCAL_DATA_DIR

SETTINGS_FILE = os.path.join(LOCAL_DATA_DIR, 'settings.json')

# Valores por defecto
DEFAULT_SETTINGS = {
    "auto_start": False,
    "capture_interval": 5,
    "custom_words": []
}


def load_settings():
    """Carga la configuración desde el archivo JSON. Si no existe, retorna los valores por defecto."""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            settings = json.load(f)

        # Asegurar que todas las claves existan
        for key, value in DEFAULT_SETTINGS.items():
            if key not in settings:
                settings[key] = value

        return settings
    except Exception as e:
        print(f"Error cargando configuración: {e}")
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    """Guarda la configuración en el archivo JSON."""
    try:
        os.makedirs(LOCAL_DATA_DIR, exist_ok=True)
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error guardando configuración: {e}")


def get_setting(key):
    """Obtiene un valor específico de la configuración."""
    settings = load_settings()
    return settings.get(key, DEFAULT_SETTINGS.get(key))


def set_setting(key, value):
    """Establece un valor específico en la configuración."""
    settings = load_settings()
    settings[key] = value
    save_settings(settings)
