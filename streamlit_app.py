import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="4DX Dashboard", layout="centered")
st.title("📊 Tablero de Ejecución 4DX")

# Datos de ejemplo iniciales
data = {
    "Meta Crucialmente Importante": [
        "Aumentar satisfacción del cliente",
        "Incrementar ventas trimestrales"
    ],
    "Medida Histórica": ["NPS mensual", "Ventas mensuales"],
    "Medidas Predictivas": ["# de seguimientos post-venta", "# de llamadas de venta semanales"],
    "Meta": [80, 15000],
    "Resultado Actual": [65, 12000],
}
df = pd.DataFrame(data)

def calcular_avance(actual, meta):
    return round((actual / meta) * 100 if meta > 0 else 0, 2)

# Calcular avance
df["% Avance"] = df.apply(lambda row: calcular_avance(row["Resultado Actual"], row["Meta"]), axis=1)

# Mostrar dashboard
st.subheader("Resumen de Metas Clave")
st.dataframe(df, use_container_width=True)

# Formulario para actualizar resultados
st.subheader("🔄 Actualizar Resultados")
with st.form("update_form"):
    objetivo = st.selectbox("Selecciona la meta a actualizar", df["Meta Crucialmente Importante"])
    nuevo_valor = st.number_input("Nuevo resultado actual", min_value=0, step=1)
    submitted = st.form_submit_button("Actualizar")

    if submitted:
        idx = df[df["Meta Crucialmente Importante"] == objetivo].index[0]
        df.at[idx, "Resultado Actual"] = nuevo_valor
        df["% Avance"] = df.apply(lambda row: calcular_avance(row["Resultado Actual"], row["Meta"]), axis=1)
        st.success("Resultado actualizado.")
        st.dataframe(df, use_container_width=True)

# Nota visual
st.markdown("""
<style>
    .stDataFrame th, .stDataFrame td {
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

st.info("Este dashboard está basado en la Disciplina 3 de 4DX: Crear un tablero de resultados convincente. Puedes integrarlo con más disciplinas como seguimiento semanal (Disciplina 4).")
