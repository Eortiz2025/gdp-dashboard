import streamlit as st
import pandas as pd

st.set_page_config(page_title="Decisiones estilo Dalio", layout="centered")

st.title("📊 Sistema de Decisiones Ponderadas - Estilo Ray Dalio")

st.markdown("""
Este sistema te ayuda a tomar decisiones basadas en opiniones **ponderadas por credibilidad**.
""")

st.subheader("Paso 1: Ingresar opiniones")

# Inicializar la tabla en sesión si no existe
if "tabla_opiniones" not in st.session_state:
    st.session_state.tabla_opiniones = pd.DataFrame(columns=["Persona", "Opinión (1-10)", "Credibilidad (1-10)"])

# Formulario de entrada
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
        nueva_fila = pd.DataFrame({
            "Persona": [persona],
            "Opinión (1-10)": [opinion],
            "Credibilidad (1-10)": [cred]
        })
        st.session_state.tabla_opiniones = pd.concat([st.session_state.tabla_opiniones, nueva_fila], ignore_index=True)

# Mostrar tabla con Ponderado
df = st.session_state.tabla_opiniones.copy()
if not df.empty:
    df["Ponderado"] = df["Opinión (1-10)"] * df["Credibilidad (1-10)"]
st.write("### Opiniones Registradas")
st.dataframe(df, use_container_width=True)

# Calcular resultado si hay datos
if not df.empty:
    st.subheader("Paso 2: Resultado de la decisión")

    total_ponderado = df["Ponderado"].sum()
    total_credibilidad = df["Credibilidad (1-10)"].sum()

    resultado = round(total_ponderado / total_credibilidad, 2) if total_credibilidad > 0 else 0

    st.metric(label="Promedio Ponderado de la Decisión", value=resultado)

    # Interpretación visual estilo semáforo
    if resultado < 5.0:
        mensaje = "🔴 Opinión mayormente negativa o con baja confianza."
    elif resultado < 7.0:
        mensaje = "🟡 Opiniones divididas, falta consenso. Requiere discusión."
    elif resultado < 9.0:
        mensaje = "🟢 Hay buena confianza en la decisión."
    else:
        mensaje = "✅ Consenso claro y muy alta confianza."

    st.info(f"**Interpretación:** {mensaje}")

    with st.expander("Ver cálculo detallado"):
        st.write(df)

# Botón para reiniciar
if st.button("🔄 Reiniciar tabla"):
    st.session_state.tabla_opiniones = pd.DataFrame(columns=["Persona", "Opinión (1-10)", "Credibilidad (1-10)"])
