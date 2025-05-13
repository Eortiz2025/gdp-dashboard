import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Proyección de Compras con Stock", layout="wide")
st.title("📦 Proyección de Compra para Mayo 2025 con Factor Ponderado")

# Subir archivos
ventas_file = st.file_uploader("📂 Sube el archivo de ventas mensuales (2023 a abril 2025)", type=["xlsx"])
stock_file = st.file_uploader("📂 Sube el archivo de stock actual", type=["xlsx"])

if ventas_file and stock_file:
    # Leer archivos
    df_ventas = pd.read_excel(ventas_file)
    df_stock = pd.read_excel(stock_file)

    # Estandarizar columnas clave
    df_ventas["Codigo"] = df_ventas["Codigo"].astype(str)
    df_stock["Código"] = df_stock["Código"].astype(str)

    # Calcular promedios históricos ene–abr
    df_ventas["Prom_ene"] = (df_ventas["2301"] + df_ventas["2401"]) / 2
    df_ventas["Prom_feb"] = (df_ventas["2302"] + df_ventas["2402"]) / 2
    df_ventas["Prom_mar"] = (df_ventas["2303"] + df_ventas["2403"]) / 2
    df_ventas["Prom_abr"] = (df_ventas["2304"] + df_ventas["2404"]) / 2
    df_ventas["Prom_mar_abr"] = df_ventas["Prom_mar"] + df_ventas["Prom_abr"]

    # Ventas reales de 2025
    df_ventas["Ene_25"] = df_ventas["2501"]
    df_ventas["Feb_25"] = df_ventas["2502"]
    df_ventas["Mar_Abr_25"] = df_ventas["2503"] + df_ventas["2504"]

    # Calcular factores individuales
    df_ventas["Fac_ene"] = df_ventas["Ene_25"] / df_ventas["Prom_ene"]
    df_ventas["Fac_feb"] = df_ventas["Feb_25"] / df_ventas["Prom_feb"]
    df_ventas["Fac_mar_abr"] = df_ventas["Mar_Abr_25"] / df_ventas["Prom_mar_abr"]

    # Factor ponderado acumulado: Ene (1), Feb (1.5), Mar+Abr (2.5)
    df_ventas["FactorPonderado"] = (
        df_ventas["Fac_ene"] * 1 + df_ventas["Fac_feb"] * 1.5 + df_ventas["Fac_mar_abr"] * 2.5
    ) / 5

    # Calcular promedio histórico mayo y proyección mayo 2025
    df_ventas["Prom_may"] = (df_ventas["2305"] + df_ventas["2405"]) / 2
    df_ventas["Proy_May_2025"] = (df_ventas["Prom_may"] * df_ventas["FactorPonderado"]).round()

    # Inventario objetivo = 2 meses de proyección
    df_ventas["Inv_2meses"] = df_ventas["Proy_May_2025"] * 2

    # Unir con stock
    df_stock = df_stock.rename(columns={"Código": "Codigo"})
    df_resultado = df_ventas.merge(df_stock, on="Codigo", how="left")

    # Asegurar que Stock sea numérico
    df_resultado["Stock"] = pd.to_numeric(df_resultado["Stock"], errors="coerce").fillna(0)

    # Calcular compra sugerida
    df_resultado["CompraSugerida"] = (df_resultado["Inv_2meses"] - df_resultado["Stock"]).clip(lower=0).round()

    # Mostrar resultados clave
    columnas_mostrar = ["Codigo", "Nombre", "Proy_May_2025", "Inv_2meses", "Stock", "CompraSugerida"]
    st.dataframe(df_resultado[columnas_mostrar])

    # Botón de descarga
    output = io.BytesIO()
    df_resultado.to_excel(output, index=False)
    st.download_button(
        label="📥 Descargar Excel con Resultados",
        data=output.getvalue(),
        file_name="Proyeccion_Compra_Mayo_con_Stock.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("🔄 Por favor sube ambos archivos para comenzar.")
