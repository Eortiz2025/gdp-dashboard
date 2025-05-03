import streamlit as st
import pandas as pd
from datetime import date
import os
import random

st.set_page_config(page_title="Reflexión Estratégica Diaria", layout="centered")
st.title("🌱 Reflexión con Propósito - Papelería")

# Vendedores
VENDEDORES = [
    "Carlos", "Dereck", "Edna", "Estefania",
    "Janeth", "Kyoto", "Lorena", "Selena", "Zaid"
]

# Ruta de almacenamiento
FILE_PATH = "reflexiones.csv"

# Preguntas optimizadas para edades 20-30 años
PREGUNTAS = [
    "¿Qué hiciste hoy que hizo sonreír o sentirse bien a un cliente?",
    "¿Qué parte de tu día te hizo sentir que esto no es ‘solo un trabajo’?",
    "Si fueras tú el cliente hoy, ¿qué detalle te habría sorprendido (para bien o mal)?",
    "¿Qué idea loca, simple o creativa se te ocurrió hoy para mejorar la tienda?",
    "¿Quién del equipo te inspiró hoy y por qué?",
    "¿Qué aprendiste hoy sin que nadie te lo dijera?",
    "¿En qué momento del día pensaste: ‘esto podríamos hacerlo mejor’?",
    "¿Qué hiciste hoy que te gustaría repetir todos los días?",
    "¿Qué viste hoy que te hizo pensar: ‘esto sí es calidez’?",
    "¿Qué agradeces de este día en la tienda, por mínimo que sea?"
]

# Cargar historial
if os.path.exists(FILE_PATH):
    historial = pd.read_csv(FILE_PATH)
else:
    historial = pd.DataFrame(columns=["Fecha", "Vendedor", "Pregunta", "Respuesta"])

st.subheader("✏️ Registrar Reflexión del Día")

nombre = st.selectbox("Selecciona tu nombre", ["Selecciona..."] + VENDEDORES)

if nombre != "Selecciona...":
    with st.form("formulario"):
        # Obtener preguntas ya respondidas por el usuario
        preguntas_respondidas = historial[historial["Vendedor"] == nombre]["Pregunta"].tolist()
        preguntas_disponibles = [p for p in PREGUNTAS if p not in preguntas_respondidas]

        if preguntas_disponibles:
            pregunta = random.choice(preguntas_disponibles)
        else:
            pregunta = random.choice(PREGUNTAS)  # Reinicio si ya contestó todas

        st.markdown(f"**Pregunta para hoy:** _{pregunta}_")
        respuesta = st.text_area("Tu respuesta")
        enviar = st.form_submit_button("Enviar reflexión")

        if enviar and respuesta.strip():
            nueva_fila = pd.DataFrame([[date.today(), nombre, pregunta, respuesta]], columns=["Fecha", "Vendedor", "Pregunta", "Respuesta"])
            historial = pd.concat([historial, nueva_fila], ignore_index=True)
            historial.to_csv(FILE_PATH, index=False)
            st.success("Gracias por compartir tu reflexión.")

st.subheader("📘 Historial de Reflexiones")
filtrar = st.selectbox("Filtrar por vendedor", ["Selecciona..."] + VENDEDORES)

if filtrar != "Selecciona...":
    historial = historial[historial["Vendedor"] == filtrar]
    st.dataframe(historial.sort_values(by="Fecha", ascending=False), use_container_width=True)
else:
    st.info("Selecciona un nombre para ver el historial correspondiente.")
