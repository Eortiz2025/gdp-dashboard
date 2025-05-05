iimport streamlit as st
import time

st.set_page_config(page_title="Meditación Guiada", layout="centered")
st.title("🧘‍♂️ Meditación Guiada en Silencio")

# Definir los pasos y subfrases con pausas individuales
pasos = [
    ("🌀 **Inicio**", [
        "Bienvenido.",
        "Comencemos con una respiración consciente.",
        "Inhala calma…",
        "Exhala luz…",
        "Repite esto tres veces con intención."
    ], 4),

    ("🌬️ **Silencio y presencia**", [
        "Cierra los ojos suavemente.",
        "Permite que tu cuerpo descanse.",
        "Observa cómo el aire entra y sale.",
        "Todo está bien en este momento.",
        "Si aparecen pensamientos, déjalos pasar como nubes."
    ], 5),

    ("🌱 **Deseo profundo**", [
        "Lentamente, pregúntate:",
        "¿Qué deseo sinceramente experimentar?",
        "Piensa desde la abundancia.",
        "Siente lo que tu alma anhela con libertad y confianza."
    ], 5),

    ("🎬 **Visualización**", [
        "Imagina una escena en la que ese deseo ya se ha cumplido.",
        "¿Qué ves?",
        "¿Qué escuchas?",
        "¿Cómo te sientes?",
        "Hazlo real en tu mente, como si ya estuvieras viviendo ese momento con plenitud."
    ], 6),

    ("🔊 **Afirmación**", [
        "Repite mentalmente o en voz baja:",
        "Estoy en paz.",
        "Estoy guiado.",
        "Todo lo bueno que me pertenece por derecho divino viene a mí con armonía perfecta."
    ], 5),

    ("🙏 **Cierre**", [
        "Siente una gratitud profunda, como si ya estuvieras viviendo la respuesta.",
        "Quédate unos instantes en esa certeza.",
        "Cuando estés listo, abre los ojos lentamente."
    ], 5)
]

# Crear un contenedor dinámico
contenedor = st.empty()

# Mostrar cada paso uno por uno, línea por línea
for titulo, lineas, pausa in pasos:
    for i, texto in enumerate(lineas):
        with contenedor:
            st.markdown(f"### {titulo}")
            st.markdown('\n\n'.join(lineas[:i+1]))
        time.sleep(pausa)

# Mensaje final
contenedor.success("🌟 Has completado la meditación. Quédate unos segundos más en silencio si lo deseas.")
