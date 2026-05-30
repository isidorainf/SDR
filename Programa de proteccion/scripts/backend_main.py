from detector import cargar_palabras_riesgo, detectar_riesgo, normalizar_texto
from captura import capturar_y_extraer
from LLM import cadena_mitigacion
from analizador_afectivo import analizar_intencion
import time

def formatear_alertas(alertas):
    return "\n".join([f"- {tipo}: {palabra}" for tipo, palabra in alertas])

print("Cargando palabras de riesgo desde MongoDB Atlas...")
palabras_riesgo = cargar_palabras_riesgo()
print(f"Cargadas {sum(len(p) for p in palabras_riesgo.values())} palabras en {len(palabras_riesgo)} categorías")

ultimo_texto = ""

while True:
    texto_extraido = capturar_y_extraer()
    texto_limpio = normalizar_texto(texto_extraido)

    print("Texto capturado:", texto_extraido)
    print("Texto limpio:", texto_limpio)
    alertas = detectar_riesgo(texto_limpio, palabras_riesgo)
    
    intencion = analizar_intencion(texto_limpio)
    print(f"Intencion detectada: {intencion}")

    if alertas and texto_limpio != ultimo_texto and len(texto_limpio) > 10:
        ultimo_texto = texto_limpio

        print(f"[{time.ctime()}] Riesgo detectado:")
        print(formatear_alertas(alertas) if alertas else "Sin palabras clave, pero toxicidad alta")

        try:
            respuesta = cadena_mitigacion.invoke({
                "texto": texto_limpio,
                "alertas": formatear_alertas(alertas) if alertas else "Ninguna",
                "intencion": intencion
            })

            respuesta = str(respuesta).strip()
            with open('Mitigaciones.txt', 'w', encoding='utf-8') as archivo:
                archivo.write(respuesta)
            print("Mitigación:", respuesta)

        except Exception as e:
            print("Error en LLM:", e)

    else:
        print(f"[{time.ctime()}] Sin riesgo o repetido")

    time.sleep(5)
