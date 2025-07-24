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

if menu == "Registrar nueva factura":
    st.header("🧾 Nueva factura")
    with st.form("factura_form"):
        fecha = st.date_input("Fecha", value=datetime.today())
        cliente = st.selectbox("Cliente", options=CLIENTES, index=0)
        num_fact = st.text_input("Número de Factura")
        importe = st.number_input("Importe", min_value=0.01, format="%.2f")
        notas = st.text_area("Notas")
        guardar = st.form_submit_button("Guardar")

    if guardar:
        if num_fact in df_facturas["No. Factura"].values:
            st.error("❌ Ya existe una factura con ese número.")
        else:
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
        importe_pagado = st.number_input("Importe pagado", min_value=0.01, format="%.2f")
        metodo = st.selectbox("Método de pago", ["Efectivo", "Transferencia", "Tarjeta", "Otro"])
        registrar = st.form_submit_button("Registrar pago")

    if registrar:
        nuevo_pago = pd.DataFrame([[factura, fecha_pago, importe_pagado, metodo]],
                                  columns=df_pagos.columns)
        df_pagos = pd.concat([df_pagos, nuevo_pago], ignore_index=True)
        df_pagos.to_excel(PAGOS_FILE, index=False)
        st.success("Pago registrado correctamente.")

elif menu == "Eliminar factura":
    st.header("🗑️ Eliminar factura")
    if df_facturas.empty:
        st.info("No hay facturas registradas.")
    else:
        factura_sel = st.selectbox("Selecciona la factura a eliminar", df_facturas["No. Factura"].tolist())
        if st.button("Eliminar factura"):
            df_facturas = df_facturas[df_facturas["No. Factura"] != factura_sel]
            df_facturas.to_excel(FACTURAS_FILE, index=False)
            df_pagos = df_pagos[df_pagos["No. Factura"] != factura_sel]
            df_pagos.to_excel(PAGOS_FILE, index=False)
            st.success(f"Factura {factura_sel} eliminada correctamente.")

elif menu == "Importar facturas":
    st.header("📥 Importar facturas desde archivo personalizado")
    archivo = st.file_uploader("Selecciona un archivo Excel con columnas: fecha factura, PROVEEDOR, FACTURA, IMPORTE", type=["xlsx"])
    if archivo is not None:
        try:
            df_archivo = pd.read_excel(archivo)
            columnas_esperadas = ["fecha factura", "PROVEEDOR", "FACTURA", "IMPORTE"]
            if all(col in df_archivo.columns for col in columnas_esperadas):
                df_convertido = pd.DataFrame()
                df_convertido["Fecha"] = pd.to_datetime(df_archivo["fecha factura"]).dt.date
                df_convertido["Cliente"] = df_archivo["PROVEEDOR"]
                df_convertido["No. Factura"] = df_archivo["FACTURA"].astype(str)
                df_convertido["Importe"] = df_archivo["IMPORTE"]
                df_convertido["Notas"] = ""

                existentes = df_facturas["No. Factura"].astype(str).values
                nuevas_unicas = df_convertido[~df_convertido["No. Factura"].isin(existentes)]

                df_facturas = pd.concat([df_facturas, nuevas_unicas], ignore_index=True)
                df_facturas.to_excel(FACTURAS_FILE, index=False)
                st.success(f"Se importaron {len(nuevas_unicas)} nuevas facturas correctamente.")
                st.dataframe(nuevas_unicas)
            else:
                st.error("El archivo no tiene las columnas requeridas: fecha factura, PROVEEDOR, FACTURA, IMPORTE")
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

elif menu == "Estado de cuenta por cliente":
    st.header("📄 Estado de cuenta")
    clientes = df_facturas["Cliente"].unique().tolist()
    if clientes:
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
    else:
        st.info("No hay facturas registradas aún.")

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

elif menu == "Exportar a Excel":
    st.header("📤 Exportar datos")
    st.download_button("Descargar Facturas", data=df_facturas.to_csv(index=False), file_name="facturas.csv")
    st.download_button("Descargar Pagos", data=df_pagos.to_csv(index=False), file_name="pagos.csv")
    st.success("Archivos preparados para descarga.")
