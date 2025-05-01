import streamlit as st
import pandas as pd
import os
from datetime import date
from uuid import uuid4

# Configuración de la app
st.set_page_config(page_title="Seguimiento de Expedientes Laborales", layout="centered")
st.title("⚖️ Seguimiento de Expedientes Laborales")

# Rutas
DATA_PATH = "data"
EXPEDIENTES_FILE = os.path.join(DATA_PATH, "expedientes.csv")
DOCS_PATH = os.path.join(DATA_PATH, "documentos")

# Crear carpetas si no existen
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)

# Inicializar archivo CSV si no existe
if not os.path.exists(EXPEDIENTES_FILE):
    df_init = pd.DataFrame(columns=["id", "cliente", "materia", "numero_expediente", "fecha_inicio", "archivo"])
    df_init.to_csv(EXPEDIENTES_FILE, index=False)

# Función para cargar expedientes
def cargar_expedientes():
    return pd.read_csv(EXPEDIENTES_FILE)

# Función para guardar un nuevo expediente
def guardar_expediente(info):
    df = cargar_expedientes()
    df = pd.concat([df, pd.DataFrame([info])], ignore_index=True)
    df.to_csv(EXPEDIENTES_FILE, index=False)

# Navegación principal
seccion = st.sidebar.radio("Menú", ["Registrar expediente", "Ver expedientes"])

if seccion == "Registrar expediente":
    st.header("Registrar nuevo expediente laboral")

    cliente = st.text_input("Nombre del cliente")
    materia = "Laboral"  # Materia fija
    numero_expediente = st.text_input("Número de expediente")
    fecha_inicio = st.date_input("Fecha de inicio", value=date.today())
    archivo = st.file_uploader("Documento PDF del expediente", type=["pdf"])

    if st.button("Guardar expediente"):
        if cliente and numero_expediente and archivo:
            df = cargar_expedientes()
            if numero_expediente in df["numero_expediente"].astype(str).values:
                st.error("⚠️ Ya existe un expediente con ese número. Debe ser único.")
            else:
                expediente_id = str(uuid4())[:8]
                archivo_nombre = f"{expediente_id}_{archivo.name}"
                archivo_path = os.path.join(DOCS_PATH, archivo_nombre)
                with open(archivo_path, "wb") as f:
                    f.write(archivo.read())

                nuevo = {
                    "id": expediente_id,
                    "cliente": cliente,
                    "materia": materia,
                    "numero_expediente": numero_expediente,
                    "fecha_inicio": fecha_inicio,
                    "archivo": archivo_nombre
                }
                guardar_expediente(nuevo)
                st.success("✅ Expediente guardado correctamente.")
        else:
            st.warning("Por favor completa todos los campos y sube un archivo.")

elif seccion == "Ver expedientes":
    st.header("Listado de expedientes laborales")
    df = cargar_expedientes()
    filtro = st.text_input("Buscar por nombre del cliente o número de expediente")
    if filtro:
        df = df[df["cliente"].str.contains(filtro, case=False) | df["numero_expediente"].astype(str).str.contains(filtro, case=False)]
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        seleccionado = st.selectbox("Selecciona un expediente", df["id"])
        expediente = df[df["id"] == seleccionado].iloc[0]
        st.subheader(f"Detalles del expediente {seleccionado}")
        st.write(f"**Cliente:** {expediente['cliente']}")
        st.write(f"**Materia:** {expediente['materia']}")
        st.write(f"**Número de expediente:** {expediente['numero_expediente']}")
        st.write(f"**Fecha de inicio:** {expediente['fecha_inicio']}")

        archivo_path = os.path.join(DOCS_PATH, expediente["archivo"])
        with open(archivo_path, "rb") as pdf_file:
            st.download_button("Descargar documento", data=pdf_file, file_name=expediente["archivo"])
