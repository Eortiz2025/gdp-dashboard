import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Reporte por paquete con fechas", layout="centered")
st.title("📦 Reporte por Paquete Educativo (agrupado por fecha si es posible)")

archivo = st.file_uploader("📎 Sube el archivo (.xls o .xlsx)", type=["xls", "xlsx"])

if archivo:
    try:
        # Leer archivo
        if archivo.name.endswith(".xlsx"):
            df = pd.read_excel(archivo)
        elif archivo.name.endswith(".xls"):
            df = pd.read_html(archivo)[0]
        else:
            raise ValueError("Formato no compatible")

        # Normalizar columnas
        df.columns = [col.strip().upper() for col in df.columns]
        requeridas = {"GRADO", "NIVEL EDUCATIVO", "FECHA ENTREGA"}
        if not requeridas.issubset(set(df.columns)):
            raise ValueError("Faltan columnas: GRADO, NIVEL EDUCATIVO, FECHA ENTREGA")

        st.write("✅ Filas totales cargadas:", len(df))

        # Clasificar paquetes
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

        # Procesar fechas válidas
        df["FECHA ENTREGA"] = pd.to_datetime(df["FECHA ENTREGA"], errors="coerce", dayfirst=True)
        df["FECHA"] = df["FECHA ENTREGA"].dt.date

        # Separar válidos y sin fecha
        df_validas = df[df["FECHA"].notna()]
        df_sin_fecha = df[df["FECHA"].isna()]

        # Agrupar por fecha
        ventas_fecha = df_validas.groupby(["FECHA", "PAQUETE"]).size().reset_index(name="VENTAS")
        tabla = ventas_fecha.pivot(index="FECHA", columns="PAQUETE", values="VENTAS").fillna(0).astype(int)
        tabla["TOTAL"] = tabla.sum(axis=1)

        # Fila total general
        total = tabla.sum(axis=0).to_frame().T
        total.index = ["TOTAL GENERAL"]
        tabla_final = pd.concat([tabla, total])

        st.subheader("📆 Ventas agrupadas por fecha")
        st.dataframe(tabla_final)

        # Mostrar si hubo registros sin fecha
        if not df_sin_fecha.empty:
            st.warning(f"⚠️ {len(df_sin_fecha)} registros no tienen fecha y no se incluyeron en el agrupamiento.")

            resumen_sin_fecha = df_sin_fecha["PAQUETE"].value_counts().sort_index().to_frame(name="SIN FECHA").T
            st.subheader("🕘 Registros sin fecha agrupados por paquete")
            st.dataframe(resumen_sin_fecha)

        # Descargar Excel
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            tabla_final.to_excel(writer, sheet_name="Por_Fecha")
            if not df_sin_fecha.empty:
                resumen_sin_fecha.to_excel(writer, sheet_name="Sin_Fecha")
        buffer.seek(0)

        st.download_button(
            label="⬇️ Descargar Excel completo",
            data=buffer,
            file_name="reporte_paquetes_con_fechas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")

else:
    st.info("📂 Sube un archivo para generar el reporte por fecha y paquete.")
