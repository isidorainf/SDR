#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que todas las importaciones funcionan correctamente
"""

import sys
import os

# Configurar el path correctamente
project_root = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(project_root, 'scripts')
sys.path.insert(0, project_root)
sys.path.insert(0, scripts_dir)

print("=" * 70)
print("VERIFICACIÓN DE IMPORTACIONES")
print("=" * 70)
print(f"\nDirectorio actual: {os.getcwd()}")
print(f"Project root: {project_root}")
print(f"Scripts dir: {scripts_dir}")
print(f"Python path: {sys.path[:3]}")

# Verificar que existen los archivos necesarios
print("\n--- Verificando archivos necesarios ---")
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
    status = "✓" if exists else "✗"
    print(f"{status} {name}: {path}")
    if not exists:
        all_files_exist = False

if not all_files_exist:
    print("\n✗ Faltan archivos necesarios")
    sys.exit(1)

# Test 1: Importar config
print("\n--- Prueba 1/5: Importando config ---")
try:
    import config
    print("✓ Éxito: config importado correctamente")
except Exception as e:
    print(f"✗ Error al importar config: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Importar funciones de timestamp_manager
print("\n--- Prueba 2/5: Importando de timestamp_manager ---")
try:
    from timestamp_manager import save_last_analysis_time, get_minutes_since_last_analysis, format_minutes_to_readable
    print("✓ Éxito: timestamp_manager importado correctamente")
    print(f"  - save_last_analysis_time: {callable(save_last_analysis_time)}")
    print(f"  - get_minutes_since_last_analysis: {callable(get_minutes_since_last_analysis)}")
    print(f"  - format_minutes_to_readable: {callable(format_minutes_to_readable)}")
except Exception as e:
    print(f"✗ Error al importar timestamp_manager: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Importar ChatWidget
print("\n--- Prueba 3/5: Importando ChatWidget de chat_widget ---")
try:
    from chat_widget import ChatWidget
    print("✓ Éxito: ChatWidget importado correctamente")
    print(f"  - ChatWidget es una clase: {isinstance(ChatWidget, type)}")
except Exception as e:
    print(f"✗ Error al importar ChatWidget: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Importar MonitoringWorker
print("\n--- Prueba 4/5: Importando MonitoringWorker de worker_thread ---")
try:
    from worker_thread import MonitoringWorker
    print("✓ Éxito: MonitoringWorker importado correctamente")
    print(f"  - MonitoringWorker es una clase: {isinstance(MonitoringWorker, type)}")
except Exception as e:
    print(f"✗ Error al importar MonitoringWorker: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 5: Verificar que dashboard_window.py importa correctamente
print("\n--- Prueba 5/5: Verificando importaciones en dashboard_window ---")
try:
    from dashboard_window import DashboardWindow
    print("✓ Éxito: DashboardWindow importado correctamente")
    print(f"  - DashboardWindow es una clase: {isinstance(DashboardWindow, type)}")
except Exception as e:
    print(f"✗ Error al importar DashboardWindow: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✓ TODAS LAS IMPORTACIONES FUNCIONAN CORRECTAMENTE")
print("=" * 70)
print("\nResumen:")
print("  ✓ config.py")
print("  ✓ timestamp_manager.py (save_last_analysis_time)")
print("  ✓ timestamp_manager.py (get_minutes_since_last_analysis)")
print("  ✓ timestamp_manager.py (format_minutes_to_readable)")
print("  ✓ chat_widget.py (ChatWidget)")
print("  ✓ worker_thread.py (MonitoringWorker)")
print("  ✓ dashboard_window.py (DashboardWindow)")
print("=" * 70)
