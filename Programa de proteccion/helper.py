#!/usr/bin/env python3
"""
Script helper para gestionar la aplicación integrada.
Uso: python helper.py [comando]
"""

import os
import sys
import subprocess
import platform

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def install_dependencies():
    """Instala las dependencias necesarias"""
    print_header("Instalando Dependencias")
    
    if os.path.exists('requirements.txt'):
        print("📦 Instalando desde requirements.txt...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=False)
        if result.returncode == 0:
            print("\n✓ Dependencias instaladas correctamente")
        else:
            print("\n✗ Error al instalar dependencias")
            sys.exit(1)
    else:
        print("✗ requirements.txt no encontrado")
        sys.exit(1)

def run_app():
    """Ejecuta la aplicación en modo desarrollo"""
    print_header("Ejecutando Aplicación")
    
    print("🚀 Iniciando aplicación...")
    if os.path.exists('main.py'):
        subprocess.run([sys.executable, 'main.py'])
    else:
        print("✗ main.py no encontrado")
        sys.exit(1)

def test_integration():
    """Ejecuta tests de integración"""
    print_header("Pruebas de Integración")
    
    test_file = os.path.join('scripts', 'test_integration.py')
    if os.path.exists(test_file):
        print("🧪 Ejecutando tests...")
        result = subprocess.run([sys.executable, test_file])
        sys.exit(result.returncode)
    else:
        print("✗ test_integration.py no encontrado en scripts/")
        print(f"  Buscaba en: {os.path.abspath(test_file)}")
        sys.exit(1)

def build_executable():
    """Compila el ejecutable con PyInstaller"""
    print_header("Compilando Ejecutable")
    
    if not os.path.exists('app_integrated.spec'):
        print("✗ app_integrated.spec no encontrado")
        sys.exit(1)
    
    print("📦 Compilando con PyInstaller...")
    print("⚠️  Esto puede tardar varios minutos...\n")
    
    result = subprocess.run([sys.executable, '-m', 'PyInstaller', 'app_integrated.spec'],
                          capture_output=False)
    
    if result.returncode == 0:
        print_header("✓ Compilación Exitosa")
        exe_path = os.path.join('dist', 'ProtectorApp.exe')
        if os.path.exists(exe_path):
            print(f"📍 Ejecutable creado en: {os.path.abspath(exe_path)}")
            print("\n¡Ahora puedes ejecutar la aplicación!")
        else:
            print("⚠️  Verificar en la carpeta dist/")
    else:
        print_header("✗ Error en Compilación")
        print("Revisa los logs arriba para más detalles")
        sys.exit(1)

def clean_build():
    """Limpia los artefactos de compilación"""
    print_header("Limpiando Artefactos")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🗑️  Eliminando {dir_name}/")
            import shutil
            shutil.rmtree(dir_name, ignore_errors=True)
    
    print("✓ Limpieza completada")

def show_help():
    """Muestra la ayuda"""
    print_header("Sistema de Protección para Menores - Helper")
    print("""
Comandos disponibles:

  python helper.py install      Instala las dependencias necesarias
  python helper.py run          Ejecuta la aplicación (desarrollo)
  python helper.py test         Ejecuta tests de integración
  python helper.py build        Compila ejecutable (PyInstaller)
  python helper.py clean        Limpia artefactos de compilación
  python helper.py help         Muestra esta ayuda

Flujo recomendado para primera ejecución:

  1. python helper.py install   (instalar dependencias)
  2. python helper.py test      (verificar que todo funciona)
  3. python helper.py run       (ejecutar en desarrollo)
  4. python helper.py build     (compilar ejecutable)

Problemas comunes:

  - Si PyInstaller no está instalado: pip install PyInstaller
  - Si módulos faltan: python helper.py install
  - Para más información: ver README.md
    """)

def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    commands = {
        'install': install_dependencies,
        'run': run_app,
        'test': test_integration,
        'build': build_executable,
        'clean': clean_build,
        'help': show_help,
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"✗ Comando desconocido: {command}")
        print("\nUsa: python helper.py help")
        sys.exit(1)

if __name__ == '__main__':
    main()
