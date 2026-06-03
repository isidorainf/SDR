INSTRUCCIONES DE INSTALACIÓN Y EJECUCIÓN

1. Descargar y extraer la carpeta del proyecto.

2. Abrir la carpeta "Programa de Proteccion" en Visual Studio Code.

3. Crear y activar un entorno virtual para Python:
   - Windows: python -m venv .venv y luego .\.venv\Scripts\activate
   - Se selecciona la versión Python 3.14 --> Se selecciona el archivo de 'requirements.txt

4. Instalar todas las dependencias usando el script de ayuda:
   - python helper.py install --> Solo para primera vez de ejecución 
   - pip install PyInstaller
   - pip install PyQt5

5. Ejecutar los siguientes comandos siempre que se abrá nuevamente el programa
   - python helper.py test
   - python helper.py run    
   - python helper.py build

6. Ejecutar archivo 'launch.py' para abrir el sistema
   - Clave asignada: 123456