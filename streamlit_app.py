import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config("POS + Inventario", layout="centered")
st.title("📦 Control de Inventario - OlaCafe")

# --------------------------
# Cargar y guardar datos
# --------------------------
def cargar_inventario():
    if os.path.exists("inventario.csv"):
        return pd.read_csv("inventario.csv")
    else:
        return pd.DataFrame(columns=["codigo", "nombre", "precio"])

def guardar_inventario(df):
    df.to_csv("inventario.csv", index=False)

def cargar_movimientos():
    if os.path.exists("movimientos.csv"):
        return pd.read_csv("movimientos.csv")
    else:
        return pd.DataFrame(columns=["fecha", "tipo", "producto", "cantidad", "proveedor"])

def guardar_movimiento(tipo, producto, cantidad, proveedor=None):
    df = cargar_movimientos()
    nuevo = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo,
        "producto": producto,
        "cantidad": cantidad,
        "proveedor": proveedor if tipo == "entrada" else None
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv("movimientos.csv", index=False)

# --------------------------
# Inventario inicial
# --------------------------
st.subheader("📌 Inventario inicial")

inventario = cargar_inventario()
if inventario.empty:
    with st.form("inv_inicial"):
        nombre = st.text_input("Nombre del producto")
        codigo = st.text_input("Código del producto")
        precio = st.number_input("Precio", min_value=0.0)
        submitted = st.form_submit_button("Agregar producto")
        if submitted and nombre and codigo:
            nuevo = pd.DataFrame([[codigo, nombre, precio]], columns=["codigo", "nombre", "precio"])
            inventario = pd.concat([inventario, nuevo], ignore_index=True)
            guardar_inventario(inventario)
            st.success("Producto agregado.")
else:
    st.info("Inventario ya registrado. Si deseas reiniciarlo, borra 'inventario.csv'.")

# --------------------------
# Entradas (compras con proveedor)
# --------------------------
st.subheader("🟢 Registro de entradas (compras)")

producto_ent = st.selectbox("Producto comprado", inventario["nombre"], key="entrada")
cant_ent = st.number_input("Cantidad comprada", min_value=1, step=1, key="cant_ent")
proveedor = st.text_input("Proveedor")
if st.button("Registrar entrada"):
    guardar_movimiento("entrada", producto_ent, cant_ent, proveedor)
    st.success(f"Entrada registrada: {producto_ent} +{cant_ent} (Proveedor: {proveedor})")

# --------------------------
# Salidas (ventas)
# --------------------------
st.subheader("🔴 Registro de salidas (ventas)")

producto_sal = st.selectbox("Producto vendido", inventario["nombre"], key="venta")
cant_sal = st.number_input("Cantidad vendida", min_value=1, step=1, key="cant_sal")
if st.button("Registrar venta"):
    guardar_movimiento("salida", producto_sal, cant_sal)
    st.success(f"Venta registrada: {producto_sal} -{cant_sal}")

# --------------------------
# Inventario actual
# --------------------------
st.markdown("---")
st.subheader("📊 Inventario actual")

movs = cargar_movimientos()

if not movs.empty:
    resumen = movs.groupby(["producto", "tipo"])["cantidad"].sum().unstack().fillna(0)
    resumen["stock"] = resumen.get("entrada", 0) - resumen.get("salida", 0)
    resumen = resumen.reset_index().merge(inventario, left_on="producto", right_on="nombre", how="left")

    for col in ["entrada", "salida"]:
        if col not in resumen.columns:
            resumen[col] = 0

    columnas_deseadas = ["codigo", "producto", "precio", "entrada", "salida", "stock"]
    columnas_existentes = [col for col in columnas_deseadas if col in resumen.columns]
    resumen = resumen[columnas_existentes]

    if "producto" in resumen.columns:
        resumen.rename(columns={"producto": "nombre"}, inplace=True)

    # Alerta de stock bajo
    if "stock" in resumen.columns:
        bajo_stock = resumen[resumen["stock"] <= 5]
        if not bajo_stock.empty:
            st.warning("⚠️ Alerta: Productos con stock bajo")
            st.dataframe(bajo_stock)

    st.dataframe(resumen, use_container_width=True)
else:
    st.info("Aún no hay movimientos registrados.")

# --------------------------
# 💰 Resumen de ventas del día en pesos
# --------------------------
st.markdown("---")
st.subheader("💵 Total de ventas del día")

hoy = datetime.now().strftime("%Y-%m-%d")
movs["fecha"] = pd.to_datetime(movs["fecha"])
ventas_dia = movs[
    (movs["tipo"] == "salida") &
    (movs["fecha"].dt.strftime("%Y-%m-%d") == hoy)
]

if not ventas_dia.empty:
    ventas_con_precios = ventas_dia.merge(inventario, left_on="producto", right_on="nombre", how="left")
    ventas_con_precios["importe"] = ventas_con_precios["cantidad"] * ventas_con_precios["precio"]
    total = ventas_con_precios["importe"].sum()
    st.success(f"Total vendido hoy: **${total:,.2f}**")
else:
    st.info("No hay ventas registradas hoy.")

# --------------------------
# Historial de movimientos
# --------------------------
st.markdown("---")
st.subheader("📜 Historial de movimientos")

if not movs.empty:
    st.dataframe(movs.sort_values(by="fecha", ascending=False), use_container_width=True)
    csv = movs.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar historial completo", csv, file_name="movimientos.csv", mime="text/csv")
else:
    st.info("No hay movimientos registrados aún.")
