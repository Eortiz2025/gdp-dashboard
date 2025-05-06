import streamlit as st
import time
import os
from gtts import gTTS
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="Sesión de Reprogramación - Murphy & Shinn", layout="centered")
st.markdown("""
<style>
    .title {
        font-size: 2.6em;
        font-weight: bold;
        color: #4B8BBE;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.2em;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 5px;
    }
    .reflection {
        font-size: 1em;
        font-style: italic;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .step {
        font-size: 1.2em;
        line-height: 1.6em;
    }
</style>
<div class='title'>🌟 Sesión Transformadora de Reprogramación</div>
<div class='subtitle'>Basada en Joseph Murphy y Florence Scovel Shinn</div>
<div class='reflection'>Este es un momento sagrado. Dejo que la Verdad me transforme.</div>
""", unsafe_allow_html=True)

# Estructura de la sesión
sesion = [
    ("🕊️ 1. Preparación y Aquietamiento", [
        "Cierra tus ojos. Lleva tu atención a tu corazón.",
        "Inhala profundamente… Exhala tensión… (3 ciclos)",
        "Entra en el templo sagrado de tu ser interno.",
        "Aquí y ahora, el subconsciente se abre a nuevas semillas de verdad."
    ], False),

    ("💬 2. Afirmaciones con Fe y Convicción", [
        "Estoy alineado con la Sabiduría y el Bien Divino.",
        "La salud, la abundancia, el amor y la paz son mi estado natural.",
        "Lo que me pertenece por derecho divino llega a mí sin esfuerzo y en armonía.",
        "Declaro la Verdad y esta se manifiesta en mi vida."
    ], True),

    ("🌅 3. Visualización Creativa y Sentida", [
        "Visualiza con detalle tu vida ideal: en salud, paz, gozo y propósito.",
        "Siente que ya estás ahí. Observa, escucha, toca, agradece.",
        "Permite que cada imagen sea una semilla viva que el subconsciente reconoce como real."
    ], True),

    ("🙏 4. Entrega y Gratitud", [
        "Entrego este deseo al orden divino. Él sabe el cómo.",
        "Confío en que todo se resuelve de forma perfecta y en el momento perfecto.",
        "Gracias. Esto, o algo mejor, se manifiesta ahora bajo la gracia."
    ], False)
]

contenedor = st.empty()

# Función para generar y reproducir audio temporalmente
def reproducir_texto(texto):
    tts = gTTS(text=texto, lang='es')
    with NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
        tts.save(tmpfile.name)
        st.audio(tmpfile.name, format="audio/mp3")
        return tmpfile.name

# Mostrar cada frase con audio opcional
for titulo, frases, usar_audio in sesion:
    for frase in frases:
        with contenedor:
            st.markdown(f"### {titulo}")
            st.markdown(f"<div class='step'>{frase}</div>", unsafe_allow_html=True)
            if usar_audio:
                archivo = reproducir_texto(frase)
        time.sleep(9)

contenedor.success("🌟 Has sembrado nuevas creencias. Permanece unos momentos en gratitud y silencio. Todo está en marcha.")
