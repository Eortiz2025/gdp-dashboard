import streamlit as st
import time

st.set_page_config(page_title="Inicio Diario", layout="centered")
st.title("🌞 Inicio de tu práctica consciente")

# Paso 1: Introducción
st.markdown("### 🧠 Mi mente subconsciente todo lo puede.")
time.sleep(1)

# Paso 2: Pregunta clave
time.sleep(1)
st.markdown("### ❓ Para empezar el día tengo una pregunta que hacerme:")
st.markdown("## ¿Cuál es mi deseo más grande?")

# Paso 3: Cierre de ojos
with st.expander("👁 Cierra los ojos por un minuto y busca dentro de ti"):
    st.info("Respira profundo, relájate y conéctate con lo que verdaderamente deseas.")

# Paso 4: Confirmación del deseo
if st.button("✅ Ya sé lo que deseo"):
    st.success("Excelente. Ahora tomemos los pasos para lograrlo.")
    st.markdown("### 🚶 Paso a paso tu deseo se convierte en realidad si lo sostienes con claridad y emoción.")
