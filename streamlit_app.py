import streamlit as st
import pandas as pd
import os
from datetime import date
from uuid import uuid4

# Configuración
st.set_page_config(page_title="Seguimiento de Expedientes Laborales", layout="centered")
st.title("⚖️ Seguimiento de Expedientes Laborales")

# Rutas
DATA_PATH = "data"
EXPEDIENTES_FILE = os.path.join(DATA_PATH, "expedientes.csv")
DOCS_PATH = os.path.join(DATA_PATH, "documentos")

# Crear carpetas si no existen
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)

# Inicializar archivo si no existe
if not os.path.exists(EXPEDIENTES_FILE):
    df_init = pd.DataFrame(columns=["id", "cliente", "materia", "numero_expediente", "fecha_inicio", "archivo"])
    df_init.to_csv(EXPEDIENTES_FILE, index=False)

# Funciones
def cargar_expedientes():
    df = pd.read_csv(EXPEDIENTES_FILE)
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"]).dt.strftime("%d/%m/%Y")
    return df

def guardar_expediente(info):
    df = cargar_expedientes()
    df = pd.concat([df, pd.DataFrame([info])], ignore_index=True)
    df.to_csv(EXPEDIENTES_FILE, index=False)

def actualizar_archivo(expediente_id, archivo_nombre):
    df = pd.read_csv(EXPEDIENTES_FILE)
    df.loc[df["id"] == expediente_id, "archivo"] = archivo_nombre
    df.to_csv(EXPEDIENTES_FILE, index=False)

# Menú
seccion = st.sidebar.radio("Menú", ["Registrar expediente", "Ver expedientes"])

# Registro de expediente
if seccion == "Registrar expediente":
    st.header("Registrar nuevo expediente laboral")

    cliente = st.text_input("Nombre del cliente")
    materia = "Laboral"
    numero_expediente = st.text_input("Número de expediente")
    fecha_inicio = st.date_input("Fecha de inicio", value=date.today())

    if st.button("Guardar expediente"):
        if cliente and numero_expediente:
            df = cargar_expedientes()
            if numero_expediente in df["numero_expediente"].astype(str).values:
                st.error("⚠️ Ya existe un expediente con ese número. Debe ser único.")
            else:
                expediente_id = str(uuid4())[:8]
                nuevo = {
                    "id": expediente_id,
                    "cliente": cliente,
                    "materia": materia,
                    "numero_expediente": numero_expediente,
                    "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),  # para guardar correctamente
                    "archivo": ""
                }
                df = pd.read_csv(EXPEDIENTES_FILE)  # recargar sin formateo para guardar correctamente
                df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
                df.to_csv(EXPEDIENTES_FILE, index=False)
                st.success("✅ Expediente registrado correctamente. Puedes subir el archivo después desde el panel de consulta.")
        else:
            st.warning("Por favor completa los campos requeridos.")

# Visualización y carga de archivo posterior
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

        if expediente["archivo"]:
            archivo_path = os.path.join(DOCS_PATH, expediente["archivo"])
            with open(archivo_path, "rb") as pdf_file:
                st.download_button("Descargar documento", data=pdf_file, file_name=expediente["archivo"])
        else:
            st.info("📂 No se ha cargado ningún documento para este expediente.")

        st.markdown("---")
        st.subheader("📤 Subir o reemplazar documento PDF")
        archivo_nuevo = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])
        if archivo_nuevo:
            archivo_nombre = f"{expediente['id']}_{archivo_nuevo.name}"
            archivo_path = os.path.join(DOCS_PATH, archivo_nombre)
            with open(archivo_path, "wb") as f:
                f.write(archivo_nuevo.read())
            actualizar_archivo(expediente["id"], archivo_nombre)
            st.success("✅ Archivo subido correctamente.")
