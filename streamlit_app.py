import streamlit as st
import pandas as pd

st.set_page_config(page_title="Proyección Estacional Ajustada 2025", layout="wide")
st.title("📦 Proyección de Compras Mayo–Diciembre 2025 (Estacional + Ajuste Real)")

archivo = st.file_uploader("Sube un archivo .CSV con columnas: codigo, producto, 2301 ... 2504", type=["csv"])

if archivo:
    try:
        df = pd.read_csv(archivo)

        st.success("✅ Archivo cargado correctamente.")
        columnas_requeridas = ["codigo", "producto"] + [f"23{m:02}" for m in range(1, 13)] + [f"24{m:02}" for m in range(1, 13)] + [f"25{m:02}" for m in range(1, 5)]
        faltantes = [col for col in columnas_requeridas if col not in df.columns]

        if faltantes:
            st.error(f"❌ Faltan columnas requeridas: {faltantes}")
            st.stop()

        resultados = []

        for _, row in df.iterrows():
            codigo = row["codigo"]
            producto = row["producto"]

            v2023 = [row[f"23{m:02}"] for m in range(1, 13)]
            v2024 = [row[f"24{m:02}"] for m in range(1, 13)]
            v2025 = [row[f"25{m:02}"] for m in range(1, 5)]  # ene a abr

            prom_hist = [(x + y) / 2 for x, y in zip(v2023[:4], v2024[:4])]
            factor_caida = sum([v / p if p > 0 else 1 for v, p in zip(v2025, prom_hist)]) / 4

            for i, mes in enumerate(range(5, 13)):  # mayo-diciembre
                base = (v2023[mes - 1] + v2024[mes - 1]) / 2
                proy = round(base * factor_caida)
                seguridad = round(proy * 0.15)
                compra = proy + seguridad

                resultados.append({
                    "Codigo": codigo,
                    "Producto": producto,
                    "Mes": f"25{mes:02}",
                    "Proyección Estacional Ajustada": proy,
                    "Stock Seguridad (15%)": seguridad,
                    "Compra Sugerida": compra
                })

        df_resultado = pd.DataFrame(resultados)

        st.subheader("📊 Compras Sugeridas 2025 (may-dic)")
        st.dataframe(df_resultado, use_container_width=True)

        # Descargar Excel
        excel = df_resultado.to_excel(index=False, engine="openpyxl")
        st.download_button("📥 Descargar Excel", data=excel, file_name="compras_2025_estacional.xlsx")

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
