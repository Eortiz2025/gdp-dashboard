import streamlit as st
import pandas as pd

st.set_page_config(page_title="Decisiones estilo Dalio", layout="centered")

st.title("📊 Sistema de Decisiones Ponderadas - Estilo Ray Dalio")

st.markdown("""
Este sistema te ayuda a tomar decisiones basadas en opiniones **ponderadas por credibilidad**.
""")

st.subheader("Paso 1: Ingresar opiniones")

# Inicializar o cargar la tabla de entradas
if "tabla_opiniones" not in st.session_state:
    st.session_state.tabla_opiniones = pd.DataFrame(columns=["Persona", "Opinión (1-10)", "Credibilidad (1-10)"])

# Formulario para agregar una nueva opinión
with st.form("formulario_opinion"):
    col1, col2, col3 = st.columns(3)
    with col1:
        persona = st.text_input("Nombre de la persona")
    with col2:
        opinion = st.slider("Opinión", 1, 10, 7)
    with col3:
        cred = st.slider("Credibilidad", 1, 10, 5)
    enviar = st.form_submit_button("Agregar")

    if enviar and persona:
        nueva_fila = pd.DataFrame([[persona, opinion, cred]], columns=st.session_state.tabla_opiniones.columns)
        st.session_state.tabla_opiniones = pd.concat([st.session_state.tabla_opiniones, nueva_fila], ignore_index=True)

# Mostrar la tabla actual
st.write("### Opiniones Registradas")
st.dataframe(st.session_state.tabla_opiniones, use_container_width=True)

# Paso 2: Cálculo del promedio ponderado
if not st.session_state.tabla_opiniones.empty:
    st.subheader("Paso 2: Resultado de la decisión")

    df = st.session_state.tabla_opiniones
    df["Ponderado"] = df["Opinión (1-10)"] * df["Credibilidad (1-10)"]

    total_ponderado = df["Ponderado"].sum()
    total_credibilidad = df["Credibilidad (1-10)"].sum()

    resultado = round(total_ponderado / total_credibilidad, 2) if total_credibilidad > 0 else 0

    st.metric(label="Promedio Ponderado de la Decisión", value=resultado)

    with st.expander("Ver cálculo detallado"):
        st.write(df)

# Botón para reiniciar
if st.button("🔄 Reiniciar tabla"):
    st.session_state.tabla_opiniones = pd.DataFrame(columns=["Persona", "Opinión (1-10)", "Credibilidad (1-10)"])
