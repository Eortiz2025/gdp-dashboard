import streamlit as st
import pandas as pd

st.set_page_config(page_title="Reporte de ventas por nivel educativo", layout="centered")

st.title("📊 Reporte de Ventas por Nivel Educativo")

# Subir archivo
archivo = st.file_uploader("📎 Sube el archivo .xls de entregas", type=["xls"])

if archivo:
    try:
        # Intentar leer como HTML (compatible con .xls viejos exportados desde sistemas)
        tablas = pd.read_html(archivo)
        df = tablas[0]

        # Procesar fechas
        df["FECHA ENTREGA"] = pd.to_datetime(df["FECHA ENTREGA"], errors="coerce", dayfirst=True)
        df["FECHA"] = df["FECHA ENTREGA"].dt.date

        # Validar existencia de columna 'NIVEL EDUCATIVO'
        if "NIVEL EDUCATIVO" in df.columns:
            # Agrupar y pivotear
            ventas = df.groupby(["FECHA", "NIVEL EDUCATIVO"]).size().reset_index(name="VENTAS")
            reporte = ventas.pivot(index="FECHA", columns="NIVEL EDUCATIVO", values="VENTAS").fillna(0).astype(int)

            # Mostrar resultados
            st.subheader("📅 Ventas por Nivel Educativo")
            st.dataframe(reporte, use_container_width=True)

            # Descargar como Excel
            excel = reporte.reset_index().to_excel(index=False, engine='openpyxl')
            st.download_button("⬇️ Descargar reporte en Excel", data=excel, file_name="reporte_ventas_niveles.xlsx")

        else:
            st.error("❌ No se encontró la columna 'NIVEL EDUCATIVO' en el archivo.")
    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
else:
    st.info("📂 Esperando que subas un archivo .xls para generar el reporte.")
