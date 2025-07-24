import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Archivo de datos
FACTURAS_FILE = "facturas.xlsx"
PAGOS_FILE = "pagos.xlsx"

# Clientes predefinidos
CLIENTES = ["Casa Ley", "Coppel", "Chata"]

# Cargar o crear archivos
if os.path.exists(FACTURAS_FILE):
    df_facturas = pd.read_excel(FACTURAS_FILE)
else:
    df_facturas = pd.DataFrame(columns=["Fecha", "Cliente", "No. Factura", "Importe", "Notas"])

if os.path.exists(PAGOS_FILE):
    df_pagos = pd.read_excel(PAGOS_FILE)
else:
    df_pagos = pd.DataFrame(columns=["No. Factura", "Fecha de Pago", "Importe Pagado", "Método de Pago"])

st.title("📘 Control de Cuentas por Cobrar")

menu = st.sidebar.selectbox("Selecciona una opción", [
    "Registrar nueva factura",
    "Registrar pago",
    "Eliminar factura",
    "Importar facturas",
    "Estado de cuenta por cliente",
    "Reporte de antigüedad de saldos",
    "Exportar a Excel"
])

# ... las demás opciones se mantienen sin cambios ...

elif menu == "Reporte de antigüedad de saldos":
    st.header("📊 Antigüedad de saldos detallada")
    hoy = pd.to_datetime(datetime.today())
    df_facturas["Fecha"] = pd.to_datetime(df_facturas["Fecha"])

    resumen = df_facturas.copy()
    resumen["Pagado"] = resumen["No. Factura"].apply(
        lambda x: df_pagos[df_pagos["No. Factura"] == x]["Importe Pagado"].sum()
    )
    resumen["Saldo"] = resumen["Importe"] - resumen["Pagado"]
    resumen = resumen[resumen["Saldo"] > 0].copy()
    resumen["Días"] = (hoy - resumen["Fecha"]).dt.days

    resumen["Al día"] = resumen.apply(lambda row: row["Saldo"] if row["Días"] <= 0 else 0.0, axis=1)
    resumen["1 a 30"] = resumen.apply(lambda row: row["Saldo"] if 1 <= row["Días"] <= 30 else 0.0, axis=1)
    resumen["31 a 60"] = resumen.apply(lambda row: row["Saldo"] if 31 <= row["Días"] <= 60 else 0.0, axis=1)
    resumen["61 a 90"] = resumen.apply(lambda row: row["Saldo"] if 61 <= row["Días"] <= 90 else 0.0, axis=1)
    resumen["91 a 120"] = resumen.apply(lambda row: row["Saldo"] if 91 <= row["Días"] <= 120 else 0.0, axis=1)

    resumen["Fecha"] = resumen["Fecha"].dt.date

    clientes = resumen["Cliente"].unique().tolist()
    clientes.insert(0, "[Todos]")
    cliente_sel = st.selectbox("Filtrar por cliente (opcional)", clientes)

    if cliente_sel != "[Todos]":
        resumen = resumen[resumen["Cliente"] == cliente_sel]

    tabla = resumen[["Fecha", "Cliente", "No. Factura", "Importe", "Saldo", "Al día", "1 a 30", "31 a 60", "61 a 90", "91 a 120"]].copy()

    totales = pd.DataFrame({
        "Fecha": [""],
        "Cliente": [""],
        "No. Factura": ["TOTAL"],
        "Importe": [tabla["Importe"].sum()],
        "Saldo": [tabla["Saldo"].sum()],
        "Al día": [tabla["Al día"].sum()],
        "1 a 30": [tabla["1 a 30"].sum()],
        "31 a 60": [tabla["31 a 60"].sum()],
        "61 a 90": [tabla["61 a 90"].sum()],
        "91 a 120": [tabla["91 a 120"].sum()]
    })

    final_tabla = pd.concat([tabla, totales], ignore_index=True)

    for col in ["Importe", "Saldo", "Al día", "1 a 30", "31 a 60", "61 a 90", "91 a 120"]:
        final_tabla[col] = final_tabla[col].map(lambda x: f"{x:,.2f}" if pd.notnull(x) else "")

    st.dataframe(final_tabla)

    # Exportar a Excel
    export_excel = pd.concat([tabla, totales], ignore_index=True)
    export_excel_raw = export_excel.copy()
    for col in ["Importe", "Saldo", "Al día", "1 a 30", "31 a 60", "61 a 90", "91 a 120"]:
        export_excel_raw[col] = pd.to_numeric(export_excel_raw[col], errors='coerce')
    st.download_button("📥 Descargar reporte en Excel", data=export_excel_raw.to_csv(index=False), file_name="reporte_antiguedad.csv")
