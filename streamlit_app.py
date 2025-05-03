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

# Preguntas con intención empática y formativa
PREGUNTAS = [
    "¿Qué momento del día te hizo sentir orgulloso de tu trabajo hoy?",
    "¿Qué acción pequeña tuviste hoy que generó una sonrisa o agradecimiento en un cliente?",
    "¿Qué puedes agradecer del día de hoy en la tienda?",
    "¿Qué hiciste hoy que ayudó a tus compañeros, aunque fuera algo pequeño?",
    "¿Qué producto o área crees que merece más atención o cariño en cómo lo presentamos?",
    "¿Qué escuchaste de los clientes hoy que te hizo pensar diferente?",
    "¿Cómo sentiste el ambiente en la tienda hoy? ¿Qué podríamos hacer para que se sienta mejor?",
    "¿Qué idea se te ocurrió hoy para mejorar algo en nuestra papelería?",
    "¿Qué aprendiste hoy que te gustaría compartir con el equipo?",
    "¿Qué hiciste hoy para ser mejor que ayer, aunque sea un poco?"
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
