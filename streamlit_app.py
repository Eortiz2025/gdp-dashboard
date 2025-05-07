import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Inicio Diario", layout="centered")
st.title("🌞 Mi mente subconsciente todo lo puede")

# Paso 1: Introducción
st.markdown("### 🧠 Mi mente subconsciente todo lo puede.")

# Paso 2: Pregunta clave
st.markdown("### ✨ Al iniciar el día me hago esta pregunta:")
st.markdown("## ¿Cuál es mi deseo más grande?")

# Paso 3: Cierre de ojos
with st.expander("👁 Cierra los ojos por un minuto y busca dentro de ti"):
    st.info("Respira profundo, relájate y conéctate con lo que verdaderamente deseas.")

# Paso 4: Confirmación del deseo
if st.button("✅ Ya sé lo que deseo"):
    st.success("Excelente. Ahora tomemos los pasos para lograrlo.")
    st.markdown("### 🚶 Paso a paso tu deseo se convierte en realidad si lo sostienes con claridad y emoción.")

    # Paso 5: Elegir acción
    st.markdown("¿Qué deseas hacer ahora para avanzar?")
    opcion = st.radio("Elige tu siguiente acción:", ["Visualizar", "Afirmar", "Escribir"])

    if opcion == "Visualizar":
        st.markdown("### 👁 Cierra los ojos por unos instantes e imagina tu deseo como si ya se hubiese cumplido.")
        st.markdown("- ¿Qué ves?\n- ¿Cómo te sientes?\n- ¿Qué hay a tu alrededor?")
        st.info("Permanece en esa imagen unos segundos, con emoción y gratitud.")

    elif opcion == "Afirmar":
        afirmacion = st.text_input("✍️ Escribe una afirmación clara y positiva basada en tu deseo:")
        if afirmacion.strip() == "":
            st.warning("✋ La afirmación debe ser específica, positiva y sentida como verdadera. Ejemplo:\n\n- 'Estoy en paz y todo fluye en mi vida'\n- 'La riqueza fluye hacia mí de forma perfecta y armoniosa'")
        else:
            st.success(f"Repite varias veces hoy: *{afirmacion}*.\nHazlo con convicción y emoción. Idealmente por la mañana y antes de dormir.")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"afirmacion_{timestamp}.txt"
            st.download_button("📥 Descargar afirmación", data=afirmacion, file_name=filename, mime="text/plain")

    elif opcion == "Escribir":
        descripcion = st.text_area("📝 Describe tu deseo con todos los detalles que puedas imaginar:")
        if descripcion.strip() == "":
            st.warning("🖊️ Escribe tu deseo en términos positivos, en tiempo presente y con gratitud. Ejemplo:\n\n- 'Estoy disfrutando de una vida plena, con salud, amor y prosperidad. Me siento en paz y agradecido.'")
        else:
            st.success("Muy bien. Cuanto más claro y emocional, más fuerte la impresión en tu subconsciente.")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"deseo_{timestamp}.txt"
            st.download_button("📥 Descargar deseo", data=descripcion, file_name=filename, mime="text/plain")
