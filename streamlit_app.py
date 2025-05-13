import streamlit as st
import pandas as pd

st.set_page_config(page_title="Proyección de Compras - Método Ponderado", layout="wide")
st.title("📦 Proyección de Compra para Mayo 2025")

uploaded_file = st.file_uploader("Sube el archivo de ventas mensuales 2023-2025", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Archivo cargado correctamente.")
    
    # Asegurar que los códigos sean string
    df["Codigo"] = df["Codigo"].astype(str)

    # Calcular promedio histórico de enero a abril
    df["Prom_ene"] = (df["2301"] + df["2401"]) / 2
    df["Prom_feb"] = (df["2302"] + df["2402"]) / 2
    df["Prom_mar"] = (df["2303"] + df["2403"]) / 2
    df["Prom_abr"] = (df["2304"] + df["2404"]) / 2
    df["Prom_mar_abr"] = df["Prom_mar"] + df["Prom_abr"]

    # Ventas reales 2025
    df["Ene_25"] = df["2501"]
    df["Feb_25"] = df["2502"]
    df["Mar_Abr_25"] = df["2503"] + df["2504"]

    # Factores individuales
    df["Fac_ene"] = df["Ene_25"] / df["Prom_ene"]
    df["Fac_feb"] = df["Feb_25"] / df["Prom_feb"]
    df["Fac_mar_abr"] = df["Mar_Abr_25"] / df["Prom_mar_abr"]

    # Factor ponderado (pesos: 1, 1.5, 2.5)
    df["FactorPonderado"] = (
        df["Fac_ene"] * 1 + df["Fac_feb"] * 1.5 + df["Fac_mar_abr"] * 2.5
    ) / 5

    # Promedio histórico de mayo
    df["Prom_may"] = (df["2305"] + df["2405"]) / 2

    # Proyección de mayo 2025
    df["Proy_May_2025"] = (df["Prom_may"] * df["FactorPonderado"]).round()

    # Inventario objetivo = 2 meses
    df["Inv_2meses"] = df["Proy_May_2025"] * 2

    # Carga de stock (opcional)
    stock_col = st.selectbox("¿Tienes columna de stock actual en el archivo?", df.columns)
    if stock_col:
        df["Stock"] = df[stock_col]
        df["CompraSugerida"] = (df["Inv_2meses"] - df["Stock"]).clip(lower=0).round()
    
    # Mostrar resultados
    columnas_mostrar = ["Codigo", "Nombre", "Proy_May_2025", "Inv_2meses"]
    if "Stock" in df.columns:
        columnas_mostrar.append("Stock")
        columnas_mostrar.append("CompraSugerida")

    st.dataframe(df[columnas_mostrar])

    # Descargar resultados
    import io
    output = io.BytesIO()
    df.to_excel(output, index=False)
    st.download_button("📥 Descargar Excel con Proyección", data=output.getvalue(), file_name="Proyeccion_Compra_Mayo.xlsx")

else:
    st.warning("Por favor sube un archivo para iniciar el análisis.")
