import streamlit as st
import pandas as pd
import os
from datetime import date
from uuid import uuid4
from PyPDF2 import PdfReader

# Configuración general
st.set_page_config(page_title="Seguimiento de Expedientes Laborales", layout="centered")
st.title("\u2696\ufe0f Seguimiento de Expedientes Laborales")

# Rutas de datos
DATA_PATH = "data"
EXPEDIENTES_FILE = os.path.join(DATA_PATH, "expedientes.csv")
DOCS_PATH = os.path.join(DATA_PATH, "documentos")

# Asegurar carpetas
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)

# Inicializar archivo de expedientes si no existe
if not os.path.exists(EXPEDIENTES_FILE):
    df_init = pd.DataFrame(columns=["id", "cliente", "materia", "numero_expediente", "fecha_inicio", "archivo"])
    df_init.to_csv(EXPEDIENTES_FILE, index=False)

# Funciones de datos
def cargar_expedientes():
    df = pd.read_csv(EXPEDIENTES_FILE)
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce")
    return df

def guardar_expediente(info):
    df = cargar_expedientes()
    df = pd.concat([df, pd.DataFrame([info])], ignore_index=True)
    df.to_csv(EXPEDIENTES_FILE, index=False)

def actualizar_archivo(expediente_id, archivo_nombre):
    df = cargar_expedientes()
    df.loc[df["id"] == expediente_id, "archivo"] = archivo_nombre
    df.to_csv(EXPEDIENTES_FILE, index=False)

def eliminar_expediente(expediente_id):
    df = cargar_expedientes()
    expediente = df[df["id"] == expediente_id]
    if not expediente.empty:
        archivo = expediente.iloc[0]["archivo"]
        if archivo:
            archivo_path = os.path.join(DOCS_PATH, archivo)
            if os.path.exists(archivo_path):
                os.remove(archivo_path)
        df = df[df["id"] != expediente_id]
        df.to_csv(EXPEDIENTES_FILE, index=False)

# Validación de PDF
def es_pdf_valido(file):
    try:
        reader = PdfReader(file)
        return True
    except:
        return False

# Menú
seccion = st.sidebar.radio("Menú", ["Registrar expediente", "Ver expedientes"])

# Registrar nuevo expediente
if seccion == "Registrar expediente":
    st.header("Registrar nuevo expediente laboral")

    cliente = st.text_input("Nombre del cliente").strip()
    numero_expediente = st.text_input("Número de expediente").strip()
    fecha_inicio = st.date_input("Fecha de inicio", value=date.today())

    if st.button("Guardar expediente"):
        if cliente and numero_expediente:
            df_existente = cargar_expedientes()
            if numero_expediente in df_existente["numero_expediente"].astype(str).values:
                st.error("\u26a0\ufe0f Ya existe un expediente con ese número.")
            else:
                expediente_id = str(uuid4())[:8]
                nuevo = {
                    "id": expediente_id,
                    "cliente": cliente,
                    "materia": "Laboral",
                    "numero_expediente": numero_expediente,
                    "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d"),
                    "archivo": ""
                }
                guardar_expediente(nuevo)
                st.success("\u2705 Expediente registrado correctamente.")
        else:
            st.warning("Por favor completa todos los campos.")

# Ver expedientes
elif seccion == "Ver expedientes":
    st.header("Listado de expedientes laborales")
    df = cargar_expedientes()

    df_mostrar = df.copy()
    df_mostrar["fecha_inicio"] = df_mostrar["fecha_inicio"].dt.strftime("%d/%m/%Y")

    filtro = st.text_input("Buscar por cliente o número de expediente")
    if filtro:
        df_mostrar = df_mostrar[
            df_mostrar["cliente"].str.contains(filtro, case=False) |
            df_mostrar["numero_expediente"].astype(str).str.contains(filtro, case=False)
        ]
    st.dataframe(df_mostrar, use_container_width=True)

    if not df.empty:
        seleccionado = st.selectbox("Selecciona un expediente", df["id"])
        expediente = df[df["id"] == seleccionado].iloc[0]

        st.subheader(f"Detalles del expediente {seleccionado}")
        st.write(f"**Cliente:** {expediente['cliente']}")
        st.write(f"**Materia:** {expediente['materia']}")
        st.write(f"**Número de expediente:** {expediente['numero_expediente']}")
        st.write(f"**Fecha de inicio:** {expediente['fecha_inicio'].strftime('%d/%m/%Y')}")

        # Documento
        if expediente["archivo"]:
            archivo_path = os.path.join(DOCS_PATH, expediente["archivo"])
            if os.path.exists(archivo_path):
                with open(archivo_path, "rb") as f:
                    st.download_button("Descargar documento", data=f, file_name=expediente["archivo"])
            else:
                st.warning("El archivo no se encuentra en el sistema.")
        else:
            st.info("\ud83d\udcc2 No se ha cargado ningún documento.")

        st.markdown("---")
        st.subheader("\ud83d\udcc4 Subir o reemplazar documento PDF")
        archivo_nuevo = st.file_uploader("Selecciona un archivo PDF", type=["pdf"])
        if archivo_nuevo:
            if es_pdf_valido(archivo_nuevo):
                archivo_nombre = f"{expediente['id']}_{archivo_nuevo.name}"
                archivo_path = os.path.join(DOCS_PATH, archivo_nombre)
                with open(archivo_path, "wb") as f:
                    f.write(archivo_nuevo.read())
                actualizar_archivo(expediente["id"], archivo_nombre)
                st.success("\u2705 Archivo subido correctamente.")
            else:
                st.error("El archivo no es un PDF válido.")

        st.markdown("---")
        if st.button("\ud83d\uddd1 Eliminar expediente"):
            eliminar_expediente(expediente["id"])
            st.success("Expediente eliminado correctamente.")
            st.experimental_rerun()
