import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="21 Días de Conexión", layout="centered")
st.title("🌞 Día a día, mejoro y mejoro.")

# --- Afirmaciones Diarias Aleatorias ---
afirmaciones_dia = [
    "Estoy conectado con la inteligencia infinita de mi subconsciente y recibo guía perfecta en todo momento.",
    "Cada célula de mi cuerpo vibra con salud, energía y vitalidad renovada.",
    "Soy mente clara, enfoque preciso y calma profunda en cada situación.",
    "Mi vida fluye con propósito, amor y equilibrio. Estoy en armonía con el universo.",
    "Acepto pensamientos de abundancia, y la prosperidad fluye hacia mí sin esfuerzo.",
    "Mi subconsciente manifiesta soluciones perfectas a todos los desafíos que enfrento.",
    "Estoy lleno de amor hacia mí mismo y hacia los demás. Atraigo relaciones armoniosas.",
    "Libero creencias limitantes y acepto solo pensamientos que me empoderan.",
    "Visualizo mi éxito y lo siento como una realidad. Mi subconsciente lo manifiesta.",
    "Estoy alineado con la salud perfecta en cuerpo, mente y espíritu.",
    "Todo lo que necesito ya está dentro de mí. Confío en mi sabiduría interior.",
    "Cada día soy más fuerte, más claro y más conectado con mi ser superior.",
    "La paz interior guía cada decisión que tomo hoy.",
    "Estoy abierto a recibir milagros y bendiciones en todos los aspectos de mi vida.",
    "Soy libre de miedos y dudas. Confío plenamente en la vida.",
    "Mi subconsciente crea mi realidad. Por eso elijo pensamientos de poder y belleza.",
    "La gratitud abre todas las puertas. Hoy agradezco y recibo con alegría.",
    "Todo está sucediendo para mi bien. Elijo ver oportunidades donde antes veía obstáculos.",
    "Mi cuerpo responde con salud a cada pensamiento amoroso que tengo.",
    "Estoy profundamente en paz conmigo mismo y con el mundo.",
    "Soy un canal limpio para la energía divina que fluye a través de mí cada día."
]

# --- Modo 21 Días con Progreso ---
plan_21_dias = {
    i: {
        "mañana": f"🌞 Afirmación del día {i}: ...",  # Reemplazar con afirmaciones reales
        "noche": f"🌙 Afirmación nocturna día {i}: ..."
    }
    for i in range(1, 22)
}

if "progreso" not in st.session_state:
    st.session_state.progreso = {i: False for i in range(1, 22)}

# --- Navegación ---
modo = st.sidebar.radio("Selecciona modo de práctica:", ["Inicio Diario", "21 Días Guiados"])

if modo == "Inicio Diario":
    if "inicio_completo" not in st.session_state:
        st.session_state.inicio_completo = False

    if not st.session_state.inicio_completo:
        afirmacion = random.choice(afirmaciones_dia)
        st.markdown("### ✨ Afirmación del día")
        st.success(afirmacion)
        if st.button("🌀 Iniciar conexión al Subconsciente"):
            st.session_state.inicio_completo = True
            st.rerun()

    else:
        st.markdown("### 🧠 Mi mente subconsciente todo lo puede.")
        st.markdown("## ¿Cuál es mi deseo más grande?")

        with st.expander("👁 Cierra los ojos por un minuto y busca dentro de ti"):
            st.info("Respira profundo, relájate y conéctate con lo que verdaderamente deseas.")

        if "afirma_deseo" not in st.session_state:
            if st.button("✅ Ya sé lo que deseo"):
                st.session_state.afirma_deseo = True
                st.rerun()
        else:
            st.success("Excelente. Ahora tomemos los pasos para lograrlo.")
            st.markdown("### 🚶 Paso a paso tu deseo se convierte en realidad si lo sostienes con claridad y emoción.")

            st.markdown("¿Qué deseas hacer ahora para avanzar?")
            opcion = st.radio("Elige tu siguiente acción:", ["Visualizar", "Afirmar", "Escribir"], index=0)

            if opcion == "Visualizar":
                st.markdown("### 👁 Visualiza el resultado final como si ya se hubiera cumplido.")
                st.markdown("- ¿Qué estás viendo?\n- ¿Cómo te sientes?\n- ¿Qué cambia en ti?")
                st.info("Permanece unos segundos con la imagen en tu mente y siéntela real.")

            elif opcion == "Afirmar":
                st.markdown("### 📣 Cómo crear tu afirmación:")
                st.markdown("""
                Una buena afirmación es:
                - En tiempo presente
                - Positiva y concreta
                - Emocionalmente verdadera

                **Ejemplos:**
                - “Estoy en calma, guiado y bendecido.”
                - “Mi cuerpo se llena de salud y energía cada día.”
                - “Soy merecedor de abundancia y la acepto con alegría.”
                """)

                afirmacion = st.text_input("✍️ Escribe tu afirmación personalizada aquí:")
                if afirmacion.strip():
                    st.success(f"Repite esta afirmación varias veces hoy:\n\n*{afirmacion}*")
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"afirmacion_{timestamp}.txt"
                    st.download_button("📥 Descargar afirmación", data=afirmacion, file_name=filename, mime="text/plain")
                    st.info("✅ Al guardar y repetir tu afirmación, la siembras más profundamente en tu subconsciente.")

            elif opcion == "Escribir":
                st.markdown("### 📝 Cómo escribir tu deseo de forma efectiva:")
                st.markdown("""
                Escribe tu deseo:
                - En presente, como si ya lo vivieras
                - Con gratitud
                - Con emoción y detalle

                **Ejemplo:**
                “Estoy disfrutando de una vida abundante, con salud plena, rodeado de amor y alegría. Me siento en paz.”
                """)

                descripcion = st.text_area("Escribe aquí tu deseo en tus propias palabras:")
                if descripcion.strip():
                    st.success("Muy bien. Cuanto más clara y sentida la descripción, más fuerte la impresión en tu subconsciente.")
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    filename = f"deseo_{timestamp}.txt"
                    st.download_button("📥 Descargar deseo", data=descripcion, file_name=filename, mime="text/plain")
                    st.info("✅ Escribir tu deseo es una poderosa forma de enfocarte y permitir su manifestación.")

elif modo == "21 Días Guiados":
    st.markdown("### 📅 Selecciona tu día de práctica")
    dia = st.selectbox("Día del programa", list(range(1, 22)))

    st.markdown(f"#### 🔆 Afirmación de la Mañana (Día {dia})")
    st.success(plan_21_dias[dia]["mañana"])

    st.markdown("#### ✍️ Escribe tu intención de hoy (opcional)")
    st.text_area("¿Qué deseo sembrar hoy en mi subconsciente?", key=f"deseo_{dia}")

    st.markdown(f"#### 🌙 Afirmación de la Noche (Día {dia})")
    st.info(plan_21_dias[dia]["noche"])

    dia_completo = st.checkbox("✅ He completado las prácticas de este día", value=st.session_state.progreso[dia])
    if dia_completo:
        st.session_state.progreso[dia] = True
        st.success("Día marcado como completado. ¡Felicidades por tu constancia!")

    completados = sum(1 for estado in st.session_state.progreso.values() if estado)
    st.markdown(f"### 🔄 Progreso: {completados}/21 días completados")
