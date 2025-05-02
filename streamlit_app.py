import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
from uuid import uuid4

# Configuración general
st.set_page_config(page_title="Sistema Bravo & Asociados", layout="centered")
st.title("📂 Sistema Bravo & Asociados")

# Rutas de archivos
DATA_PATH = "data"
EXPEDIENTES_FILE = os.path.join(DATA_PATH, "expedientes.csv")
EVENTOS_FILE = os.path.join(DATA_PATH, "eventos.csv")
CHAT_FILE = os.path.join(DATA_PATH, "chat.csv")
DOCS_PATH = os.path.join(DATA_PATH, "documentos")
EVENTOS_TIPOS = ["Audiencia", "Escrito presentado", "Acuerdo", "Resolución", "Otro"]

os.makedirs(DATA_PATH, exist_ok=True)
os.makedirs(DOCS_PATH, exist_ok=True)

if not os.path.exists(EXPEDIENTES_FILE):
    pd.DataFrame(columns=["id", "cliente", "materia", "numero_expediente", "fecha_inicio", "archivo"]).to_csv(EXPEDIENTES_FILE, index=False)
if not os.path.exists(EVENTOS_FILE):
    pd.DataFrame(columns=["expediente_id", "fecha", "tipo_evento", "descripcion"]).to_csv(EVENTOS_FILE, index=False)
if not os.path.exists(CHAT_FILE):
    pd.DataFrame(columns=["expediente_id", "fecha_hora", "autor", "mensaje"]).to_csv(CHAT_FILE, index=False)

# Funciones auxiliares
def cargar_expedientes():
    df = pd.read_csv(EXPEDIENTES_FILE)
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce")
    return df

def guardar_expediente(info):
    df = cargar_expedientes()
    df = pd.concat([df, pd.DataFrame([info])], ignore_index=True)
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

# Menú principal con botones del mismo tamaño
if "vista_actual" not in st.session_state:
    st.session_state.vista_actual = "Inicio"

col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("➕ Registrar expediente", use_container_width=True):
        st.session_state.vista_actual = "Registro"
with col2:
    if st.button("💬 Chat expediente", use_container_width=True):
        st.session_state.vista_actual = "Chat"
with col3:
    if st.button("📁 Ver expedientes", use_container_width=True):
        st.session_state.vista_actual = "Expedientes"
with col4:
    if st.button("📅 Próximas audiencias", use_container_width=True):
        st.session_state.vista_actual = "Audiencias"

st.markdown("---")

# Vista: Registro
if st.session_state.vista_actual == "Registro":
    st.subheader("Registrar nuevo expediente")
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

# Vista: Chat
elif st.session_state.vista_actual == "Chat":
    st.subheader("💬 Actualización de expedientes (Chat)")
    df_expedientes = cargar_expedientes()

    if not df_expedientes.empty:
        seleccionado = st.selectbox("Selecciona expediente", ["Selecciona un expediente"] + [f"{num} - {cliente}" for num, cliente in zip(df_expedientes["numero_expediente"], df_expedientes["cliente"])], key="chat_exp")

        if seleccionado != "Selecciona un expediente":
            expediente_numero = seleccionado.split(" - ")[0]
            expediente = df_expedientes[df_expedientes["numero_expediente"] == expediente_numero]

            if not expediente.empty:
                expediente = expediente.iloc[0]

                autor = st.text_input("Tu nombre o iniciales", key="autor_chat")
                mensaje = st.text_area("Mensaje", key="mensaje_chat")
                if st.button("Enviar mensaje"):
                    if autor.strip() and mensaje.strip():
                        guardar_mensaje_chat(expediente["id"], autor.strip(), mensaje.strip())
                        st.success("Mensaje enviado.")
                    else:
                        st.warning("Completa autor y mensaje.")

                st.markdown("### Historial del chat")
                df_chat = cargar_chat()
                mensajes = df_chat[df_chat["expediente_id"] == expediente["id"]].sort_values("fecha_hora")
                for idx, row in mensajes.iterrows():
                    st.markdown(f"🗓️ `{row['fecha_hora']}` **{row['autor']}**: {row['mensaje']}")

                # Formulario para agendar evento
                with st.expander("📅 Agendar un evento", expanded=False):
                    with st.form("form_evento_chat"):
                        fecha_evento = st.date_input("Fecha del evento", value=date.today())
                        tipo_evento = st.selectbox("Tipo de evento", EVENTOS_TIPOS)
                        descripcion = st.text_area("Descripción del evento")
                        submit = st.form_submit_button("Guardar evento")
                        if submit:
                            guardar_evento(expediente["id"], fecha_evento, tipo_evento, descripcion)
                            st.success("✅ Evento guardado.")
            else:
                st.warning("No se encontró el expediente seleccionado.")
        else:
            st.info("Por favor selecciona un expediente.")
    else:
        st.info("No hay expedientes disponibles.")

# Vista: Expedientes
elif st.session_state.vista_actual == "Expedientes":
    st.subheader("📁 Listado de expedientes")
    df_expedientes = cargar_expedientes()
    df_eventos = cargar_eventos()

    df_eventos["fecha"] = pd.to_datetime(df_eventos["fecha"], errors="coerce")
    hoy = pd.to_datetime(date.today())

    futuras = df_eventos[(df_eventos["tipo_evento"] == "Audiencia") & (df_eventos["fecha"] >= hoy)]
    futuras = futuras.sort_values("fecha")

    df_expedientes["Proxima Audiencia"] = df_expedientes["id"].apply(
        lambda x: futuras[futuras["expediente_id"] == x]["fecha"].min() if x in futuras["expediente_id"].values else None
    )

    df_mostrar = df_expedientes[["cliente", "numero_expediente", "Proxima Audiencia"]]
    df_mostrar["Proxima Audiencia"] = pd.to_datetime(df_mostrar["Proxima Audiencia"], errors="coerce")
    df_mostrar["Proxima Audiencia"] = df_mostrar["Proxima Audiencia"].dt.strftime("%d/%m/%Y")

    df_mostrar = df_mostrar.rename(columns={
        "cliente": "Cliente",
        "numero_expediente": "Expediente",
        "Proxima Audiencia": "Próxima Audiencia"
    })

    st.dataframe(df_mostrar, use_container_width=True)

# Vista: Audiencias
elif st.session_state.vista_actual == "Audiencias":
    st.subheader("📅 Próximas audiencias")
    df_eventos = cargar_eventos()
    df_expedientes = cargar_expedientes()
    df_eventos["fecha"] = pd.to_datetime(df_eventos["fecha"], errors="coerce")
    hoy = pd.to_datetime(date.today())
    futuras = df_eventos[(df_eventos["tipo_evento"] == "Audiencia") & (df_eventos["fecha"] >= hoy)]
    futuras = futuras.sort_values("fecha")

    if futuras.empty:
        st.info("No hay audiencias futuras registradas.")
    else:
        for _, row in futuras.iterrows():
            fecha = row['fecha']
            fecha_str = f"{fecha.day} de {fecha.strftime('%B').capitalize()}"
            exp_id = row['expediente_id']
            expediente = df_expedientes[df_expedientes['id'] == exp_id]
            numero_exp = expediente['numero_expediente'].values[0] if not expediente.empty else "(no encontrado)"
            cliente = expediente['cliente'].values[0] if not expediente.empty else "(no encontrado)"
            st.markdown(f"""📌 {fecha_str} | {numero_exp} ({cliente})  
📝 {row['descripcion']}""")
