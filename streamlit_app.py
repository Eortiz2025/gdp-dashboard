import streamlit as st
import pandas as pd
from datetime import date
import os

# Nombre del archivo para guardar los datos
DATA_FILE = "habitos.csv"

# Lista de hábitos (orden alfabético)
habits = ["Camina", "Escribe", "Estira", "Lee", "Medita", "Respira", "Tapping"]

# Cargar datos existentes o crear nuevo DataFrame
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE, parse_dates=["Fecha"])
else:
    df = pd.DataFrame(columns=["Fecha"] + habits)

st.title("🧘 Seguimiento Diario de Hábitos")

# Fecha seleccionada
selected_date = st.date_input("Selecciona la fecha", date.today())

# Entrada existente
existing_entry = df[df["Fecha"] == pd.Timestamp(selected_date)]

# Checkboxes
st.subheader("Marca los hábitos que cumpliste hoy:")
habit_status = {}
for habit in habits:
    default_val = False
    if not existing_entry.empty:
        default_val = existing_entry.iloc[0][habit]
    habit_status[habit] = st.checkbox(habit, value=default_val)

# Botón guardar
if st.button("Guardar"):
    new_row = {"Fecha": selected_date}
    new_row.update(habit_status)
    df = df[df["Fecha"] != pd.Timestamp(selected_date)]  # elimina entrada previa
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
