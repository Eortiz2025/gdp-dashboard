import streamlit as st
import time

st.set_page_config(page_title="Meditación por Áreas - Murphy, Silva y Shinn", layout="centered")
st.title("🧘‍♀️ Meditación Guiada por Áreas de Vida")

# Áreas disponibles con instrucciones respiratorias repetidas 3 veces
areas = {
    "🩺 Salud": [
        ("Respiración curativa", [
            "Respira profundamente y coloca tu atención en tu cuerpo.",
            "Inhala calma…",
            "Exhala tension…",
            "Inhala calma…",
            "Exhala tension…",
            "Inhala calma…",
            "Exhala tension…",
            "Imagina que cada célula recibe inteligencia sanadora.",
            "Di mentalmente: Estoy completamente sano y en equilibrio."
        ], 4),
        ("Visualización Silva", [
            "Visualiza una luz blanca envolviendo tu cuerpo.",
            "Esa luz armoniza tus órganos, nervios y emociones.",
            "Observa tu cuerpo fuerte, en paz y en movimiento libre."
        ], 5),
        ("Decretos finales", [
            "La inteligencia que me creó me restaura ahora.",
            "Mi subconsciente actúa con poder curativo.",
            "Gracias. Asi es, asi sera, Ya está hecho."
        ], 4)
    ],
    "💰 Abundancia": [
        ("Respiración de abundacia", [
            "Inhala expansión…",
            "Exhala limitaciones…",
            "Inhala expansión…",
            "Exhala limitaciones…",
            "Inhala expansión…",
            "Exhala limitaciones…",
            "Relaja todo el cuerpo, siente espacio."
        ], 4),
        ("Visualización de flujo", [
            "Imagina un río dorado entrando a tu vida.",
            "Ese río representa el bien, el dinero, las oportunidades.",
            "Obsérvate recibiendo con alegría y compartiendo sin miedo."
        ], 5),
        ("Decretos afirmativos", [
            "Todo lo bueno que me pertenece viene a mí en armonía perfecta.",
            "Estoy abierto a la riqueza, la abundancia y el orden divino.",
            "Gracias. Asi es, asi sera, lo acepto con alegría."
        ], 4)
    ],
    "💞 Relaciones": [
        ("Respiración en el corazón", [
            "Coloca tu mano en el pecho.",
            "Inhala paz…",
            "Exhala resentimiento…",
            "Inhala paz…",
            "Exhala resentimiento…",
            "Inhala paz…",
            "Exhala resentimiento…",
            "Siente compasión hacia ti y hacia los demás."
        ], 4),
        ("Visualización de armonía", [
            "Imagina a la persona con quien necesitas sanar.",
            "Visualiza un lazo de luz entre ustedes, desde el corazón.",
            "Di mentalmente: Te suelto en paz. Me libero. Somos libres."
        ], 5),
        ("Decretos amorosos", [
            "Estoy en paz con todos los seres del universo.",
            "Lo que doy, vuelve a mí multiplicado en armonía.",
            "El amor divino gobierna mis relaciones."
        ], 4)
    ],
    "🧭 Propósito y Paz": [
        ("Respiración de Paz", [
            "Inhala confianza…",
            "Exhala temor…",
            "Inhala confianza…",
            "Exhala temor…",
            "Inhala confianza…",
            "Exhala temor…",
            "Siente el centro de tu pecho en calma.",
            "Permanece unos segundos en ese vacío fértil."
        ], 4),
        ("Visualización con propósito", [
            "Visualiza tu día ideal, tu trabajo perfecto, tu forma de servir al mundo.",
            "Observa alegría, claridad y sentido.",
            "Di mentalmente: Estoy guiado. Estoy alineado con lo mejor en mí."
        ], 5),
        ("Decretos de guía", [
            "La inteligencia infinita me guía en cada paso.",
            "Cada día estoy más alineado con mi propósito.",
            "Confío. Estoy en el camino correcto."
        ], 4)
    ]
}

# Mostrar botones
seleccion = st.radio("Selecciona un área para trabajar hoy:", list(areas.keys()), index=None)

# Mostrar rutina paso a paso
if seleccion:
    st.markdown(f"## {seleccion}")
    contenedor = st.empty()

    for titulo, frases, pausa in areas[seleccion]:
        for i in range(len(frases)):
            with contenedor:
                st.markdown(f"### {titulo}")
                st.markdown("\n\n".join(frases[:i+1]))
            time.sleep(pausa)

    contenedor.success("🌟 Has completado tu sesión. Quédate unos segundos más en silencio si lo deseas.")


