import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Compras con MLE", page_icon="📈")
st.title("📦 Planificador de Compras con MLE")

st.markdown("Sube un archivo con las ventas mensuales históricas de productos. Luego, puedes subir solo los productos que se están vendiendo este mes con sus cantidades e inventario actual, y el sistema calculará cuánto deberías comprar usando el modelo de Máxima Verosimilitud (MLE).")

# Subir archivo principal con ventas históricas
archivo_hist = st.file_uploader("🗂️ Archivo de ventas históricas (Excel o CSV)", type=["xlsx", "csv"])

# Subir archivo mensual actual (sólo productos activos del mes)
archivo_mes = st.file_uploader("📆 Archivo de ventas e inventario del mes actual (sólo productos a calcular)", type=["xlsx", "csv"])

# Ingresar días efectivos del mes actual
dias_efectivos = st.number_input("🕒 Días útiles de venta del mes actual", min_value=1, max_value=31, value=26)

if archivo_hist and archivo_mes:
    try:
        # Cargar histórico
        if archivo_hist.name.endswith(".csv"):
            df_hist = pd.read_csv(archivo_hist)
        else:
            df_hist = pd.read_excel(archivo_hist)

        # Cargar mes actual
        if archivo_mes.name.endswith(".csv"):
            df_mes = pd.read_csv(archivo_mes)
        else:
            df_mes = pd.read_excel(archivo_mes)

        # Validaciones mínimas
        if not {'Producto', 'Mes', 'Ventas'}.issubset(df_hist.columns):
            st.error("El archivo histórico debe tener columnas: Producto, Mes, Ventas")
            st.stop()

        if not {'Producto', 'Cantidad vendida', 'Stock (total)'}.issubset(df_mes.columns):
            st.error("El archivo del mes debe tener columnas: Producto, Cantidad vendida, Stock (total)")
            st.stop()

        # Filtrar histórico para solo productos activos este mes
        productos_mes = df_mes['Producto'].unique()
        df_hist = df_hist[df_hist['Producto'].isin(productos_mes)]

        # Agrupar histórico por producto
        df_hist['DiasMes'] = df_hist['Mes'].apply(lambda x: 30 if 'abr' in x.lower() else 31)
        df_grouped = df_hist.groupby('Producto').agg({
            'Ventas': 'sum',
            'DiasMes': 'sum'
        }).reset_index()

        df_grouped['LambdaMLE'] = df_grouped['Ventas'] / df_grouped['DiasMes']
        df_grouped = df_grouped.merge(df_mes, on='Producto', how='left')

        df_grouped['Cantidad vendida'] = df_grouped['Cantidad vendida'].fillna(0)
        df_grouped['Stock (total)'] = df_grouped['Stock (total)'].fillna(0)

        df_grouped['DemandaEsperada'] = df_grouped['LambdaMLE'] * dias_efectivos
        df_grouped['CompraSugerida'] = (
            df_grouped['DemandaEsperada'] - df_grouped['Cantidad vendida'] - df_grouped['Stock (total)']
        ).clip(lower=0).round()

        st.success("✅ Cálculo completado. Aquí están tus compras sugeridas:")
        st.dataframe(df_grouped[['Producto', 'LambdaMLE', 'DemandaEsperada', 'Cantidad vendida', 'Stock (total)', 'CompraSugerida']])

        # Descarga
        output = df_grouped[['Producto', 'LambdaMLE', 'DemandaEsperada', 'Cantidad vendida', 'Stock (total)', 'CompraSugerida']]
        st.download_button("📥 Descargar Excel de resultados", data=output.to_csv(index=False),
                           file_name="compras_mle.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error al procesar los archivos: {e}")
