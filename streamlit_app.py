import streamlit as st
import time

st.set_page_config(page_title="Meditación Guiada", layout="centered")
st.title("🧘‍♂️ Meditación Guiada en Silencio")
st.markdown("Respira profundo. Deja que cada palabra te acompañe suavemente. El texto se mostrará paso a paso.")

# Pasos de la meditación con duración optimizada
pasos = [
    ("🌀 **Inicio**", 
     "Bienvenido. Comencemos con una respiración profunda.\n\nInhala calma… Exhala tensión… Repite esto 3 veces en silencio.", 
     10),

    ("🌬️ **Silencio y presencia**", 
     "Cierra los ojos un momento y siente tu cuerpo. Solo observa cómo entra y sale el aire por tu nariz.\n\nSi aparecen pensamientos, déjalos pasar como nubes.", 
     20),

    ("🌱 **Deseo profundo**", 
     "Lentamente, pregúntate:\n\n> ¿Qué deseo sinceramente experimentar?\n\nNo pienses desde la escasez. Siente lo que tu alma anhela.", 
     15),

    ("🎬 **Visualización**", 
     "Imagina una escena en la que ese deseo ya se ha cumplido.\n\n¿Qué ves? ¿Qué escuchas? ¿Cómo te sientes?\n\nHazlo real en tu mente, como una película luminosa.", 
     25),

    ("🔊 **Afirmación**", 
     "*Repite mentalmente o en voz baja:*\n\n> Estoy en paz.\n> Estoy guiado.\n> Lo que es mío por derecho divino viene a mí ahora.", 
     15),

    ("🙏 **Cierre**", 
     "Siente gratitud, como si todo ya estuviera hecho.\n\n> Gracias. Confío plenamente.\n\nCuando estés listo, abre los ojos lentamente.", 
     10)
]

# Mostrar cada etapa automáticamente con pausas
for titulo, contenido, duracion in pasos:
    st.markdown(f"### {titulo}")
    st.markdown(contenido)
    time.sleep(duracion)
    st.empty()

st.success("🌟 Has completado la meditación. Quédate unos segundos más en silencio si lo deseas.")
