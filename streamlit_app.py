import streamlit as st
import pandas as pd
from datetime import datetime
import os
from io import BytesIO

# Configuración
st.set_page_config(page_title="Comentarios del Día", layout="centered")
st.title("🗣️ Registro de Comentarios del Día")

# Archivo CSV
DATA_FILE = "comentarios.csv"

# Crear si no existe
if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=["fecha", "nombre", "comentario"]).to_csv(DATA_FILE, index=False)

# Formulario
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
            st.error("❌ Por favor, completa tu nombre y comentario.")

# Zona de dirección con contraseña
st.markdown("---")
st.subheader("🔒 Zona de Dirección")

password = st.text_input("Ingresa la contraseña para ver los comentarios", type="password")

if password == "1001":
    df = pd.read_csv(DATA_FILE)
    df = df.sort_values(by="fecha", ascending=False)
    st.dataframe(df, use_container_width=True)

    # Convertir a Excel en memoria
    def convertir_a_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Comentarios')
        output.seek(0)
        return output

    excel_file = convertir_a_excel(df)

    st.download_button(
        label="📥 Descargar comentarios en Excel",
        data=excel_file,
        file_name="comentarios.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
elif password:
    st.error("❌ Contraseña incorrecta.")
