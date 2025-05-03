import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Configuración de la app
st.set_page_config(page_title="Comentarios del Día", layout="centered")
st.title("🗣️ Registro de Comentarios del Día")

# Archivo donde se guardan los comentarios
DATA_FILE = "comentarios.csv"

# Crear archivo si no existe
if not os.path.exists(DATA_FILE):
    df_vacio = pd.DataFrame(columns=["fecha", "nombre", "comentario"])
    df_vacio.to_csv(DATA_FILE, index=False)

# Formulario para capturar comentario
with st.form("formulario_comentario"):
    nombre = st.text_input("Tu nombre")
    comentario = st.text_area("Escribe tu comentario del día")
    enviado = st.form_submit_button("Enviar comentario")

    if enviado:
        if nombre and comentario:
            nueva_fila = {
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nombre": nombre,
                "comentario": comentario
            }
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Comentario registrado exitosamente.")
        else:
            st.error("Por favor, completa tu nombre y comentario.")

# Mostrar historial de comentarios
st.markdown("---")
st.subheader("📋 Comentarios registrados recientemente")

df = pd.read_csv(DATA_FILE)
df = df.sort_values(by="fecha", ascending=False)
st.dataframe(df, use_container_width=True)
