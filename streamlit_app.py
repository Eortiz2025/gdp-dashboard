import streamlit as st
from gtts import gTTS
from pydub.generators import Sine
from pydub import AudioSegment
import io

st.set_page_config(page_title="Meditación Guiada", layout="centered")
st.title("🧘‍♂️ Meditación Guiada con Afirmaciones")

# Textos para cada fase
frases = {
    "Intro": "Bienvenido. Comencemos con una respiración profunda. Inhala calma... exhala tensión.",
    "Silencio": "Ahora, simplemente observa tu respiración. No hagas nada más. Permanece en silencio y presencia.",
    "Deseo": "Lentamente, pregúntate: ¿Qué deseo experimentar sinceramente? Escucha con el corazón.",
    "Visualización": "Ahora visualiza: imagina que tu deseo ya es real. Siente cómo se ve, cómo suena, cómo vibra.",
    "Afirmación": "Repite conmigo: Estoy en paz. Estoy guiado. Lo que es mío por derecho divino viene a mí ahora.",
    "Cierre": "Gracias. Ya está hecho. Confío plenamente. Puedes abrir los ojos cuando estés listo."
}

# Selección de partes
seleccion = st.multiselect("Selecciona las partes que deseas incluir:", list(frases.keys()), default=list(frases.keys()))

# Botón para generar y reproducir audio
if st.button("🎧 Generar Meditación"):
    for etapa in seleccion:
        with st.spinner(f"Generando voz para: {etapa}..."):
            tts = gTTS(frases[etapa], lang="es")
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)
            st.audio(mp3_fp, format="audio/mp3")

    # Gong al final
    st.markdown("### 🔔 Sonido final tipo gong:")
    gong_audio = Sine(440).to_audio_segment(duration=1000).fade_in(200).fade_out(200)
    buffer = io.BytesIO()
    gong_audio.export(buffer, format="mp3")
    buffer.seek(0)
    st.audio(buffer, format="audio/mp3")
