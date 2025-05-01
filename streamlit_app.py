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

# Funciones

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

# Menú
seccion = st.sidebar.radio("Menú", ["Registrar nuevo expediente", "Consultar expedientes"])

if seccion == "Registrar nuevo expediente":
    st.header("Registrar nuevo expediente")
    cliente = st.text_input("Nombre del cliente").strip()
    numero_expediente = st.text_input("Número de expediente").strip()
    fecha_inicio = st.date_input("Fecha de inicio", value=date.today())

    if st.button("Guardar expediente"):
        if cliente and numero_expediente:
            df_existente = cargar_expedientes()
            if numero_expediente in df_existente["numero_expediente"].astype(str).values:
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

elif seccion == "Consultar expedientes":
    st.header("Consulta de expedientes laborales")
    df = cargar_expedientes()

    df_mostrar = df.copy()
    df_mostrar["Fecha de Inicio"] = pd.to_datetime(df_mostrar["fecha_inicio"], errors="coerce").dt.strftime("%d/%m/%Y")
    df_mostrar = df_mostrar.rename(columns={"numero_expediente": "Expediente"})
    df_mostrar = df_mostrar[["cliente", "Expediente", "Fecha de Inicio"]]

    filtro = st.text_input("Buscar por nombre del cliente")
    if filtro:
        df_mostrar = df_mostrar[df_mostrar["cliente"].str.contains(filtro, case=False)]

    st.dataframe(df_mostrar, use_container_width=True)

    if not df.empty:
        seleccionado = st.selectbox("Selecciona un expediente", df["numero_expediente"])
        expediente = df[df["numero_expediente"] == seleccionado].iloc[0]

        st.subheader(f"Detalles del expediente {seleccionado}")
        st.write(f"**Cliente:** {expediente['cliente']}")
        st.write(f"**Materia:** {expediente['materia']}")

        try:
            fecha_inicio_dt = pd.to_datetime(expediente["fecha_inicio"], errors="coerce")
            fecha_formateada = fecha_inicio_dt.strftime("%d/%m/%Y") if not pd.isnull(fecha_inicio_dt) else "Sin fecha"
        except:
            fecha_formateada = "Sin fecha"
        st.write(f"**Fecha de inicio:** {fecha_formateada}")

        archivo_nombre = str(expediente["archivo"])
        if archivo_nombre and archivo_nombre.lower() != "nan":
            archivo_path = os.path.join(DOCS_PATH, archivo_nombre)
            if os.path.exists(archivo_path):
                with open(archivo_path, "rb") as f:
                    st.download_button("Descargar documento", data=f, file_name=archivo_nombre)

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

        st.markdown("## 💬 Chat interno del expediente")
        autor = st.text_input("Tu nombre o iniciales", max_chars=50)
        mensaje = st.text_area("Escribe tu mensaje")
        if st.button("Enviar mensaje"):
            if autor.strip() and mensaje.strip():
                guardar_mensaje_chat(expediente["id"], autor.strip(), mensaje.strip())
                st.success("Mensaje enviado.")
            else:
                st.warning("Debes completar autor y mensaje.")

        st.markdown("### Historial del chat")
        df_chat = cargar_chat()
        mensajes = df_chat[df_chat["expediente_id"] == expediente["id"]].sort_values("fecha_hora")
        if not mensajes.empty:
            for _, row in mensajes.iterrows():
                st.markdown(f"🗓️ `{row['fecha_hora']}` **{row['autor']}**: {row['mensaje']}")
        else:
            st.info("Aún no hay mensajes en este expediente.")
