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
        img_np = np.array(screenshot)

        os.makedirs(CAPTURAS_PATH, exist_ok=True)
        nombre_archivo = datetime.now().strftime("captura_%Y-%m-%d_%H-%M-%S.png")
        ruta_completa = os.path.join(CAPTURAS_PATH, nombre_archivo)
        cv2.imwrite(ruta_completa, img_np)
        
        print(f"Captura guardada en: {ruta_completa}")
        resultado = reader.readtext(img_np, detail=0)
        texto = " ".join(resultado)

        return texto

