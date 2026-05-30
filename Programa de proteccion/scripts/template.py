from langchain_core.prompts import PromptTemplate

template_mitigacion = PromptTemplate(
    input_variables=["texto", "alertas", "intencion"],
    template="""
Eres un experto en prevenir violencia digital en menores.

Tu tarea es clasificar el nivel de riesgo y generar UNA recomendación para tutores.

Sigue estrictamente el siguiente formato (EJEMPLOS).

---

Ejemplo 1:
Texto: "hola eres muy tonto"
Alertas: intelectual: tonto
Intencion: La intención de este mensaje es leve.


Respuesta:
Nivel: BAJO
Motivo: insulto leve sin amenaza ni intención de daño grave, respaldado por bajo puntaje de toxicidad.
Recomendación: supervisar conversación y educar sobre lenguaje respetuoso.

---

Ejemplo 2:
Texto: "nadie te quiere mejor muérete"
Alertas: acoso: muérete
Intencion:  La intención de este mensaje es negativa porque tiene un tono agresivo o negativo.

Respuesta:
Nivel: ALTO
Motivo: lenguaje de auto-daño y acoso directo con alta carga emocional, respaldado por alto puntaje de toxicidad.
Recomendación: intervenir inmediatamente y notificar al tutor.

---

Ejemplo 3:
Texto: "eres feo y nadie te habla"
Alertas: apariencia_fisica: feo
Intencion:  La intención de este mensaje es negativa porque tiene un tono agresivo o negativo.

Respuesta:
Nivel: MEDIO
Motivo: contenido repetido de humillación social sin amenaza directa, respaldado por toxicidad moderada.
Recomendación: monitorear interacción y reforzar apoyo emocional.

---

Texto del usuario: {texto}

Palabras clave detectadas: {alertas}

Un sistema de inteligencia emocional analizó el mensaje y concluyó: {intencion}

---

Genera UNA respuesta de mitigación y prevencion ante el riesgo.

Respuesta: (Con formato de ejemplos)

""".strip()
)
