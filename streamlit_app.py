import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="4DX Dashboard", layout="centered")
st.title("📊 Dashboard de Ventas - Papelería")

# Datos de ejemplo
vendedores = ["Ana", "Luis", "Karla"]
data = {
    "Vendedor": vendedores,
    "Ticket Promedio Actual": [102, 85, 95],
    "Meta Ticket Promedio": [110, 110, 110],
    "Ofertas Sugeridas Hoy": [12, 8, 10],
    "Tickets con Combo": [6, 3, 5],
}
df = pd.DataFrame(data)

def calcular_avance(actual, meta):
    return round((actual / meta) * 100 if meta > 0 else 0, 2)

df["% Avance"] = df.apply(lambda row: calcular_avance(row["Ticket Promedio Actual"], row["Meta Ticket Promedio"]), axis=1)

# Mostrar dashboard
st.subheader("🔍 Resumen de Ticket Promedio por Vendedor")
st.dataframe(df, use_container_width=True)

# Formulario para actualizar resultados
st.subheader("✏️ Actualizar Datos de Vendedor")
with st.form("update_form"):
    vendedor = st.selectbox("Selecciona vendedor", vendedores)
    nuevo_ticket = st.number_input("Nuevo ticket promedio", min_value=0.0, step=1.0)
    nuevas_ofertas = st.number_input("Ofertas sugeridas hoy", min_value=0, step=1)
    nuevos_combos = st.number_input("Tickets con combo", min_value=0, step=1)
    submitted = st.form_submit_button("Actualizar")

    if submitted:
        idx = df[df["Vendedor"] == vendedor].index[0]
        df.at[idx, "Ticket Promedio Actual"] = nuevo_ticket
        df.at[idx, "Ofertas Sugeridas Hoy"] = nuevas_ofertas
        df.at[idx, "Tickets con Combo"] = nuevos_combos
        df["% Avance"] = df.apply(lambda row: calcular_avance(row["Ticket Promedio Actual"], row["Meta Ticket Promedio"]), axis=1)
        st.success("Datos actualizados.")
        st.dataframe(df, use_container_width=True)

st.info("Esta app sigue la metodología 4DX. La Meta Crucialmente Importante (MCI) es aumentar el ticket promedio. Las acciones predictivas son sugerencias de productos y ventas cruzadas.")
