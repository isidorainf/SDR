#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verificador interactivo de importaciones
Muestra un resumen visual de todas las importaciones
"""

import sys
import os
from pathlib import Path

# Configurar el path correctamente
project_root = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(project_root, 'scripts')
sys.path.insert(0, project_root)
sys.path.insert(0, scripts_dir)

class Colors:
    """Códigos de color ANSI para terminal"""
    RESET = '\033[0m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    
def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 80}{Colors.RESET}\n")

def print_section(text):
    print(f"{Colors.BOLD}{Colors.BLUE}→ {text}{Colors.RESET}")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.RESET}")

def check_file(name, path):
    """Verifica si un archivo existe"""
    exists = os.path.exists(path)
    if exists:
        print_success(f"{name}: {os.path.relpath(path, project_root)}")
    else:
        print_error(f"{name}: {os.path.relpath(path, project_root)}")
    return exists

def test_import(module_name, import_stmt, description=""):
    """Intenta realizar una importación y reporta el resultado"""
    try:
        exec(import_stmt)
        print_success(f"{module_name}: {description or import_stmt}")
        return True
    except Exception as e:
        print_error(f"{module_name}: {str(e)}")
        return False

def main():
    print_header("VERIFICADOR DE IMPORTACIONES - SISTEMA DE PROTECCIÓN PARA MENORES")
    
    # Información del entorno
    print_info(f"Directorio de trabajo: {os.getcwd()}")
    print_info(f"Raíz del proyecto: {project_root}")
    print_info(f"Versión de Python: {sys.version.split()[0]}")
    
    # ========================================================================
    # 1. VERIFICAR ARCHIVOS
    # ========================================================================
    print_section("PASO 1: Verificando archivos necesarios")
    
    files = [
        ("config.py", os.path.join(project_root, 'config.py')),
        ("timestamp_manager.py", os.path.join(scripts_dir, 'timestamp_manager.py')),
        ("chat_widget.py", os.path.join(scripts_dir, 'chat_widget.py')),
        ("worker_thread.py", os.path.join(scripts_dir, 'worker_thread.py')),
        ("dashboard_window.py", os.path.join(scripts_dir, 'dashboard_window.py')),
    ]
    
    all_files_exist = all(check_file(name, path) for name, path in files)
    
    if not all_files_exist:
        print_error("Faltan archivos necesarios")
        return False
    
    # ========================================================================
    # 2. VERIFICAR DEPENDENCIAS
    # ========================================================================
    print_section("PASO 2: Verificando dependencias principales")
    
    stdlib_modules = ['os', 'sys', 'datetime', 'time', 'socket']
    for mod in stdlib_modules:
        try:
            __import__(mod)
            print_success(f"Librería estándar: {mod}")
        except ImportError:
            print_error(f"Librería estándar: {mod}")
    
    # Verificar PySide6 (con manejo de error gracioso)
    try:
        from PySide6.QtCore import Qt
        from PySide6.QtWidgets import QWidget
        from PySide6.QtGui import QFont
        print_success("PySide6: Todas las clases necesarias disponibles")
    except ImportError as e:
        print_warning(f"PySide6: {str(e)}")
        print_warning("PySide6 es necesario para la interfaz gráfica. Instalar con: pip install PySide6>=6.4.0")
    
    # ========================================================================
    # 3. IMPORTAR MÓDULOS
    # ========================================================================
    print_section("PASO 3: Importando módulos locales")
    
    success_count = 0
    total_imports = 5
    
    # config
    if test_import("config.py", "import config", "Configuración central"):
        success_count += 1
    
    # timestamp_manager
    if test_import("timestamp_manager", 
                   "from timestamp_manager import save_last_analysis_time, get_minutes_since_last_analysis, format_minutes_to_readable",
                   "Funciones de timestamps (3)"):
        success_count += 1
    
    # chat_widget
    if test_import("chat_widget", 
                   "from chat_widget import ChatWidget",
                   "Widget de chat para reportes"):
        success_count += 1
    
    # worker_thread
    if test_import("worker_thread", 
                   "from worker_thread import MonitoringWorker",
                   "Worker thread para monitoreo"):
        success_count += 1
    
    # dashboard_window
    if test_import("dashboard_window", 
                   "from dashboard_window import DashboardWindow",
                   "Ventana principal del dashboard"):
        success_count += 1
    
    # ========================================================================
    # 4. RESUMEN FINAL
    # ========================================================================
    print_header(f"RESUMEN FINAL: {success_count}/{total_imports} importaciones exitosas")
    
    if success_count == total_imports:
        print_success("TODAS LAS IMPORTACIONES FUNCIONAN CORRECTAMENTE")
        
        print(f"\n{Colors.BOLD}Importaciones verificadas:{Colors.RESET}")
        print_success("save_last_analysis_time() - timestamp_manager.py")
        print_success("get_minutes_since_last_analysis() - timestamp_manager.py")
        print_success("format_minutes_to_readable() - timestamp_manager.py")
        print_success("ChatWidget - chat_widget.py")
        print_success("MonitoringWorker - worker_thread.py")
        print_success("DashboardWindow - dashboard_window.py")
        
        print_success(f"\n✨ El sistema está listo para usar")
        return True
    else:
        print_error(f"Se encontraron {total_imports - success_count} problema(s)")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
