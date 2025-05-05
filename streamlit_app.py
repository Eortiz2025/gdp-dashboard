import streamlit as st
import time

st.set_page_config(page_title="Meditación por Áreas - Murphy, Silva y Shinn", layout="centered")
st.markdown("""
<style>
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: #4B8BBE;
        text-align: center;
    }
    .subtitle {
        font-size: 1.3em;
        color: #306998;
    }
    .section-title {
        color: #2C3E50;
        font-weight: bold;
    }
</style>
<div class='title'>🧘‍♀️ Meditación Guiada por Áreas de Vida</div>
""", unsafe_allow_html=True)

# Imágenes simbólicas por área
imagenes = {
    "🩺 Salud": "https://images.unsplash.com/photo-1552068751-34cb6b48b5bc?fit=crop&w=800&q=80",
    "💰 Abundancia": "https://images.unsplash.com/photo-1526401485004-2fa806b5dca3?fit=crop&w=800&q=80",
    "💞 Relaciones": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?fit=crop&w=800&q=80",
    "🧭 Propósito y Paz": "https://images.unsplash.com/photo-1506748686214-e9df14d4d9d0?fit=crop&w=800&q=80"
}

areas = {
    "🩺 Salud": [
        ("Respiración Curativa", [
            "Respira profundamente y coloca tu atención en tu cuerpo.",
            "Inhala calma…", "Exhala tensión…",
            "Inhala calma…", "Exhala tensión…",
            "Inhala calma…", "Exhala tensión…",
            "Imagina que cada célula recibe inteligencia sanadora.",
            "Di mentalmente: Estoy completamente sano y en equilibrio."
        ], 4),
        ("Visualización de Salud", [
            "Visualiza una luz blanca envolviendo tu cuerpo.",
            "Esa luz armoniza tus órganos, nervios y emociones.",
            "Observa tu cuerpo fuerte, en paz y en movimiento libre."
        ], 5, True),
        ("Decretos de Sanación", [
            "La inteligencia que me creó me restaura ahora.",
            "Mi subconsciente actúa con poder curativo.",
            "Gracias. Así es. Así será. Ya está hecho."
        ], 4),
        ("Integración Sensorial (Método Silva)", [
            "🔍 ¿Qué estoy viendo ahora que mi cuerpo ya irradia salud y energía?",
            "❤️ ¿Cómo se siente mi cuerpo al moverse libre, fuerte y en armonía?",
            "👂 ¿Qué escucho decir a mi interior o a los demás sobre mi bienestar renovado?"
        ], 10)
    ],
    "💰 Abundancia": [
        ("Respiración de Abundancia", [
            "Inhala expansión…", "Exhala limitaciones…",
            "Inhala expansión…", "Exhala limitaciones…",
            "Inhala expansión…", "Exhala limitaciones…",
            "Relaja todo el cuerpo, siente espacio."
        ], 4),
        ("Visualización de Flujo", [
            "Imagina un río dorado entrando a tu vida.",
            "Ese río representa el bien, el dinero, las oportunidades.",
            "Obsérvate recibiendo con alegría y compartiendo sin miedo."
        ], 5, True),
        ("Decretos de Abundancia", [
            "Todo lo bueno que me pertenece viene a mí en armonía perfecta.",
            "Estoy abierto a la riqueza, la abundancia y el orden divino.",
            "Gracias. Así es. Así será. Lo acepto con alegría y certeza."
        ], 4),
        ("Integración Sensorial (Método Silva)", [
            "🔍 ¿Qué veo en mi entorno ahora que la abundancia fluye con naturalidad?",
            "❤️ ¿Cómo se siente en mi cuerpo y corazón el vivir sin miedo, con plenitud?",
            "👂 ¿Qué escucho al recibir oportunidades, agradecimientos y confirmaciones?"
        ], 10)
    ],
    "💞 Relaciones": [
        ("Respiración en el Corazón", [
            "Coloca tu mano en el pecho.",
            "Inhala paz…", "Exhala resentimiento…",
            "Inhala paz…", "Exhala resentimiento…",
            "Inhala paz…", "Exhala resentimiento…",
            "Siente compasión hacia ti y hacia los demás."
        ], 4),
        ("Visualización de Armonía", [
            "Imagina a la persona con quien necesitas sanar.",
            "Visualiza un lazo de luz entre ustedes, desde el corazón.",
            "Di mentalmente: Te suelto en paz. Me libero. Somos libres."
        ], 5, True),
        ("Decretos de Amor", [
            "Estoy en paz con todos los seres del universo.",
            "Lo que doy, vuelve a mí multiplicado en armonía.",
            "El amor divino gobierna mis relaciones."
        ], 4),
        ("Integración Sensorial (Método Silva)", [
            "🔍 ¿Qué imágenes vienen a mí ahora que hay paz y amor en mis vínculos?",
            "❤️ ¿Qué emociones fluyen en mí cuando comparto con otros desde el corazón?",
            "👂 ¿Qué palabras de armonía, perdón o gratitud escucho resonar?"
        ], 10)
    ],
    "🧭 Propósito y Paz": [
        ("Respiración de Paz Interior", [
            "Inhala confianza…", "Exhala temor…",
            "Inhala confianza…", "Exhala temor…",
            "Inhala confianza…", "Exhala temor…",
            "Siente el centro de tu pecho en calma.",
            "Permanece unos segundos en ese vacío fértil."
        ], 4),
        ("Visualización con Propósito", [
            "Visualiza tu día ideal, tu trabajo perfecto, tu forma de servir al mundo.",
            "Observa alegría, claridad y sentido.",
            "Di mentalmente: Estoy guiado. Estoy alineado con lo mejor en mí."
        ], 5, True),
        ("Decretos de Guía", [
            "La inteligencia infinita me guía en cada paso.",
            "Cada día estoy más alineado con mi propósito.",
            "Confío. Estoy en el camino correcto."
        ], 4),
        ("Integración Sensorial (Método Silva)", [
            "🔍 ¿Qué veo cuando estoy caminando en mi propósito con claridad y certeza?",
            "❤️ ¿Qué sensaciones me recorren al saber que estoy alineado con mi alma?",
            "👂 ¿Qué escucho desde mi guía interior o el universo que me confirma este camino?"
        ], 10)
    ]
}

seleccion = st.radio("Selecciona un área para trabajar hoy:", list(areas.keys()), index=None)

if seleccion:
    st.markdown(f"<div class='subtitle'>Has seleccionado: {seleccion}</div>", unsafe_allow_html=True)
    contenedor = st.empty()

    for paso in areas[seleccion]:
        if len(paso) == 4 and paso[3]:
            st.image(imagenes[seleccion], use_container_width=True)
        titulo, frases, pausa = paso[:3]
        for i in range(len(frases)):
            with contenedor:
                st.markdown(f"### {titulo}")
                st.markdown("\n\n".join(frases[:i+1]))
            time.sleep(pausa)

    contenedor.success("🌟 Has completado tu sesión. Quédate unos segundos más en silencio si lo deseas.")
