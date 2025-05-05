import streamlit as st
import pandas as pd
import numpy as np
import io
from datetime import datetime

st.set_page_config(page_title="Compras con MLE", page_icon="📈")
st.title("📦 Planificador de Compras con MLE")

st.markdown("Sube un archivo con las ventas históricas de productos (en formato por columnas mes a mes). Luego, sube sólo los productos vendidos este mes con sus cantidades e inventario actual (desde tu ERP convertido a Excel), y el sistema calculará automáticamente cuánto deberías comprar usando el modelo de Máxima Verosimilitud (MLE).")

archivo_hist = st.file_uploader("🗂️ Archivo de ventas históricas por producto (Excel o CSV)", type=["xlsx", "csv"])
archivo_mes = st.file_uploader("📆 Archivo del mes actual exportado desde ERP (convertido a Excel)", type=["xlsx"])
dias_efectivos = st.number_input("🕒 Días útiles de venta del mes actual", min_value=1, max_value=31, value=26)

if archivo_hist and archivo_mes:
    try:
        # Leer archivo histórico
        if archivo_hist.name.endswith(".csv"):
            df_hist = pd.read_csv(archivo_hist)
        else:
            df_hist = pd.read_excel(archivo_hist)

        # Leer archivo mensual desde Excel
        df_mes = pd.read_excel(archivo_mes)

        # Renombrar columnas del mes actual para que coincidan con el modelo
        df_mes = df_mes.rename(columns={
            'Codigo': 'Producto',
            'Stock': 'Stock (total)'
        })

        # Detectar nombre de columna que actúe como 'Codigo'
        codigo_col = next((col for col in df_hist.columns if col.lower().strip() in ['codigo', 'código', 'producto']), None)
        if not codigo_col:
            st.error("No se encontró una columna tipo 'Codigo' o 'Producto' en el archivo histórico.")
            st.stop()

        df_hist = df_hist.rename(columns={codigo_col: 'Producto'})

        # Convertir de formato ancho a largo
        cols_mes = [col for col in df_hist.columns if col not in ['Producto', 'Nombre']]
        df_hist = df_hist.melt(id_vars=['Producto', 'Nombre'], value_vars=cols_mes,
                               var_name='Mes', value_name='Ventas')

        # Validaciones mínimas
        if not {'Producto', 'Cantidad vendida', 'Stock (total)'}.issubset(df_mes.columns):
            st.error("El archivo del mes debe tener columnas: Producto, Cantidad vendida, Stock (total)")
            st.stop()

        productos_mes = df_mes['Producto'].unique()
        df_hist = df_hist[df_hist['Producto'].isin(productos_mes)]

        df_hist['DiasMes'] = df_hist['Mes'].apply(lambda x: 30 if str(x).lower().startswith("abr") else 31)
        df_grouped = df_hist.groupby('Producto').agg({
            'Ventas': 'sum',
            'DiasMes': 'sum'
        }).reset_index()

        df_grouped['LambdaMLE'] = df_grouped['Ventas'] / df_grouped['DiasMes']
        df_grouped = df_grouped.merge(df_mes, on='Producto', how='left')

        df_grouped['Cantidad vendida'] = pd.to_numeric(df_grouped['Cantidad vendida'], errors='coerce').fillna(0)
        df_grouped['Stock (total)'] = pd.to_numeric(df_grouped['Stock (total)'], errors='coerce').fillna(0)

        df_grouped['DemandaEsperada'] = df_grouped['LambdaMLE'] * dias_efectivos
        df_grouped['CompraSugerida'] = (
            df_grouped['DemandaEsperada'] - df_grouped['Cantidad vendida'] - df_grouped['Stock (total)']
        ).clip(lower=0).round()

        st.success("✅ Cálculo completado. Aquí están tus compras sugeridas:")
        st.dataframe(df_grouped[['Producto', 'LambdaMLE', 'DemandaEsperada', 'Cantidad vendida', 'Stock (total)', 'CompraSugerida']])

        output = df_grouped[['Producto', 'LambdaMLE', 'DemandaEsperada', 'Cantidad vendida', 'Stock (total)', 'CompraSugerida']]
        st.download_button("📥 Descargar Excel de resultados", data=output.to_csv(index=False),
                           file_name="compras_mle.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Error al procesar los archivos: {e}")
