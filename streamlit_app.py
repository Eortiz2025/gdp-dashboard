import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Inicio Diario", layout="centered")
st.title("🌞 Día a día, en todos sentidos, mejoro y mejoro.")

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
        st.markdown("### 👁 Visualiza el resultado final como si ya se hubiera cumplido.")
        st.markdown("- ¿Qué estás viendo?\n- ¿Cómo te sientes?\n- ¿Qué cambia en ti?")
        st.info("Permanece unos segundos con la imagen en tu mente y siéntela real.")

    elif opcion == "Afirmar":
        st.markdown("### 📣 Cómo crear tu afirmación:")
        st.markdown("""
        Una buena afirmación es:
        - En tiempo presente
        - Positiva y concreta
        - Emocionalmente verdadera

        **Ejemplos:**
        - “Estoy en calma, guiado y bendecido.”
        - “Mi cuerpo se llena de salud y energía cada día.”
        - “Soy merecedor de abundancia y la acepto con alegría.”
        """)

        afirmacion = st.text_input("✍️ Escribe tu afirmación personalizada aquí:")
        if afirmacion.strip():
            st.success(f"Repite esta afirmación varias veces hoy:\n\n*{afirmacion}*")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"afirmacion_{timestamp}.txt"
            st.download_button("📥 Descargar afirmación", data=afirmacion, file_name=filename, mime="text/plain")

    elif opcion == "Escribir":
        st.markdown("### 📝 Cómo escribir tu deseo de forma efectiva:")
        st.markdown("""
        Escribe tu deseo:
        - En presente, como si ya lo vivieras
        - Con gratitud
        - Con emoción y detalle

        **Ejemplo:**
        “Estoy disfrutando de una vida abundante, con salud plena, rodeado de amor y alegría. Me siento en paz.”
        """)

        descripcion = st.text_area("Escribe aquí tu deseo en tus propias palabras:")
        if descripcion.strip():
            st.success("Muy bien. Cuanto más clara y sentida la descripción, más fuerte la impresión en tu subconsciente.")
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"deseo_{timestamp}.txt"
            st.download_button("📥 Descargar deseo", data=descripcion, file_name=filename, mime="text/plain")
