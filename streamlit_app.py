import streamlit as st

st.set_page_config(page_title="Meditación Guiada", layout="centered")
st.title("🧘‍♂️ Meditación Guiada en Silencio")
st.markdown("Lee y contempla cada etapa con calma. Respira profundo y deja que cada palabra entre en ti.")

# Texto por etapas
pasos = [
    "🌀 **Inicio**\n\nBienvenido. Comencemos con una respiración profunda. Inhala calma... exhala tensión.",
    "🌬️ **Silencio y presencia**\n\nAhora, simplemente observa tu respiración. No hagas nada más. Permanece en silencio y presencia.",
    "🌱 **Deseo profundo**\n\nLentamente, pregúntate: ¿Qué deseo experimentar sinceramente? Escucha con el corazón.",
    "🎬 **Visualización**\n\nAhora visualiza: imagina que tu deseo ya es real. Siente cómo se ve, cómo suena, cómo vibra.",
    "🔊 **Afirmación**\n\nRepite mentalmente: *Estoy en paz. Estoy guiado. Lo que es mío por derecho divino viene a mí ahora.*",
    "🙏 **Cierre**\n\nGracias. Ya está hecho. Confío plenamente. Puedes abrir los ojos cuando estés listo."
]

# Guardar paso actual en la sesión
if "paso_actual" not in st.session_state:
    st.session_state.paso_actual = 0

# Mostrar paso actual
st.markdown(pasos[st.session_state.paso_actual])

# Botón para avanzar
if st.session_state.paso_actual < len(pasos) - 1:
    if st.button("➡️ Siguiente paso"):
        st.session_state.paso_actual += 1
else:
    st.success("Has completado la meditación. 🌟")

# Reiniciar
if st.button("🔄 Reiniciar"):
    st.session_state.paso_actual = 0
