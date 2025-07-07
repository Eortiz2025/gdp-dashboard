import pandas as pd
import streamlit as st
import io

st.set_page_config(page_title="Agente de Compras", page_icon="💼")
st.title("💼 Agente de Compras")

# Subida del archivo
archivo = st.file_uploader("🗂️ Sube el archivo exportado desde Erply (.xls)", type=["xls"])

# Preguntar número de días
dias = st.text_input("⏰ ¿Cuántos días deseas calcular para VtaProm? (Escribe un número)")

# Validar número
if not dias.strip().isdigit() or int(dias) <= 0:
    st.warning("⚠️ Por favor escribe un número válido de días (mayor que 0) para continuar.")
    st.stop()

dias = int(dias)

if archivo:
    try:
        # Leer archivo
        tabla = pd.read_html(archivo, header=3)[0]
        if tabla.columns[0] in ("", "Unnamed: 0", "No", "Moneda"):
            tabla = tabla.iloc[:, 1:]

        columnas_deseadas = [
            "Código", "Código EAN", "Nombre",
            "Stock (total)", "Stock (apartado)", "Stock (disponible)",
            "Proveedor", "Cantidad vendida", "Ventas netas totales ($)",
            "Cantidad vendida (2)", "Ventas netas totales ($) (2)"
        ]

        if len(tabla.columns) >= len(columnas_deseadas):
            tabla.columns = columnas_deseadas[:len(tabla.columns)]
        else:
            st.error("❌ El archivo no tiene suficientes columnas.")
            st.stop()

        # Eliminar columnas innecesarias
        columnas_a_eliminar = [
            "Ventas netas totales ($)", "Stock (apartado)", "Stock (disponible)",
            "Ventas netas totales ($) (2)"
        ]
        tabla = tabla.drop(columns=columnas_a_eliminar)

        # Renombrar columnas según nuevo uso
        tabla = tabla.rename(columns={
            "Stock (total)": "Stock",
            "Cantidad vendida": "V30D_Actual",         # últimos 30 días reales
            "Cantidad vendida (2)": "V30D_AñoPasado"   # mismos 30 días del año pasado
        })

        # Filtrar productos sin proveedor
        tabla = tabla[tabla["Proveedor"].notna()]
        tabla = tabla[tabla["Proveedor"].astype(str).str.strip() != ""]

        # Filtrar por proveedor (opcional)
        calcular_proveedor = st.checkbox("¿Deseas calcular sólo un proveedor?", value=False)

        if calcular_proveedor:
            lista_proveedores = tabla["Proveedor"].dropna().unique()
            proveedor_seleccionado = st.selectbox("Selecciona el proveedor a calcular:", sorted(lista_proveedores))
            tabla = tabla[tabla["Proveedor"] == proveedor_seleccionado]

        # Convertir a numérico
        tabla["V30D_Actual"] = pd.to_numeric(tabla["V30D_Actual"], errors="coerce").fillna(0).round()
        tabla["V30D_AñoPasado"] = pd.to_numeric(tabla["V30D_AñoPasado"], errors="coerce").fillna(0).round()
        tabla["Stock"] = pd.to_numeric(tabla["Stock"], errors="coerce").fillna(0).round()

        # Calcular venta diaria y proyección
        tabla["VtaDiaria"] = (tabla["V30D_Actual"] / 30).round(2)
        tabla["VtaProm"] = (tabla["VtaDiaria"] * dias).round()

        # Cálculo de Max
        max_calculado = []
        for i, row in tabla.iterrows():
            if row["V30D_AñoPasado"] == 0:
                max_val = 0.5 * row["VtaProm"]
            else:
                intermedio = max(0.6 * row["V30D_AñoPasado"] + 0.4 * row["VtaProm"], row["V30D_AñoPasado"])
                max_val = min(intermedio, row["V30D_AñoPasado"] * 1.5)
            max_calculado.append(round(max_val))

        tabla["Max"] = max_calculado
        tabla["Compra"] = (tabla["Max"] - tabla["Stock"]).clip(lower=0).round()

        # Eliminar temporal
        tabla = tabla.drop(columns=["VtaDiaria"])

        # Filtrar productos con compra
        tabla = tabla[tabla["Compra"] > 0].sort_values("Nombre")

        # Mostrar proveedor (opcional)
        mostrar_proveedor = st.checkbox("¿Mostrar Proveedor?", value=False)

        if mostrar_proveedor:
            columnas_finales = [
                "Código", "Código EAN", "Nombre", "Proveedor", "Stock",
                "V30D_Actual", "VtaProm", "V30D_AñoPasado", "Max", "Compra"
            ]
        else:
            tabla = tabla.drop(columns=["Proveedor"])
            columnas_finales = [
                "Código", "Código EAN", "Nombre", "Stock",
                "V30D_Actual", "VtaProm", "V30D_AñoPasado", "Max", "Compra"
            ]

        tabla = tabla[columnas_finales]

        st.success("✅ Archivo procesado correctamente")
        st.dataframe(tabla)

        # Descargar Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            tabla.to_excel(writer, index=False, sheet_name='Compra del día')
            workbook = writer.book
            worksheet = writer.sheets['Compra del día']
            worksheet.freeze_panes = worksheet['A2']

        processed_data = output.getvalue()

        st.download_button(
            label="📄 Descargar Excel",
            data=processed_data,
            file_name="Compra del día.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Top productos donde año pasado > actual
        st.subheader("🔥 Top 10 productos donde V30D_AñoPasado supera V30D_Actual")

        productos_calientes = tabla[tabla["V30D_AñoPasado"] > tabla["V30D_Actual"]]

        if not productos_calientes.empty:
            productos_calientes = productos_calientes.sort_values("Nombre", ascending=True)
            top_productos = productos_calientes.head(10)
            columnas_a_mostrar = ["Código", "Nombre", "V30D_Actual", "VtaProm", "V30D_AñoPasado"]
            st.dataframe(top_productos[columnas_a_mostrar])
        else:
            st.info("✅ No hay productos donde V30D del año pasado supere al actual.")

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
