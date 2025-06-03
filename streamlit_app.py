import streamlit as st
import pandas as pd
from datetime import date
import os

# Archivo de datos
DATA_FILE = "habitos.csv"

# Lista de hábitos (orden alfabético)
habits = ["Camina", "Escribe", "Estira", "Lee", "Medita", "Respira", "Tapping"]

# Cargar o crear DataFrame
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
else:
    df = pd.DataFrame(columns=["Fecha"] + habits)

st.title("🧘 Seguimiento Diario de Hábitos")

# Selección de fecha
selected_date = st.date_input("Selecciona la fecha", date.today())

# Obtener valores por defecto
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
    key = f"{habit}_{selected_date}"
    habit_status[habit] = st.checkbox(habit, value=defaults[habit], key=key)

# Guardar datos
if st.button("Guardar"):
    new_row = {"Fecha": selected_date}
    new_row.update(habit_status)

    # Eliminar entrada existente
    df = df[df["Fecha"] != pd.Timestamp(selected_date)]

    # Agregar nueva fila
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Guardar CSV
    df.to_csv(DATA_FILE, index=False)

    # Limpiar claves de sesión
    for habit in habits:
        st.session_state.pop(f"{habit}_{selected_date}", None)

    st.success("✅ Datos guardados correctamente.")

# Mostrar historial
st.subheader("📊 Historial")
if not df.empty:
    df["% Cumplimiento"] = df[habits].sum(axis=1) / len(habits) * 100
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")  # asegurar fechas válidas
    df_sorted = df.sort_values("Fecha", ascending=False)
    st.dataframe(df_sorted.style.format({"% Cumplimiento": "{:.0f}%"}))
else:
    st.info("No hay datos aún.")
