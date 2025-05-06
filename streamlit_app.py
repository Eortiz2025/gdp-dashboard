import streamlit as st
import time

# Configuración inicial de la página
st.set_page_config(page_title="Sesión de Reprogramación - Murphy & Shinn", layout="centered")

# Estilos personalizados
st.markdown('''
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
''', unsafe_allow_html=True)

# Definición de áreas y secciones con mejoras
areas = {
    "🩺 Salud y Equilibrio": [
        ("Preparación Mental", [
            "Estoy en paz. Mi mente consciente y subconsciente están en armonía.",
            "Estoy receptivo/a a la salud y el equilibrio que ya son míos por derecho divino."
        ]),
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
        ("Visualización Cinemática", [
            "Imagina una escena donde te ves lleno/a de energía y vitalidad.",
            "Vive esa película interna con todos tus sentidos.",
            "Siente gratitud por esa salud manifestada."
        ])
    ],
    "💰 Abundancia y Provisión": [
        ("Preparación Mental", [
            "Renuncio a todo pensamiento de carencia. Acepto mi provisión ilimitada.",
            "Dios es mi fuente. Todo fluye hacia mí en abundancia perfecta."
        ]),
        ("Respiración y Apertura", [
            "Inhala expansión… Exhala toda limitación…",
            "Siente que el universo es un campo de posibilidades infinitas."
        ]),
        ("Afirmaciones", [
            "La provisión divina fluye constantemente en mi vida.",
            "Recibo con gozo y comparto con amor.",
            "Soy un canal perfecto de riqueza espiritual y material."
        ]),
        ("Visualización Cinemática", [
            "Visualiza una corriente dorada entrando a tu vida.",
            "Mira una película mental donde tus necesidades ya están cubiertas.",
            "Agradece por el flujo constante de recursos."
        ])
    ],
    "💞 Relaciones y Amor": [
        ("Preparación Mental", [
            "Perdono y libero todo juicio. Estoy listo/a para el amor perfecto.",
            "Soy amor, doy amor, recibo amor."
        ]),
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
        ("Visualización Cinemática", [
            "Visualiza un lazo de luz conectándote en paz con quienes amas.",
            "Observa una escena de armonía y comprensión con tus relaciones.",
            "Permite que la luz del perdón transforme tus vínculos."
        ])
    ],
    "🧭 Propósito y Paz Interior": [
        ("Preparación Mental", [
            "Confío en mi sabiduría interna. Estoy alineado con el propósito divino.",
            "La paz y la claridad son mi estado natural."
        ]),
        ("Respiración y Silencio", [
            "Inhala confianza… Exhala dudas…",
            "Permanece en el centro de tu sabiduría interna."
        ]),
        ("Afirmaciones", [
            "Estoy guiado por la Inteligencia Infinita.",
            "Mi vida tiene dirección, sentido y propósito.",
            "Confío en el camino que se despliega ante mí."
        ]),
        ("Visualización Cinemática", [
            "Visualiza tu día ideal: con propósito, gozo y claridad.",
            "Mira una película mental donde vives con sentido y paz.",
            "Agradece por tu misión alineada con lo superior."
        ])
    ]
}

# Interfaz principal
seleccion = st.radio("Selecciona un área para trabajar hoy:", list(areas.keys()), index=None)

if seleccion:
    if st.button("Comenzar"):
        contenedor = st.empty()
        for titulo, frases in areas[seleccion]:
            for frase in frases:
                with contenedor:
                    st.markdown(f"### {titulo}")
                    st.markdown(f"<div class='step'>{frase}</div>", unsafe_allow_html=True)
                time.sleep(9)
        contenedor.success("🌟 Has sembrado nuevas semillas de verdad. Quédate en calma y gratitud unos instantes más.")
