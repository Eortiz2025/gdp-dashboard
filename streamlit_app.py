import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Reporte de ventas por nivel educativo", layout="centered")
st.title("📊 Reporte de Ventas por Nivel Educativo")

archivo = st.file_uploader("📎 Sube el archivo .xls de entregas", type=["xls"])

if archivo:
    try:
        # Leer archivo .xls como tabla HTML
        tablas = pd.read_html(archivo)
        df = tablas[0]

        # Convertir fecha
        df["FECHA ENTREGA"] = pd.to_datetime(df["FECHA ENTREGA"], errors="coerce", dayfirst=True)
        df["FECHA"] = df["FECHA ENTREGA"].dt.date

        if "NIVEL EDUCATIVO" in df.columns:
            # Agrupar y pivotear
            ventas = df.groupby(["FECHA", "NIVEL EDUCATIVO"]).size().reset_index(name="VENTAS")
            reporte = ventas.pivot(index="FECHA", columns="NIVEL EDUCATIVO", values="VENTAS").fillna(0).astype(int)

            # Agregar columna TOTAL (por día)
            reporte["TOTAL"] = reporte.sum(axis=1)

            # Agregar fila TOTAL GENERAL
            fila_total = reporte.sum(axis=0).to_frame().T
            fila_total.index = ["TOTAL GENERAL"]

            # Combinar
            reporte_final = pd.concat([reporte, fila_total])

            # Mostrar en pantalla
            st.subheader("📅 Ventas por Nivel Educativo")
            st.dataframe(reporte_final, use_container_width=True)

            # Descargar como Excel
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                reporte_final.to_excel(writer, sheet_name='Reporte', index=True)
            buffer.seek(0)

            st.download_button(
                label="⬇️ Descargar reporte en Excel",
                data=buffer,
                file_name="reporte_ventas_niveles.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        else:
            st.error("❌ No se encontró la columna 'NIVEL EDUCATIVO' en el archivo.")

    except Exception as e:
        st.error(f"Error al procesar el archivo: {str(e)}")
else:
    st.info("📂 Esperando que subas un archivo .xls para generar el reporte.")
