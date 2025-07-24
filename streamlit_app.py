import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Archivo de datos
FACTURAS_FILE = "facturas.xlsx"
PAGOS_FILE = "pagos.xlsx"

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
    "Estado de cuenta por cliente",
    "Exportar a Excel"
])

if menu == "Registrar nueva factura":
    st.header("🧾 Nueva factura")
    with st.form("factura_form"):
        fecha = st.date_input("Fecha", value=datetime.today())
        cliente = st.text_input("Cliente")
        num_fact = st.text_input("Número de Factura")
        importe = st.number_input("Importe", min_value=0.01)
        notas = st.text_area("Notas")
        guardar = st.form_submit_button("Guardar")

    if guardar:
        nueva_factura = pd.DataFrame([[fecha, cliente, num_fact, importe, notas]],
                                     columns=df_facturas.columns)
        df_facturas = pd.concat([df_facturas, nueva_factura], ignore_index=True)
        df_facturas.to_excel(FACTURAS_FILE, index=False)
        st.success("Factura guardada correctamente.")

elif menu == "Registrar pago":
    st.header("💵 Registrar pago")
    facturas_pendientes = df_facturas["No. Factura"].unique().tolist()
    with st.form("pago_form"):
        factura = st.selectbox("Número de Factura", facturas_pendientes)
        fecha_pago = st.date_input("Fecha de pago", value=datetime.today())
        importe_pagado = st.number_input("Importe pagado", min_value=0.01)
        metodo = st.selectbox("Método de pago", ["Efectivo", "Transferencia", "Tarjeta", "Otro"])
        registrar = st.form_submit_button("Registrar pago")

    if registrar:
        nuevo_pago = pd.DataFrame([[factura, fecha_pago, importe_pagado, metodo]],
                                  columns=df_pagos.columns)
        df_pagos = pd.concat([df_pagos, nuevo_pago], ignore_index=True)
        df_pagos.to_excel(PAGOS_FILE, index=False)
        st.success("Pago registrado correctamente.")

elif menu == "Estado de cuenta por cliente":
    st.header("📄 Estado de cuenta")
    clientes = df_facturas["Cliente"].unique().tolist()
    cliente_sel = st.selectbox("Selecciona un cliente", clientes)

    facturas_cliente = df_facturas[df_facturas["Cliente"] == cliente_sel]
    pagos_cliente = df_pagos[df_pagos["No. Factura"].isin(facturas_cliente["No. Factura"])]

    st.subheader("Facturas")
    st.dataframe(facturas_cliente)

    st.subheader("Pagos")
    st.dataframe(pagos_cliente)

    resumen = facturas_cliente.copy()
    resumen["Pagado"] = resumen["No. Factura"].apply(
        lambda x: pagos_cliente[pagos_cliente["No. Factura"] == x]["Importe Pagado"].sum()
    )
    resumen["Saldo"] = resumen["Importe"] - resumen["Pagado"]
    st.subheader("Resumen")
    st.dataframe(resumen[["No. Factura", "Importe", "Pagado", "Saldo"]])

elif menu == "Exportar a Excel":
    st.header("📤 Exportar datos")
    st.download_button("Descargar Facturas", data=df_facturas.to_csv(index=False), file_name="facturas.csv")
    st.download_button("Descargar Pagos", data=df_pagos.to_csv(index=False), file_name="pagos.csv")
    st.success("Archivos preparados para descarga.")
