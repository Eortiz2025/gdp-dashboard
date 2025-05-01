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
CHAT_FILE = os.path.join(DATA_PATH, "chat.csv")
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

if not os.path.exists(CHAT_FILE):
    df_chat_init = pd.DataFrame(columns=["expediente_id", "fecha_hora", "autor", "mensaje"])
    df_chat_init.to_csv(CHAT_FILE, index=False)

# Funciones auxiliares

def cargar_expedientes():
    df = pd.read_csv(EXPEDIENTES_FILE)
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

def cargar_chat():
    return pd.read_csv(CHAT_FILE)

def guardar_mensaje_chat(expediente_id, autor, mensaje):
    df = cargar_chat()
    nuevo = {
        "expediente_id": expediente_id,
        "fecha_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "autor": autor,
        "mensaje": mensaje
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv(CHAT_FILE, index=False)

# Formulario rápido en la barra lateral
st.sidebar.title("Formulario rápido")
opcion = st.sidebar.radio("Selecciona una opción", ["Dame las próximas audiencias", "Quiero actualizar un expediente"])

if opcion == "Dame las próximas audiencias":
    st.subheader("📅 Próximas audiencias")
    df_eventos = cargar_eventos()
    df_eventos["fecha"] = pd.to_datetime(df_eventos["fecha"], errors="coerce")
    hoy = pd.to_datetime(date.today())
    futuras = df_eventos[(df_eventos["tipo_evento"] == "Audiencia") & (df_eventos["fecha"] >= hoy)]
    futuras = futuras.sort_values("fecha")
    if futuras.empty:
        st.info("No hay audiencias futuras registradas.")
    else:
        for _, row in futuras.iterrows():
            fecha = row['fecha'].strftime("%d/%m/%Y")
            st.write(f"📌 {fecha}: {row['descripcion']}")

elif opcion == "Quiero actualizar un expediente":
    st.subheader("✏️ Actualizar expediente")
    df_expedientes = cargar_expedientes()
    if df_expedientes.empty:
        st.info("No hay expedientes registrados.")
    else:
        df_expedientes["mostrar"] = df_expedientes["numero_expediente"] + " - " + df_expedientes["cliente"]
        seleccionado = st.selectbox("Selecciona un expediente para actualizar", df_expedientes["mostrar"])
        expediente_id = df_expedientes[df_expedientes["mostrar"] == seleccionado]["id"].values[0]
        st.write(f"Has seleccionado el expediente con ID: `{expediente_id}`")

# Aquí continuarían las secciones previas completas como "Registrar nuevo expediente" y "Consultar expedientes"
# (omitidas aquí por brevedad, pero conservadas en el texto original)
