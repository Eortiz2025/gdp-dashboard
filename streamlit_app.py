import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Dot Collector - Estilo Ray Dalio", layout="wide")

st.title("🟡 Dot Collector - Evaluación por Áreas Temáticas")

st.markdown("""
Evalúa a las personas de tu equipo en distintas áreas clave (estilo Ray Dalio).  
Los puntos recolectados se almacenan para análisis y construcción de perfiles de credibilidad.
""")

# Lista de áreas temáticas personalizables
AREAS = ["Estrategia", "Marketing", "Producto", "Liderazgo", "Comunicación", "Innovación"]

# Inicializar tabla en sesión
if "dots" not in st.session_state:
    st.session_state.dots = pd.DataFrame(columns=["Persona", "Área", "Evaluación", "Comentario", "Fecha"])

# Formulario de evaluación
st.subheader("🔘 Nueva evaluación")
with st.form("form_dot"):
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        persona = st.text_input("Nombre de la persona a evaluar")
    with col2:
        area = st.selectbox("Área temática", AREAS)
    with col3:
        evaluacion = st.slider("Evaluación (1-10)", 1, 10, 7)
    comentario = st.text_area("Comentario (opcional)")
    enviar = st.form_submit_button("Registrar")

    if enviar and persona:
        nueva_fila = pd.DataFrame([{
            "Persona": persona.strip().title(),
            "Área": area,
            "Evaluación": evaluacion,
            "Comentario": comentario.strip(),
            "Fecha": datetime.today().strftime("%Y-%m-%d")
        }])
        st.session_state.dots = pd.concat([st.session_state.dots, nueva_fila], ignore_index=True)
        st.success(f"Evaluación registrada para {persona.strip().title()}")

# Visualización del historial
st.subheader("📋 Historial de evaluaciones")
st.dataframe(st.session_state.dots, use_container_width=True)

# Agrupado por persona y área (promedios)
if not st.session_state.dots.empty:
    st.subheader("📊 Credibilidad promedio por persona y área")
    resumen = st.session_state.dots.groupby(["Persona", "Área"]).agg(
        Promedio_Evaluación=("Evaluación", "mean"),
        Evaluaciones=("Evaluación", "count")
    ).reset_index()
    resumen["Promedio_Evaluación"] = resumen["Promedio_Evaluación"].round(2)
    st.dataframe(resumen, use_container_width=True)

# Botón para reiniciar
if st.button("🔄 Reiniciar todos los registros"):
    st.session_state.dots = pd.DataFrame(columns=["Persona", "Área", "Evaluación", "Comentario", "Fecha"])
