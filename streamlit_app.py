import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Cargar inventario
def cargar_inventario():
    if os.path.exists("inventario.csv"):
        return pd.read_csv("inventario.csv")
    else:
        st.error("No se encontró 'inventario.csv'")
        return pd.DataFrame(columns=["codigo", "nombre", "precio", "stock"])

# Guardar inventario actualizado
def guardar_inventario(df):
    df.to_csv("inventario.csv", index=False)

# Guardar venta
def registrar_venta(producto, cantidad, total):
    venta = pd.DataFrame([{
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "producto": producto,
        "cantidad": cantidad,
        "total": total
    }])
    archivo = "ventas.csv"
    if os.path.exists(archivo):
        venta.to_csv(archivo, mode="a", header=False, index=False)
    else:
        venta.to_csv(archivo, index=False)

# Interfaz
st.set_page_config("POS Café", layout="centered")
st.title("🧾 Punto de Venta - OlaCafe")

inventario = cargar_inventario()

if not inventario.empty:
    producto_seleccionado = st.selectbox("Selecciona un producto", inventario["nombre"])
    datos_producto = inventario[inventario["nombre"] == producto_seleccionado].iloc[0]

    precio = datos_producto["precio"]
    stock = datos_producto["stock"]

    cantidad = st.number_input("Cantidad", min_value=1, max_value=int(stock), step=1)

    total = cantidad * precio
    st.markdown(f"**Total: ${total:,.2f}**")

    if st.button("💳 Registrar venta"):
        idx = inventario[inventario["nombre"] == producto_seleccionado].index[0]
        if cantidad <= inventario.at[idx, "stock"]:
            inventario.at[idx, "stock"] -= cantidad
            guardar_inventario(inventario)
            registrar_venta(producto_seleccionado, cantidad, total)
            st.success("Venta registrada con éxito ✅")
            st.info(f"Ticket:\n\nProducto: {producto_seleccionado}\nCantidad: {cantidad}\nTotal: ${total:,.2f}")
        else:
            st.error("No hay suficiente stock para esta venta.")
