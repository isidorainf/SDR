#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar importaciones sin requerir todas las dependencias
"""

import sys
import os

# Configurar el path correctamente
project_root = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(project_root, 'scripts')
sys.path.insert(0, project_root)
sys.path.insert(0, scripts_dir)

print("=" * 80)
print("DIAGNÓSTICO DE IMPORTACIONES - SISTEMA DE PROTECCIÓN PARA MENORES")
print("=" * 80)

print(f"\n📁 INFORMACIÓN DEL ENTORNO:")
print(f"  Directorio de trabajo: {os.getcwd()}")
print(f"  Raíz del proyecto: {project_root}")
print(f"  Directorio scripts: {scripts_dir}")
print(f"  Versión de Python: {sys.version.split()[0]}")

# ============================================================================
# 1. VERIFICAR ARCHIVOS
# ============================================================================
print("\n" + "=" * 80)
print("1️⃣ VERIFICACIÓN DE ARCHIVOS NECESARIOS")
print("=" * 80)

files_to_check = [
    ('config.py', os.path.join(project_root, 'config.py')),
    ('timestamp_manager.py', os.path.join(scripts_dir, 'timestamp_manager.py')),
    ('chat_widget.py', os.path.join(scripts_dir, 'chat_widget.py')),
    ('worker_thread.py', os.path.join(scripts_dir, 'worker_thread.py')),
    ('dashboard_window.py', os.path.join(scripts_dir, 'dashboard_window.py')),
]

all_files_exist = True
for name, path in files_to_check:
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    rel_path = os.path.relpath(path, project_root)
    print(f"{status} {name:<30} {rel_path}")
    if not exists:
        all_files_exist = False

if not all_files_exist:
    print("\n❌ FALTA ARCHIVOS NECESARIOS")
    sys.exit(1)

# ============================================================================
# 2. VERIFICAR DEPENDENCIAS
# ============================================================================
print("\n" + "=" * 80)
print("2️⃣ VERIFICACIÓN DE DEPENDENCIAS PRINCIPALES")
print("=" * 80)

dependencies = [
    'os',
    'sys',
    'datetime',
    'json',
    'PySide6',
    'PySide6.QtWidgets',
    'PySide6.QtCore',
    'PySide6.QtGui',
]

missing_deps = []
for dep in dependencies:
    try:
        parts = dep.split('.')
        module = __import__(dep)
        print(f"✅ {dep:<40}")
    except ImportError as e:
        print(f"❌ {dep:<40} Error: {str(e)}")
        missing_deps.append(dep)

# ============================================================================
# 3. IMPORTAR CONFIG
# ============================================================================
print("\n" + "=" * 80)
print("3️⃣ IMPORTACIÓN: config.py")
print("=" * 80)

try:
    import config
    print(f"✅ config importado correctamente")
    print(f"   - PROJECT_ROOT: {config.PROJECT_ROOT}")
    print(f"   - SCRIPTS_DIR: {config.SCRIPTS_DIR}")
    print(f"   - APP_NAME: {config.APP_NAME}")
    print(f"   - LOCAL_DATA_DIR: {config.LOCAL_DATA_DIR}")
except Exception as e:
    print(f"❌ Error al importar config: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 4. IMPORTAR TIMESTAMP_MANAGER
# ============================================================================
print("\n" + "=" * 80)
print("4️⃣ IMPORTACIÓN: timestamp_manager.py")
print("=" * 80)

try:
    from timestamp_manager import (
        save_last_analysis_time, 
        get_minutes_since_last_analysis, 
        format_minutes_to_readable
    )
    print(f"✅ timestamp_manager importado correctamente")
    print(f"   - save_last_analysis_time: {type(save_last_analysis_time).__name__}")
    print(f"   - get_minutes_since_last_analysis: {type(get_minutes_since_last_analysis).__name__}")
    print(f"   - format_minutes_to_readable: {type(format_minutes_to_readable).__name__}")
    
    # Probar funciones
    print(f"\n   Prueba de funciones:")
    test_minutes = format_minutes_to_readable(125)
    print(f"   - format_minutes_to_readable(125) = '{test_minutes}'")
    
except Exception as e:
    print(f"❌ Error al importar timestamp_manager: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 5. IMPORTAR CHAT_WIDGET
# ============================================================================
print("\n" + "=" * 80)
print("5️⃣ IMPORTACIÓN: chat_widget.py")
print("=" * 80)

try:
    from chat_widget import ChatWidget
    print(f"✅ ChatWidget importado correctamente")
    print(f"   - ChatWidget: {type(ChatWidget).__name__}")
    print(f"   - Es una clase: {isinstance(ChatWidget, type)}")
    print(f"   - Métodos disponibles: {[m for m in dir(ChatWidget) if not m.startswith('_')][:5]}...")
    
except Exception as e:
    print(f"❌ Error al importar ChatWidget: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 6. IMPORTAR WORKER_THREAD
# ============================================================================
print("\n" + "=" * 80)
print("6️⃣ IMPORTACIÓN: worker_thread.py")
print("=" * 80)

try:
    from worker_thread import MonitoringWorker
    print(f"✅ MonitoringWorker importado correctamente")
    print(f"   - MonitoringWorker: {type(MonitoringWorker).__name__}")
    print(f"   - Es una clase: {isinstance(MonitoringWorker, type)}")
    print(f"   - Es un QThread: {hasattr(MonitoringWorker, 'run')}")
    
except Exception as e:
    print(f"❌ Error al importar MonitoringWorker: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# 7. IMPORTAR DASHBOARD_WINDOW
# ============================================================================
print("\n" + "=" * 80)
print("7️⃣ IMPORTACIÓN: dashboard_window.py")
print("=" * 80)

try:
    from dashboard_window import DashboardWindow
    print(f"✅ DashboardWindow importado correctamente")
    print(f"   - DashboardWindow: {type(DashboardWindow).__name__}")
    print(f"   - Es una clase: {isinstance(DashboardWindow, type)}")
    print(f"   - Dependencias: ChatWidget, MonitoringWorker, timestamp_manager")
    
except Exception as e:
    print(f"❌ Error al importar DashboardWindow: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "=" * 80)
print("✅ VERIFICACIÓN COMPLETADA - TODAS LAS IMPORTACIONES FUNCIONAN")
print("=" * 80)

print("\n📋 RESUMEN DE IMPORTS VERIFICADOS:")
print("  ✅ config.py")
print("  ✅ timestamp_manager.py")
print("     └─ save_last_analysis_time()")
print("     └─ get_minutes_since_last_analysis()")
print("     └─ format_minutes_to_readable()")
print("  ✅ chat_widget.py")
print("     └─ ChatWidget (class)")
print("  ✅ worker_thread.py")
print("     └─ MonitoringWorker (class)")
print("  ✅ dashboard_window.py")
print("     └─ DashboardWindow (class)")

if missing_deps:
    print(f"\n⚠️  ADVERTENCIA: {len(missing_deps)} dependencia(s) no disponible(s):")
    for dep in missing_deps:
        print(f"   - {dep}")
else:
    print("\n🎉 ¡Todas las dependencias disponibles!")

print("\n" + "=" * 80)
