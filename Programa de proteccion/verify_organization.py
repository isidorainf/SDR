#!/usr/bin/env python3
"""
Script de verificación de la reorganización.
Comprueba que todos los imports funcionen correctamente.
"""

import os
import sys

project_root = r'c:\Users\elcre\Desktop\Intentando cosas'
scripts_dir = os.path.join(project_root, 'scripts')

print("=" * 60)
print("VERIFICACIÓN DE REORGANIZACIÓN")
print("=" * 60)

# Agregar scripts al path
sys.path.insert(0, scripts_dir)
os.chdir(project_root)

# Verificar estructura
print("\n1. Verificando estructura de carpetas...")
required_files = {
    'main.py': 'Punto de entrada',
    'config.py': 'Configuración',
    'helper.py': 'Helper',
    'scripts': 'Carpeta de scripts',
}

for file_name, description in required_files.items():
    path = os.path.join(project_root, file_name)
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"  {status} {file_name:20s} ({description})")

# Verificar archivos en scripts
print("\n2. Verificando archivos en scripts/...")
required_in_scripts = [
    'detector.py',
    'captura.py',
    'LLM.py',
    'analizador_afectivo.py',
    'template.py',
    'login_window.py',
    'main_app.py',
    'palabras_riesgo.json',
    'backend_main.py',
]

for file_name in required_in_scripts:
    path = os.path.join(scripts_dir, file_name)
    exists = os.path.exists(path)
    status = "✓" if exists else "✗"
    print(f"  {status} {file_name}")

# Intentar importar módulos clave
print("\n3. Probando imports desde scripts/...")
try:
    import template
    print("  ✓ template")
except Exception as e:
    print(f"  ✗ template: {e}")

try:
    import detector
    print("  ✓ detector")
except Exception as e:
    print(f"  ✗ detector: {e}")

# Verificar que carpeta vieja no existe
print("\n4. Verificando limpieza...")
old_dir = os.path.join(project_root, 'Sistema-de-detecci-n-y-recomendaci-n-main')
if os.path.exists(old_dir):
    print(f"  ⚠️  Carpeta vieja aún existe: {old_dir}")
    print("     (Ejecuta _cleanup_run.py para limpiar)")
else:
    print("  ✓ Carpeta vieja eliminada")

print("\n" + "=" * 60)
print("VERIFICACIÓN COMPLETADA")
print("=" * 60)
print("\nUsa: python main.py para ejecutar la aplicación")
