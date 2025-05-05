import streamlit as st
import time

st.set_page_config(page_title="Meditación Guiada", layout="centered")
st.title("🧘‍♂️ Meditación Guiada en Silencio")
st.markdown(
    """
    Respira profundo. Cada etapa aparecerá automáticamente, reemplazando la anterior.  
    Deja que cada palabra te lleve hacia adentro.
    """
)

# Lista de pasos con texto y duración (en segundos)
pasos = [
    ("🌀 **Inicio**",
     "Bienvenido. Comencemos con una respiración consciente.\n\nInhala calma… Exhala luz… Repite esto tres veces con intención.",
     10),

    ("🌬️ **Silencio y presencia**",
     "Cierra los ojos suavemente y permite que tu cuerpo descanse.\n\nObserva cómo el aire entra y sale. Todo está bien en este momento.\n\nSi aparecen pensamientos, déjalos pasar como nubes.",
     20),

    ("🌱 **Deseo profundo**",
     "Lentamente, pregúntate:\n\n> ¿Qué deseo sinceramente experimentar?\n\nPiensa desde la abundancia. Siente lo que tu alma anhela con libertad y confianza.",
     15),

    ("🎬 **Visualización**",
     "Imagina una escena en la que ese deseo ya se ha cumplido.\n\n¿Qué ves? ¿Qué escuchas? ¿Cómo te sientes?\n\nHazlo real en tu mente, como si ya estuvieras viviendo ese momento con plenitud.",
     25),

    ("🔊 **Afirmación**",
     "*Repite mentalmente o en voz baja:*\n\n> Estoy en paz.\n> Estoy guiado.\n> Todo lo bueno que me pertenece por derecho divino viene a mí con armonía perfecta.",
     15),

    ("🙏 **Cierre**",
     "Siente una gratitud profunda, como si ya estuvieras viviendo la respuesta.\n\nQuédate unos instantes en esa certeza. Cuando estés listo, abre los ojos lentamente.",
     10)
]

# Crear un contenedor dinámico
contenedor = st.empty()

# Mostrar un paso a la vez
for titulo, contenido, duracion in pasos:
    with contenedor:
        st.markdown(f"### {titulo}")
        st.markdown(contenido)
    time.sleep(duracion)

# Mostrar mensaje final
contenedor.success("🌟 Has completado la meditación. Quédate unos segundos más en silencio si lo deseas.")
