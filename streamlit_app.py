import streamlit as st
import time

st.set_page_config(page_title="Sesión de Reprogramación - Murphy & Shinn", layout="centered")
st.markdown("""
<style>
    .title {
        font-size: 2.6em;
        font-weight: bold;
        color: #4B8BBE;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 1.2em;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 5px;
    }
    .reflection {
        font-size: 1em;
        font-style: italic;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .step {
        font-size: 1.2em;
        line-height: 1.6em;
    }
</style>
<div class='title'>🌟 Reprogramación por Áreas de Vida</div>
<div class='subtitle'>Inspirada en Joseph Murphy y Florence Scovel Shinn</div>
<div class='reflection'>Este es un momento sagrado. Dejo que la Verdad me transforme.</div>
""", unsafe_allow_html=True)

areas = {
    "🩺 Salud y Equilibrio": [
        ("Respiración y Preparación", [
            "Cierra los ojos y lleva tu atención a tu cuerpo.",
            "Inhala calma… Exhala tensión…",
            "Entra en un espacio de armonía interior."
        ]),
        ("Afirmaciones", [
            "Mi cuerpo obedece la ley perfecta de la salud divina.",
            "Cada célula vibra en equilibrio y regeneración.",
            "Estoy completamente sano y en paz."
        ]),
        ("Visualización", [
            "Visualiza una luz blanca envolviendo todo tu cuerpo.",
            "Observa cómo irradias vitalidad y bienestar.",
            "Permanece ahí unos momentos en gratitud."
        ])
    ],
    "💰 Abundancia y Provisión": [
        ("Respiración y Apertura", [
            "Inhala expansión… Exhala toda limitación…",
            "Siente que el universo es un campo de posibilidades infinitas."
        ]),
        ("Afirmaciones", [
            "La provisión divina fluye constantemente en mi vida.",
            "Recibo con gozo y comparto con amor.",
            "Soy un canal perfecto de riqueza espiritual y material."
        ]),
        ("Visualización", [
            "Visualiza una corriente dorada entrando a tu vida.",
            "Siente cómo todo lo que necesitas ya viene en camino.",
            "Agradece desde ahora todo lo que estás recibiendo."
        ])
    ],
    "💞 Relaciones y Amor": [
        ("Respiración de Corazón", [
            "Coloca tu atención en el centro de tu pecho.",
            "Inhala paz… Exhala resentimiento…",
            "Abre tu corazón al amor divino."
        ]),
        ("Afirmaciones", [
            "Estoy en armonía con todos los seres.",
            "El amor divino guía mis vínculos.",
            "Amo, perdono y soy libre."
        ]),
        ("Visualización", [
            "Visualiza un lazo de luz conectándote en paz con quienes amas.",
            "Observa cómo se disuelven los juicios.",
            "Permite que la luz del perdón transforme tus relaciones."
        ])
    ],
    "🧭 Propósito y Paz Interior": [
        ("Respiración y Silencio", [
            "Inhala confianza… Exhala dudas…",
            "Permanece en el centro de tu sabiduría interna."
        ]),
        ("Afirmaciones", [
            "Estoy guiado por la Inteligencia Infinita.",
            "Mi vida tiene dirección, sentido y propósito.",
            "Confío en el camino que se despliega ante mí."
        ]),
        ("Visualización", [
            "Visualiza tu día ideal: con propósito, gozo y claridad.",
            "Siente que ya estás viviendo esa verdad.",
            "Agradece por tu misión alineada con lo superior."
        ])
    ]
}

seleccion = st.radio("Selecciona un área para trabajar hoy:", list(areas.keys()), index=None)

if seleccion:
    contenedor = st.empty()
    for titulo, frases in areas[seleccion]:
        for frase in frases:
            with contenedor:
                st.markdown(f"### {titulo}")
                st.markdown(f"<div class='step'>{frase}</div>", unsafe_allow_html=True)
            time.sleep(9)

    contenedor.success("🌟 Has sembrado nuevas semillas de verdad. Quédate en calma y gratitud unos instantes más.")
