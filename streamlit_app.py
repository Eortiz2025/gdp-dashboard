import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
from uuid import uuid4
from PyPDF2 import PdfReader

# Configuración general
st.set_page_config(page_title="Seguimiento de Expedientes Laborales", layout="centered")
st.title("Seguimiento de Expedientes Laborales")

# Rutas de datos
DATA_PATH = "data"
EXPEDIENTES_FILE = os.path.join(DATA_PATH, "expedientes.csv")
DOCS_PATH = os.path.join(DATA_PATH, "documentos")
EVENTOS_FILE = os.path.join(DATA_PATH, "eventos.csv")
EVENTOS_TIPOS = ["Audiencia", "Escrito presentado", "Acuerdo", "Resolución", "Otro"]

# Asegurar carpetas
os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)

# Inicializar archivos si no existen
if not os.path.exists(EXPEDIENTES_FILE):
    df_init = pd.DataFrame(columns=["id", "cliente", "materia", "numero_expediente", "fecha_inicio", "archivo"])
    df_init.to_csv(EXPEDIENTES_FILE, index=False)

if not os.path.exists(EVENTOS_FILE):
    df_eventos_init = pd.DataFrame(columns=["expediente_id", "fecha", "tipo_evento", "descripcion"])
    df_eventos_init.to_csv(EVENTOS_FILE, index=False)

# Funciones de expedientes
def cargar_expedientes():
    columnas = ["id", "cliente", "materia", "numero_expediente", "fecha_inicio", "archivo"]
    try:
        df = pd.read_csv(EXPEDIENTES_FILE)
        if not all(col in df.columns for col in columnas):
            raise ValueError("Columnas faltantes")
    except Exception:
        df = pd.DataFrame(columns=columnas)
        df.to_csv(EXPEDIENTES_FILE, index=False)
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce")
    return df

def guardar_expediente(info):
    df = cargar_expedientes()
    df = pd.concat([df, pd.DataFrame([info])], ignore_index=True)
    df.to_csv(EXPEDIENTES_FILE, index=False, date_format="%Y-%m-%d")

def actualizar_archivo(expediente_id, archivo_nombre):
    df = cargar_expedientes()
    df.loc[df["id"] == expediente_id, "archivo"] = archivo_nombre
    df.to_csv(EXPEDIENTES_FILE, index=False, date_format="%Y-%m-%d")

def eliminar_expediente(expediente_id):
    df = cargar_expedientes()
    expediente = df[df["id"] == expediente_id]
    if not expediente.empty:
        archivo = expediente.iloc[0]["archivo"]
        archivo = str(archivo) if pd.notna(archivo) else ""
        if archivo:
            archivo_path = os.path.join(DOCS_PATH, archivo)
            if os.path.exists(archivo_path):
                os.remove(archivo_path)
        df = df[df["id"] != expediente_id]
        df.to_csv(EXPEDIENTES_FILE, index=False, date_format="%Y-%m-%d")

# Validación de PDF
def es_pdf_valido(file):
    try:
        reader = PdfReader(file)
        return True
    except:
        return False

# Funciones de eventos
def cargar_eventos():
    return pd.read_csv(EVENTOS_FILE)

def guardar_evento(expediente_id, fecha, tipo_evento, descripcion):
    df = cargar_eventos()
    nuevo = {
        "expediente_id": expediente_id,
        "fecha": fecha.strftime("%Y-%m-%d"),
        "tipo_evento": tipo_evento,
        "descripcion": descripcion
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(EVENTOS_FILE, index=False)

# Menú
seccion = st.sidebar.radio("Menú", ["Registrar nuevo expediente", "Consultar expedientes"])

# Registrar nuevo expediente
if seccion == "Registrar nuevo expediente":
    st.header("Registrar nuevo expediente")

    cliente = st.text_input("Nombre del cliente").strip()
    numero_expediente = st.text_input("Número de expediente").strip()
    fecha_inicio = st.date_input("Fecha de inicio", value=date.today())

    if st.button("Guardar expediente"):
        if cliente and numero_expediente:
            df_existente = cargar_expedientes()
            if "numero_expediente" in df_existente.columns and numero_expediente in df_existente["numero_expediente"].astype(str).values:
                st.error("Ya existe un expediente con ese número.")
            else:
                expediente_id = str(uuid4())[:8]
                nuevo = {
                    "id": expediente_id,
                    "cliente": cliente,
                    "materia": "Laboral",
                    "numero_expediente": numero_expediente,
                    "fecha_inicio": datetime.combine(fecha_inicio, datetime.min.time()),
                    "archivo": ""
                }
                guardar_expediente(nuevo)
                st.success("Expediente registrado correctamente.")
        else:
            st.warning("Por favor completa todos los campos.")

# Consultar expedientes
elif seccion == "Consultar expedientes":
    st.header("Consulta de expedientes laborales")
    df = cargar_expedientes()

    df_mostrar = df.copy()
    df_mostrar["fecha_inicio"] = pd.to_datetime(df_mostrar["fecha_inicio"], errors="coerce")
    df_mostrar = df_mostrar[["cliente", "numero_expediente", "fecha_inicio"]]
    df_mostrar["fecha_inicio"] = df_mostrar["fecha_inicio"].dt.strftime("%d/%m/%Y")
    df_mostrar["fecha_inicio"] = df_mostrar["fecha_inicio"].fillna("Sin fecha").replace("NaT", "Sin fecha")

    filtro = st.text_input("Buscar por nombre del cliente o número de expediente")
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
        fecha_formateada = pd.to_datetime(expediente["fecha_inicio"], errors="coerce").strftime("%d/%m/%Y")
        st.write(f"**Fecha de inicio:** {fecha_formateada}")

        archivo_nombre = str(expediente["archivo"])
        if archivo_nombre and archivo_nombre.lower() != "nan":
            archivo_path = os.path.join(DOCS_PATH, archivo_nombre)
            if os.path.exists(archivo_path):
                with open(archivo_path, "rb") as f:
                    st.download_button("Descargar documento", data=f, file_name=archivo_nombre)
            else:
                st.warning("El archivo no se encuentra disponible en la carpeta.")
        else:
            st.info("📂 No se ha cargado ningún documento.")

        st.markdown("## 📜 Cronología del expediente")
        df_eventos = cargar_eventos()
        eventos = df_eventos[df_eventos["expediente_id"] == expediente["id"]]
        if not eventos.empty:
            eventos["fecha"] = pd.to_datetime(eventos["fecha"], errors="coerce")
            eventos = eventos.sort_values("fecha")
            for _, row in eventos.iterrows():
                st.markdown(f"**{row['fecha'].strftime('%d/%m/%Y')} – {row['tipo_evento']}**: {row['descripcion']}")
        else:
            st.info("Este expediente aún no tiene eventos registrados.")

        st.markdown("### ➕ Agregar evento")
        with st.form("form_evento"):
            fecha_evento = st.date_input("Fecha del evento", value=date.today(), key="fecha_evento")
            tipo_evento = st.selectbox("Tipo de evento", EVENTOS_TIPOS, key="tipo_evento")
            descripcion = st.text_area("Descripción del evento", key="descripcion_evento")
            submit = st.form_submit_button("Guardar evento")
            if submit:
                guardar_evento(expediente["id"], fecha_evento, tipo_evento, descripcion)
                st.success("✅ Evento agregado correctamente. Recarga la página para verlo.")
