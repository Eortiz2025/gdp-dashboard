import streamlit as st
import pandas as pd

st.set_page_config(page_title="Proyección de Compras 2025", layout="wide")
st.title("📦 Proyección de Compras Mayo–Diciembre 2025 por Producto")

# Paso 1: Subir archivo CSV
archivo = st.file_uploader("Sube tu archivo .CSV con columnas: codigo, producto, 2301 ... 2504", type=["csv"])

if archivo:
    try:
        df = pd.read_csv(archivo)
        st.success("Archivo cargado correctamente.")

        # Definir columnas requeridas
        ventas_2023 = [f"23{m:02}" for m in range(1, 13)]
        ventas_2024 = [f"24{m:02}" for m in range(1, 13)]
        ventas_2025 = [f"25{m:02}" for m in range(1, 5)]  # enero a abril
        columnas_necesarias = ["Codigo", "Producto"] + ventas_2023 + ventas_2024 + ventas_2025

        # Verificar columnas faltantes
        faltantes = [col for col in columnas_necesarias if col not in df.columns]
        if faltantes:
            st.error(f"❌ Faltan columnas requeridas en el archivo: {faltantes}")
            st.stop()

        # Procesar cada fila (producto)
        resultados = []
        for _, row in df.iterrows():
            codigo = row["Codigo"]
            producto = row["Producto"]

            v2023 = [row[col] for col in ventas_2023]
            v2024 = [row[col] for col in ventas_2024]
            v2025 = [row[col] for col in ventas_2025]

            # Calcular factor de caída real
            prom_2023_2024 = [(x + y) / 2 for x, y in zip(v2023[:4], v2024[:4])]
            factor_caida = sum([
                v / p if p > 0 else 1 for v, p in zip(v2025, prom_2023_2024)
            ]) / 4

            # Generar proyección para mayo-diciembre 2025
            for i, mes in enumerate(range(5, 13)):  # meses 5 a 12
                base = (v2023[mes - 1] + v2024[mes - 1]) / 2
                proyeccion = round(base * factor_caida)
                stock_seguridad = round(proyeccion * 0.15)
                compra = proyeccion + stock_seguridad

                resultados.append({
                    "Codigo": codigo,
                    "Producto": producto,
                    "Mes": f"25{mes:02}",
                    "Proyección": proyeccion,
                    "Stock Seguridad (15%)": stock_seguridad,
                    "Compra Sugerida": compra
                })

        df_resultado = pd.DataFrame(resultados)

        st.subheader("📊 Tabla de Compras Sugeridas (2025/05 a 2025/12)")
        st.dataframe(df_resultado, use_container_width=True)

        # Opción de descarga
        csv = df_resultado.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar resultados en CSV", data=csv, file_name="compras_2025.csv", mime="text/csv")

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo: {e}")
