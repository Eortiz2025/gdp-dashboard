import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Reporte completo por paquete", layout="centered")
st.title("📦 Reporte Paquete Escolares")

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

        st.write("✅ Filas totales cargadas:", len(df))

        # Clasificar paquete (ajustada según nueva lógica)
        def clasificar_paquete(row):
            nivel = str(row["NIVEL EDUCATIVO"]).upper()
            grado = row["GRADO"]
            if nivel == "PREESCOLAR":
                return "Paq1"
            elif nivel == "PRIMARIA" and grado in [1, 2]:
                return "Paq2"
            elif nivel == "PRIMARIA" and grado in [3, 4, 5, 6]:
                return "Paq3"
            elif nivel == "SECUNDARIA":
                return "Paq4"
            else:
                return "Otro"

        df["PAQUETE"] = df.apply(clasificar_paquete, axis=1)

        # 🛠 EXTRAER SOLO FECHA
        df["FECHA ENTREGA"] = (
            df["FECHA ENTREGA"]
            .astype(str)
            .str.replace("a. m.", "AM", regex=False)
            .str.replace("p. m.", "PM", regex=False)
            .str.extract(r"(\d{2}/\d{2}/\d{4})")[0]
        )

        df["FECHA ENTREGA"] = pd.to_datetime(df["FECHA ENTREGA"], errors="coerce", dayfirst=True)
        df["FECHA"] = df["FECHA ENTREGA"].dt.date

        # Dividir registros válidos e inválidos
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

        ### 📦 TOTAL ABSOLUTO + META
        conteo = df["PAQUETE"].value_counts().sort_index()
        total_por_paquete = conteo.to_frame().T
        total_por_paquete.index = ["TOTAL ABSOLUTO"]
        total_por_paquete["TOTAL"] = total_por_paquete.sum(axis=1)

        # Agregar metas y % de avance
        metas = {"Paq1": 500, "Paq2": 950, "Paq3": 2450, "Paq4": 2100}
        avance = {}
        for col in metas:
            if col in total_por_paquete.columns:
                vendidos = total_por_paquete.at["TOTAL ABSOLUTO", col]
                avance[col] = f"{(vendidos / metas[col]) * 100:.1f}%"
            else:
                avance[col] = "0%"

        metas_row = {**metas, "TOTAL": sum(metas.values())}
        avance_row = {**avance, "TOTAL": ""}

        tabla_totales = pd.concat([
            total_por_paquete,
            pd.DataFrame([metas_row], index=["META"]),
            pd.DataFrame([avance_row], index=["% AVANCE"])
        ])

        # Mostrar resultados
        st.subheader("📊 Ventas por Fecha y Paquete")
        st.dataframe(agrupado_fecha)

        if not df_sin_fecha.empty:
            st.subheader("⚠️ Registros sin fecha")
            st.dataframe(sin_fecha)

        st.subheader("🎯 Total , Meta y % Avance")
        st.dataframe(tabla_totales)

        ### 📁 EXPORTAR A EXCEL
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            agrupado_fecha.to_excel(writer, sheet_name="Por_Fecha")
            sin_fecha.to_excel(writer, sheet_name="Sin_Fecha")
            tabla_totales.to_excel(writer, sheet_name="Totales_Globales")
        buffer.seek(0)

        st.download_button(
            label="⬇️ Descargar Excel completo",
            data=buffer,
            file_name="reporte_final_con_metas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")

else:
    st.info("📂 Sube un archivo para generar el reporte.")
