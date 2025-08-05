import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Reporte por paquete", layout="centered")
st.title("📦 Reporte de Ventas por Paquete Educativo")

archivo = st.file_uploader("📎 Sube el archivo de entregas (.xls o .xlsx)", type=["xls", "xlsx"])

if archivo:
    try:
        # Detectar extensión y cargar correctamente
        if archivo.name.endswith(".xlsx"):
            df = pd.read_excel(archivo)
        elif archivo.name.endswith(".xls"):
            df = pd.read_html(archivo)[0]
        else:
            raise ValueError("Formato de archivo no compatible")

        # Normalizar nombres de columnas
        df.columns = [col.strip().upper() for col in df.columns]

        # Verificar columnas necesarias
        if "FECHA ENTREGA" not in df.columns or "GRADO" not in df.columns or "NIVEL EDUCATIVO" not in df.columns:
            raise ValueError("El archivo no tiene las columnas necesarias: FECHA ENTREGA, GRADO, NIVEL EDUCATIVO")

        # Procesar fecha
        df["FECHA ENTREGA"] = pd.to_datetime(df["FECHA ENTREGA"], errors="coerce", dayfirst=True)
        df["FECHA"] = df["FECHA ENTREGA"].dt.date

        # Clasificar en paquetes
        def clasificar_paquete(row):
            nivel = str(row["NIVEL EDUCATIVO"]).upper()
            grado = row["GRADO"]
            if nivel == "PREESCOLAR":
                return "Paq1"
            elif nivel == "PRIMARIA" and grado in [1, 2, 3]:
                return "Paq2"
            elif nivel == "PRIMARIA" and grado in [4, 5, 6]:
                return "Paq3"
            elif nivel == "SECUNDARIA":
                return "Paq4"
            else:
                return "Otro"

        df["PAQUETE"] = df.apply(clasificar_paquete, axis=1)

        # Agrupar por fecha y paquete
        ventas = df.groupby(["FECHA", "PAQUETE"]).size().reset_index(name="VENTAS")
        reporte = ventas.pivot(index="FECHA", columns="PAQUETE", values="VENTAS").fillna(0).astype(int)
        reporte["TOTAL"] = reporte.sum(axis=1)

        # Fila TOTAL GENERAL
        total = reporte.sum(axis=0).to_frame().T
        total.index = ["TOTAL GENERAL"]
        reporte_final = pd.concat([reporte, total])

        # Mostrar resultado
        st.subheader("📊 Ventas por Paquete")
        st.dataframe(reporte_final, use_container_width=True)

        # Exportar a Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            reporte_final.to_excel(writer, sheet_name='Paquetes', index=True)
        buffer.seek(0)

        st.download_button(
            label="⬇️ Descargar Excel",
            data=buffer,
            file_name="reporte_paquetes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
else:
    st.info("📂 Sube un archivo .xls o .xlsx para generar el reporte.")
