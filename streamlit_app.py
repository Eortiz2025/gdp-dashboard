import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Reporte por paquete", layout="centered")
st.title("📦 Reporte de Ventas por Paquete Educativo")

archivo = st.file_uploader("📎 Sube el archivo de entregas (.xls o .xlsx)", type=["xls", "xlsx"])

if archivo:
    try:
        # Leer archivo según extensión
        if archivo.name.endswith(".xlsx"):
            df = pd.read_excel(archivo)
        elif archivo.name.endswith(".xls"):
            df = pd.read_html(archivo)[0]
        else:
            raise ValueError("Formato no compatible")

        # Normalizar nombres de columnas
        df.columns = [col.strip().upper() for col in df.columns]

        # Verificar columnas requeridas
        requeridas = {"FECHA ENTREGA", "GRADO", "NIVEL EDUCATIVO"}
        if not requeridas.issubset(set(df.columns)):
            raise ValueError("Faltan columnas requeridas: FECHA ENTREGA, GRADO, NIVEL EDUCATIVO")

        # Procesar fechas
        df["FECHA ENTREGA"] = pd.to_datetime(df["FECHA ENTREGA"], errors="coerce", dayfirst=True)
        df["FECHA"] = df["FECHA ENTREGA"].dt.date

        # Clasificación por paquete
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

        # 🔍 Verificación rápida
        st.write("✅ Total filas cargadas:", len(df))
        st.write("🧾 Vista previa de los datos:", df[["FECHA", "GRADO", "NIVEL EDUCATIVO", "PAQUETE"]].head())

        # Agrupar y pivotear
        ventas = df.groupby(["FECHA", "PAQUETE"]).size().reset_index(name="VENTAS")
        reporte = ventas.pivot(index="FECHA", columns="PAQUETE", values="VENTAS").fillna(0).astype(int)
        reporte["TOTAL"] = reporte.sum(axis=1)

        # Fila total general
        total = reporte.sum(axis=0).to_frame().T
        total.index = ["TOTAL GENERAL"]
        reporte_final = pd.concat([reporte, total])

        # Mostrar
        st.subheader("📊 Resumen por Paquete")
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
