import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

st.set_page_config(page_title="Reflexión Diaria - Papelería", layout="centered")
st.title("📝 Reflexión Estratégica Diaria")

# Vendedores
VENDEDORES = [
    "Carlos", "Dereck", "Edna", "Estefania",
    "Janeth", "Kyoto", "Lorena", "Selena", "Zaid"
]

# Ruta de almacenamiento
FILE_PATH = "reflexiones.csv"

# Preguntas estratégicas (rotativas)
PREGUNTAS = [
    "¿Qué ocurrió hoy que fue importante o diferente en la tienda?",
    "¿Qué podrías haber hecho hoy para mejorar la experiencia del cliente?",
    "¿Viste algo que podríamos cambiar o mejorar?",
    "¿Qué aprendiste hoy sobre ti o sobre los clientes?",
    "¿Qué idea propones para que mañana sea mejor?"
]

st.subheader("✏️ Registro de Reflexión del Día")

with st.form("formulario_reflexion"):
    nombre = st.selectbox("Tu nombre", VENDEDORES)
    fecha = date.today().strftime("%Y-%m-%d")
    respuestas = []
    for pregunta in PREGUNTAS:
        respuesta = st.text_area(pregunta, key=pregunta)
        respuestas.append(respuesta)
    enviado = st.form_submit_button("Guardar reflexión")

    if enviado:
        nueva_fila = pd.DataFrame([[fecha, nombre] + respuestas])
        columnas = ["Fecha", "Vendedor"] + [f"Pregunta {i+1}" for i in range(len(PREGUNTAS))]
        nueva_fila.columns = columnas

        if os.path.exists(FILE_PATH):
            df = pd.read_csv(FILE_PATH)
            df = pd.concat([df, nueva_fila], ignore_index=True)
        else:
            df = nueva_fila

        df.to_csv(FILE_PATH, index=False)
        st.success("Reflexión registrada correctamente.")

st.subheader("📂 Historial de Reflexiones")
if os.path.exists(FILE_PATH):
    df_historial = pd.read_csv(FILE_PATH)
    vendedor_filtrado = st.selectbox("Filtrar por vendedor", ["Todos"] + VENDEDORES)
    if vendedor_filtrado != "Todos":
        df_historial = df_historial[df_historial["Vendedor"] == vendedor_filtrado]
    st.dataframe(df_historial, use_container_width=True)
else:
    st.info("Aún no hay reflexiones registradas.")
