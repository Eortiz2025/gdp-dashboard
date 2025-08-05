import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Reporte completo por paquete", layout="centered")
st.title("📦 Reporte Final por Paquete Educativo")

archivo = st.file_uploader("📎 Sube el archivo (.xls o .xlsx)", type=["xls", "xlsx"])

if archivo:
    try:
        # Leer archivo según extensión
        if archivo.name.endswith(".xlsx"):
            df = pd.read_excel(archivo)
        elif archivo.name.endswith(".xls"):
            df = pd.read_html(archivo)[0]
        else:
            raise ValueError("Formato no compatible")

        # Normalizar columnas
        df.columns = [col.strip().upper() for col in df.columns]
        requeridas = {"GRADO", "NIVEL EDUCATIVO", "FECHA ENTREGA"}
        if not requeridas.issubset(df.columns):
            raise ValueError("El archivo debe contener las columnas: GRADO, NIVEL EDUCATIVO, FECHA ENTREGA")

        # Clasificar paquete
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

        # Convertir fecha (manejar errores)
        df["FECHA ENTREGA"] = pd.to_datetime(df["FECHA ENTREGA"], errors="coerce", dayfirst=True)
        df["FECHA"] = df["FECHA ENTREGA"].dt.date

        # Dividir registros
        df_validos = df[df["FECHA"].notna()]
        df_sin_fecha = df[df["FECHA"].isna()]

        ### 📅 AGRUPAR POR FECHA
        agrupado_fecha = (
            df_validos
            .groupby(["FECHA", "PAQUETE"])
            .size()
            .reset_index(name="CANTIDAD")
            .pivot(index="FECHA", columns="PAQUETE", values="CANTIDAD")
            .fillna(0).astype(int)
        )
        agrupado_fecha["TOTAL"] = agrupado_fecha.sum(axis=1)
        agrupado_fecha.loc["TOTAL GENERAL"] = agrupado_fecha.sum()

        ### ❓ AGRUPAR SIN FECHA
        if not df_sin_fecha.empty:
            sin_fecha = df_sin_fecha["PAQUETE"].value_counts().sort_index().to_frame().T
            sin_fecha.index = ["SIN FECHA"]
            sin_fecha["TOTAL"] = sin_fecha.sum(axis=1)
        else:
            sin_fecha = pd.DataFrame({"Mensaje": ["Todos los registros tienen fecha."]})

        ### 📦 TOTAL COMBINADO (OPCIONAL)
        total_por_paquete = df["PAQUETE"].value_counts().sort_index().to_frame().T
        total_por_paquete.index = ["TOTAL ABSOLUTO"]
        total_por_paquete["TOTAL"] = total_por_paquete.sum(axis=1)

        # Mostrar resultados
        st.subheader("📊 Ventas por Fecha y Paquete")
        st.dataframe(agrupado_fecha)

        if not df_sin_fecha.empty:
            st.subheader("⚠️ Registros sin fecha")
            st.dataframe(sin_fecha)

        st.subheader("🔢 Total absoluto por Paquete")
        st.dataframe(total_por_paquete)

        ### 📁 EXPORTAR A EXCEL
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            agrupado_fecha.to_excel(writer, sheet_name="Por_Fecha")
            sin_fecha.to_excel(writer, sheet_name="Sin_Fecha")
            total_por_paquete.to_excel(writer, sheet_name="Totales_Globales")
        buffer.seek(0)

        st.download_button(
            label="⬇️ Descargar Excel completo",
            data=buffer,
            file_name="reporte_final_paquetes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("📂 Sube un archivo para generar el reporte.")
