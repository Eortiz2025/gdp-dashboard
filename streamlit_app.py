import streamlit as st
import time

st.set_page_config(page_title="Reprogramación Diaria - Murphy & Shinn", layout="centered")
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
<div class='title'>🌟 Ritual Diario de Reprogramación Subconsciente</div>
<div class='subtitle'>Basado en las enseñanzas de Joseph Murphy y Florence Scovel Shinn</div>
""", unsafe_allow_html=True)

ritual_diario = [
    ("🕊️ Fase 1: Silencio y Respiración", [
        "Cierra tus ojos. Lleva tu atención al corazón.",
        "Inhala fe… Exhala preocupación…",
        "Inhala paz… Exhala juicio…",
        "Inhala amor… Exhala resistencia…",
        "Siente cómo entras en el templo interior de tu mente subconsciente."
    ], 5),

    ("💬 Fase 2: Afirmaciones Conscientes", [
        "Estoy alineado con la Verdad divina que me guía en todo momento.",
        "Lo que me pertenece por derecho divino llega a mí ahora, con gracia y sin esfuerzo.",
        "Soy salud, abundancia, amor y paz. Esto es la verdad de mi ser."
    ], 5),

    ("🌅 Fase 3: Visualización Creativa", [
        "Imagina la escena perfecta: tu cuerpo sano, tu hogar lleno de armonía, tu propósito cumplido.",
        "Observa con detalle. ¿Qué colores ves? ¿Qué palabras escuchas? ¿Cómo se siente tu corazón?",
        "Siéntelo como real. Ya lo eres. Ya está hecho."
    ], 6),

    ("🙏 Fase 4: Entrega y Agradecimiento", [
        "Entrego este deseo al Espíritu. Confío plenamente en el orden divino.",
        "Gracias por la manifestación que ya está en camino.",
        "Esto, o algo mejor, se manifiesta ahora bajo la gracia y de manera perfecta."
    ], 5)
]

contenedor = st.empty()
st.markdown("<div class='subtitle'>Prepara tu corazón. Este es un momento sagrado.</div>", unsafe_allow_html=True)

for titulo, frases, pausa in ritual_diario:
    for i in range(len(frases)):
        with contenedor:
            st.markdown(f"### {titulo}")
            st.markdown(f"<div class='step'>{'<br><br>'.join(frases[:i+1])}</div>", unsafe_allow_html=True)
        time.sleep(pausa)

contenedor.success("🌟 Tu subconsciente ha recibido semillas de verdad. Permanece unos instantes en silencio si lo deseas.")
