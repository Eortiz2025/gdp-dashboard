import streamlit as st
import pandas as pd

st.set_page_config(page_title="Proyección de Compras 2025", layout="wide")
st.title("📊 Proyección de Compras Mayo-Diciembre 2025")

# Subir archivo
archivo = st.file_uploader("Sube tu archivo Excel con ventas (formato: código, nombre, 2301 ... 2504)", type=["xlsx"])

if archivo:
    df = pd.read_excel(archivo)
    st.success("Archivo cargado correctamente.")

    # Verifica columnas esperadas
    columnas_validas = ["codigo", "nombre"] + [f"{a}{b:02}" for a in range(23, 26) for b in range(1, 13)]
    columnas_validas = columnas_validas[:len(df.columns)]  # solo las necesarias
    df.columns = columnas_validas

    # Tomamos enero-abril de 2023, 2024 y 2025
    cols_2023 = [f"23{m:02}" for m in range(1, 13)]
    cols_2024 = [f"24{m:02}" for m in range(1, 13)]
    cols_2025 = [f"25{m:02}" for m in range(1, 5)]  # hasta abril

    resultados = []

    for _, row in df.iterrows():
        codigo = row["codigo"]
        nombre = row["nombre"]
        ventas_2023 = [row[col] for col in cols_2023]
        ventas_2024 = [row[col] for col in cols_2024]
        ventas_2025 = [row[col] for col in cols_2025]

        promedio_2023_2024 = [(v2023 + v2024) / 2 for v2023, v2024 in zip(ventas_2023[:4], ventas_2024[:4])]
        factor_caida = sum([v2025 / p if p > 0 else 1 for v2025, p in zip(ventas_2025, promedio_2023_2024)]) / 4

        for mes in range(5, 13):  # mayo a diciembre
            base = (ventas_2023[mes - 1] + ventas_2024[mes - 1]) / 2
            proyeccion = round(base * factor_caida)
            stock_seg = round(proyeccion * 0.15)
            compra = round(proyeccion + stock_seg)

            resultados.append({
                "codigo": codigo,
                "nombre": nombre,
                "mes": f"25{mes:02}",
                "proyeccion": proyeccion,
                "stock_seguridad": stock_seg,
                "compra_sugerida": compra
            })

    df_resultado = pd.DataFrame(resultados)
    st.subheader("📦 Compras sugeridas por producto (may-dic 2025)")
    st.dataframe(df_resultado, use_container_width=True)

    # Descargar como Excel
    output_excel = df_resultado.pivot_table(index=["codigo", "nombre"], 
                                            columns="mes", 
                                            values="compra_sugerida", 
                                            fill_value=0).reset_index()

    st.download_button("Descargar Excel de compras sugeridas", 
                       output_excel.to_excel(index=False, engine="openpyxl"), 
                       file_name="compras_sugeridas_2025.xlsx")
