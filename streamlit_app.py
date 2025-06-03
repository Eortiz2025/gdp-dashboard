import streamlit as st
import pandas as pd
from datetime import date
import os

# Archivo de datos
DATA_FILE = "habitos.csv"

# Lista de hábitos
habits = ["Camina", "Escribe", "Estira", "Lee", "Medita", "Respira", "Tapping"]

# Cargar datos
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce").dt.date
else:
    df = pd.DataFrame(columns=["Fecha"] + habits)

st.title("🧘 Seguimiento Diario de Hábitos")

# Selección de fecha
selected_date = st.date_input("Selecciona la fecha", date.today())

# Obtener valores por defecto
def get_checkbox_defaults(selected_date, df, habits):
    match = df[df["Fecha"] == selected_date]
    if not match.empty:
        return {habit: bool(match.iloc[0][habit]) for habit in habits}
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
    df = df[df["Fecha"] != selected_date]
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    for habit in habits:
        st.session_state.pop(f"{habit}_{selected_date}", None)
    st.success("✅ Datos guardados correctamente.")

# Mostrar historial
st.subheader("📊 Historial")
if not df.empty:
    df["% Cumplimiento"] = df[habits].sum(axis=1) / len(habits) * 100
    df_sorted = df.sort_values("Fecha", ascending=False).copy()
    df_sorted["Fecha"] = df_sorted["Fecha"].astype(str)
    st.dataframe(df_sorted.style.format({"% Cumplimiento": "{:.0f}%"}))
else:
    st.info("No hay datos aún.")

# 🔻 Botón para borrar historial al final
st.markdown("---")
if st.button("🗑️ Borrar historial COMPLETO"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        df = pd.DataFrame(columns=["Fecha"] + habits)
        st.warning("⚠️ Historial eliminado correctamente. Refresca la página.")
