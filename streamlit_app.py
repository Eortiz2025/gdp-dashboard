import streamlit as st
import time

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
        margin-bottom: 30px;
    }
    .step {
        font-size: 1.2em;
        line-height: 1.6em;
    }
</style>
<div class='title'>🌟 Sesión Transformadora de Reprogramación</div>
<div class='subtitle'>Basada en Joseph Murphy y Florence Scovel Shinn</div>
""", unsafe_allow_html=True)

# Etapas de la sesión combinando ambas metodologías
sesion = [
    ("🕊️ 1. Preparación y Aquietamiento", [
        "Cierra tus ojos. Lleva tu atención a tu corazón.",
        "Inhala profundamente… Exhala tensión… (3 ciclos)",
        "Entra en el templo sagrado de tu ser interno.",
        "Aquí y ahora, el subconsciente se abre a nuevas semillas de verdad."
    ], 5),

    ("💬 2. Afirmaciones con Fe y Convicción", [
        "Estoy alineado con la Sabiduría y el Bien Divino.",
        "La salud, la abundancia, el amor y la paz son mi estado natural.",
        "Lo que me pertenece por derecho divino llega a mí sin esfuerzo y en armonía.",
        "Declaro la Verdad y esta se manifiesta en mi vida."
    ], 6),

    ("🌅 3. Visualización Creativa y Sentida", [
        "Visualiza con detalle tu vida ideal: en salud, paz, gozo y propósito.",
        "Siente que ya estás ahí. Observa, escucha, toca, agradece.",
        "Permite que cada imagen sea una semilla viva que el subconsciente reconoce como real."
    ], 6),

    ("🙏 4. Entrega y Gratitud", [
        "Entrego este deseo al orden divino. El sabe el cómo.",
        "Confío en que todo se resuelve de forma perfecta y en el momento perfecto.",
        "Gracias. Esto, o algo mejor, se manifiesta ahora bajo la gracia."
    ], 5)
]

contenedor = st.empty()
st.markdown("<div class='subtitle'>Este es un momento sagrado. Dejo que la Verdad me transforme.</div>", unsafe_allow_html=True)

for titulo, frases, pausa in sesion:
    for i in range(len(frases)):
        with contenedor:
            st.markdown(f"### {titulo}")
            st.markdown(f"<div class='step'>{'<br><br>'.join(frases[:i+1])}</div>", unsafe_allow_html=True)
        time.sleep(pausa)

contenedor.success("🌟 Has sembrado nuevas creencias. Permanece unos momentos en gratitud y silencio. Todo está en marcha.")
