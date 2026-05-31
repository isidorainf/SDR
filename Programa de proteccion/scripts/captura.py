import mss
import numpy as np
import easyocr
import cv2
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import CAPTURAS_PATH

reader = easyocr.Reader(['es', 'en'])

def capturar_y_extraer():
    with mss.mss() as sct:
        screenshot = sct.grab(sct.monitors[1])
        
        # 1. Convertir a numpy array y quitar canal Alfa
        img_np = np.array(screenshot)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_BGRA2BGR)

        # 2. Asegurar ruta absoluta
        ruta_absoluta = os.path.abspath(CAPTURAS_PATH)
        os.makedirs(ruta_absoluta, exist_ok=True)
        
        nombre_archivo = datetime.now().strftime("captura_%Y-%m-%d_%H-%M-%S.png")
        ruta_completa = os.path.join(ruta_absoluta, nombre_archivo)
        
        # 3. SOLUCIÓN A TILDES: Usar imencode y numpy.tofile en lugar de cv2.imwrite
        exito, buffer = cv2.imencode('.png', img_bgr)
        
        if exito:
            buffer.tofile(ruta_completa)
            print(f"✅ Captura guardada con éxito en: {ruta_completa}")
        else:
            print(f"❌ ERROR: No se pudo codificar la imagen en memoria.")
        
        # 4. Extraer el texto usando la imagen original
        resultado = reader.readtext(img_np, detail=0)
        texto = " ".join(resultado)

        return texto