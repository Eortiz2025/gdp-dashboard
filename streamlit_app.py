import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config("POS + Inventario", layout="centered")
st.title("📦 Control de Inventario - OlaCafe")

# --------------------------
# Cargar datos
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
        return pd.DataFrame(columns=["fecha", "tipo", "producto", "cantidad"])

def guardar_movimiento(tipo, producto, cantidad):
    df = cargar_movimientos()
    nuevo = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tipo": tipo,
        "producto": producto,
        "cantidad": cantidad
    }
    df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
    df.to_csv("movimientos.csv", index=False)

# --------------------------
# Registro de inventario inicial
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
# Entradas (compras del día)
# --------------------------
st.subheader("🟢 Registro de entradas (compras)")

inventario = cargar_inventario()
if not inventario.empty:
    producto_ent = st.selectbox("Producto comprado", inventario["nombre"])
    cant_ent = st.number_input("Cantidad comprada", min_value=1, step=1)
    if st.button("Registrar entrada"):
        guardar_movimiento("entrada", producto_ent, cant_ent)
        st.success(f"Entrada registrada: {producto_ent} +{cant_ent}")

# --------------------------
# Salidas (ventas)
# --------------------------
st.subheader("🔴 Registro de salidas (ventas)")

producto_sal = st.selectbox("Producto vendido", inventario["nombre"], key="venta")
cant_sal = st.number_input("Cantidad vendida", min_value=1, step=1, key="venta_cant")
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
    resumen = resumen.reset_index().merge(inventario, left_on="producto", right_on="nombre")
    resumen = resumen[["codigo", "producto", "precio", "entrada", "salida", "stock"]]
    resumen.rename(columns={"producto": "nombre"}, inplace=True)
    st.dataframe(resumen, use_container_width=True)
else:
    st.info("Aún no hay movimientos registrados.")

# --------------------------
# Historial de movimientos
# --------------------------
st.markdown("---")
st.subheader("📜 Historial de movimientos")

if not movs.empty:
    st.dataframe(movs.sort_values(by="fecha", ascending=False), use_container_width=True)
    csv = movs.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Descargar historial", csv, file_name="movimientos.csv", mime="text/csv")
else:
    st.info("No hay movimientos registrados aún.")
