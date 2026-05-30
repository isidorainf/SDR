# -*- mode: python ; coding: utf-8 -*-
"""
Especificación de PyInstaller para la aplicación integrada.
Uso: pyinstaller app_integrated.spec
"""

import os
import sys

block_cipher = None

# Ruta del proyecto (CORREGIDO: Se eliminó os.path.dirname para no retroceder de carpeta)
project_dir = os.path.abspath(SPECPATH)
scripts_dir = os.path.join(project_dir, 'scripts')
backend_dir = os.path.join(project_dir, 'Sistema-de-detecci-n-y-recomendaci-n-main')

# Datos a incluir (archivos que no son Python)
datas = [
    (os.path.join(scripts_dir, 'palabras_riesgo.json'), '.'),  # CORREGIDO: Ahora busca en scripts_dir
]

# Importaciones ocultas necesarias
hiddenimports = [
    'PySide6',
    'easyocr',
    'mss',
    'cv2',
    'torch',
    'transformers',
    'langchain',
    'langchain_community',
    'langchain_huggingface',
    'pymongo',
    'detoxify',
]

a = Analysis(
    [os.path.join(project_dir, 'main.py')],
    pathex=[scripts_dir, backend_dir, project_dir],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ProtectorApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)