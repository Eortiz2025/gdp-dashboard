import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import os

# Configuración
st.set_page_config(page_title="Comentarios del Día", layout="centered")
st.title("🗣️ Registro de Comentarios del Día")

# Zona horaria de Pacífico (Mazatlán, Sinaloa, etc.)
zona_pacifico = pytz.timezone("America/Mazatlan")

# Archivo CSV
DATA_FILE = "comentarios.csv"

# Crear archivo si no existe
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["fecha", "nombre", "comentario"]).to_csv(DATA_FILE, index=False)

# Formulario para comentarios
with st.form("formulario_comentario"):
    nombre = st.text_input("Tu nombre")
    comentario = st.text_area("Escribe tu comentario del día")
    enviado = st.form_submit_button("Enviar comentario")

    if enviado:
        if nombre and comentario:
            ahora = datetime.now(zona_pacifico).strftime("%Y-%m-%d %H:%M:%S")
            nueva_fila = {
                "fecha": ahora,
                "nombre": nombre,
                "comentario": comentario
            }
            df = pd.read_csv(DATA_FILE)
            df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Comentario registrado exitosamente.")
        else:
            st.error("❌ Por favor, completa tu nombre y comentario.")

# Zona de dirección protegida
st.markdown("---")
st.subheader("🔒 Zona de Dirección")

password = st.text_input("Ingresa la contraseña para ver los comentarios", type="password")

if password == "1001":
    df = pd.read_csv(DATA_FILE)
    df = df.sort_values(by="fecha", ascending=False)
    st.dataframe(df, use_container_width=True)

    # Botón para descargar CSV
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Descargar comentarios en CSV",
        data=csv_data,
        file_name="comentarios.csv",
        mime="text/csv"
    )

    # Botón para borrar todo
    if st.button("🗑️ Borrar todos los comentarios"):
        confirmar = st.radio("¿Estás seguro?", ["No", "Sí"], index=0)
        if confirmar == "Sí":
            pd.DataFrame(columns=["fecha", "nombre", "comentario"]).to_csv(DATA_FILE, index=False)
            st.success("⚠️ Todos los comentarios han sido eliminados.")
            st.experimental_rerun()
else:
    if password:
        st.error("❌ Contraseña incorrecta.")
