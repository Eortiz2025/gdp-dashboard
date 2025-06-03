import streamlit as st
import pandas as pd
from datetime import date
import os

# Archivo donde se guarda la información
DATA_FILE = "habitos.csv"

# Lista de hábitos (orden alfabético)
habits = ["Camina", "Escribe", "Estira", "Lee", "Medita", "Respira", "Tapping"]

# Cargar datos si existen
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, parse_dates=["Fecha"])
else:
    df = pd.DataFrame(columns=["Fecha"] + habits)

st.title("🧘 Seguimiento Diario de Hábitos")

# Selección de fecha
selected_date = st.date_input("Selecciona la fecha", date.today())

# Obtener valores por defecto para los checkboxes
def get_checkbox_defaults(selected_date, df, habits):
    entry = df[df["Fecha"] == pd.Timestamp(selected_date)]
    if not entry.empty:
        return {habit: bool(entry.iloc[0][habit]) for habit in habits}
    else:
        return {habit: False for habit in habits}

defaults = get_checkbox_defaults(selected_date, df, habits)

# Mostrar checkboxes
st.subheader("Marca los hábitos que cumpliste hoy:")
habit_status = {}
for habit in habits:
    habit_status[habit] = st.checkbox(habit, value=defaults[habit])

# Guardar los datos
if st.button("Guardar"):
    new_row = {"Fecha": selected_date}
    new_row.update(habit_status)
    df = df[df["Fecha"] != pd.Timestamp(selected_date)]  # Elimina entrada previa del mismo día
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("✅ Datos guardados correctamente")

# Mostrar historial
st.subheader("📊 Historial")
if not df.empty:
    df["% Cumplimiento"] = df[habits].sum(axis=1) / len(habits) * 100
    df_sorted = df.sort_values("Fecha", ascending=False)
    st.dataframe(df_sorted.style.format({"% Cumplimiento": "{:.0f}%"}))
else:
    st.info("No hay datos aún.")
