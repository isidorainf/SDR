INSTRUCCIONES DE INSTALACIÓN Y EJECUCIÓN

1. Descargar y extraer la carpeta del proyecto.
2. Abrir la carpeta "Programa de Proteccion" en Visual Studio Code.
3. Crear y activar un entorno virtual para Python:
   - Windows: python -m venv .venv y luego .\.venv\Scripts\activate
4. Instalar todas las dependencias usando el script de ayuda:
   - python helper.py install
5. (OPCIONAL) Si tienes una tarjeta gráfica NVIDIA, instala la versión acelerada de PyTorch para mejorar el rendimiento del LLM:
   - pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
6. Ejecutar pruebas de integridad:
   - python helper.py test
7. Iniciar la aplicación:
   - python helper.py run

8. Si usarás la aplicación en otro momento solo debes ejecutar:
   - python helper.py run       
   - python helper.py build
   - Ejecutar archivo launch.py