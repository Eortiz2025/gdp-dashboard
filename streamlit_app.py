import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config("POS + Inventario", layout="centered")
st.title("🧾 Punto de Venta - OlaCafe (con Tickets)")

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
        return pd.DataFrame(columns=["fecha", "tipo", "producto", "cantidad", "proveedor", "ticket"])

def guardar_movimientos_batch(detalles):
    df = cargar_movimientos()
    nuevos = pd.DataFrame(detalles)
    df = pd.concat([df, nuevos], ignore_index=True)
    df.to_csv("movimientos.csv", index=False)

def generar_codigo_ticket():
    hoy = datetime.now().strftime("%Y%m%d")
    df = cargar_movimientos()
    if "ticket" in df.columns:
        hoy_tickets = df[df["ticket"].str.contains(hoy, na=False)]
        consecutivo = len(hoy_tickets) + 1
    else:
        consecutivo = 1
    return f"T-{hoy}-{consecutivo:04d}"

# --------------------------
# Sesión: inicializar carrito
# --------------------------
if "carrito" not in st.session_state:
    st.session_state["carrito"] = []

# --------------------------
# Cargar datos
# --------------------------
inventario = cargar_inventario()

# --------------------------
# Agregar productos al carrito
# --------------------------
st.subheader("🛒 Agregar productos al ticket")

producto_sel = st.selectbox("Producto", inventario["nombre"])
cantidad = st.number_input("Cantidad", min_value=1, step=1)
if st.button("➕ Agregar al ticket"):
    producto = inventario[inventario["nombre"] == producto_sel].iloc[0]
    st.session_state.carrito.append({
        "producto": producto["nombre"],
        "cantidad": cantidad,
        "precio": producto["precio"],
        "subtotal": cantidad * producto["precio"]
    })
    st.success(f"Agregado: {producto['nombre']} x {cantidad}")

# --------------------------
# Mostrar contenido del ticket
# --------------------------
st.markdown("---")
st.subheader("📋 Ticket actual")

if st.session_state.carrito:
    df_ticket = pd.DataFrame(st.session_state.carrito)
    total = df_ticket["subtotal"].sum()
    st.dataframe(df_ticket[["producto", "cantidad", "precio", "subtotal"]], use_container_width=True)
    st.markdown(f"### 💵 Total a cobrar: ${total:,.2f}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Registrar venta"):
            ticket_id = generar_codigo_ticket()
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            detalles = [{
                "fecha": fecha,
                "tipo": "salida",
                "producto": item["producto"],
                "cantidad": item["cantidad"],
                "proveedor": None,
                "ticket": ticket_id
            } for item in st.session_state.carrito]
            guardar_movimientos_batch(detalles)
            st.success(f"✅ Venta registrada con ticket: {ticket_id}")
            st.session_state.carrito = []  # Limpiar carrito

    with col2:
        if st.button("🗑️ Cancelar ticket"):
            st.session_state.carrito = []
            st.info("Ticket cancelado.")
else:
    st.info("No hay productos en el ticket aún.")

# --------------------------
# Inventario actual
# --------------------------
st.markdown("---")
st.subheader("📦 Inventario actual")

movs = cargar_movimientos()

if not movs.empty:
    resumen = movs.groupby(["producto", "tipo"])["cantidad"].sum().unstack().fillna(0)
    resumen["stock"] = resumen.get("entrada", 0) - resumen.get("salida", 0)
    resumen = resumen.reset_index().merge(inventario, left_on="producto", right_on="nombre", how="left")

    for col in ["entrada", "salida"]:
        if col not in resumen.columns:
            resumen[col] = 0

    columnas = ["codigo", "producto", "precio", "entrada", "salida", "stock"]
    columnas_existentes = [c for c in columnas if c in resumen.columns]
    resumen = resumen[columnas_existentes]
    if "producto" in resumen.columns:
        resumen.rename(columns={"producto": "nombre"}, inplace=True)

    bajo = resumen[resumen["stock"] <= 5] if "stock" in resumen.columns else pd.DataFrame()
    if not bajo.empty:
        st.warning("⚠️ Stock bajo")
        st.dataframe(bajo)

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
    st.download_button("📥 Descargar historial completo", csv, file_name="movimientos.csv", mime="text/csv")
else:
    st.info("No hay movimientos registrados aún.")
