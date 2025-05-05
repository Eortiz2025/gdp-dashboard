import streamlit as st
import time

st.set_page_config(page_title="Reprogramación Subconsciente - Murphy & Shinn", layout="centered")
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
        margin-bottom: 30px;
    }
    .step {
        font-size: 1.2em;
        line-height: 1.6em;
    }
</style>
<div class='title'>🌟 Conexión Profunda con tu Subconsciente</div>
<div class='subtitle'>Inspirado en Joseph Murphy y Florence Scovel Shinn</div>
""", unsafe_allow_html=True)

areas = {
    "🩺 Restauración del Cuerpo": [
        ("Armonía Interior", [
            "Cierra los ojos. Respira serenamente. Permite que tu atención descienda al corazón.",
            "Inhala paz… Exhala toda tensión… (x3)",
            "Siente cómo una luz dorada envuelve tu cuerpo físico y etérico.",
            "Di mentalmente: 'Estoy en armonía perfecta con la Ley Divina de salud.'"
        ], 5),
        ("Decretos Sagrados", [
            "La Inteligencia Infinita guía cada célula de mi cuerpo a su perfecto equilibrio.",
            "La salud es mi derecho divino. La acepto con gozo y gratitud.",
            "Soy restaurado por la Sabiduría que me creó."
        ], 5)
    ],
    "💰 Receptividad a la Abundancia": [
        ("Apertura al Bien", [
            "Coloca tu mano sobre el pecho. Inhala profundo desde la gratitud.",
            "Inhala certeza… Exhala toda carencia… (x3)",
            "Imagina una lluvia dorada descendiendo suavemente sobre ti, bendiciendo cada aspecto de tu vida."
        ], 5),
        ("Afirmaciones de Riqueza Espiritual", [
            "La fuente divina me provee ilimitadamente. Estoy siempre sostenido.",
            "Lo que me pertenece por derecho divino viene a mí sin esfuerzo, en orden perfecto.",
            "Acepto el flujo constante de provisión, paz y propósito."
        ], 5)
    ],
    "💞 Relaciones en Armonía": [
        ("Amor Liberador", [
            "Lleva tu conciencia al centro del pecho. Siente tu corazón expandirse.",
            "Inhala amor… Exhala todo resentimiento… (x3)",
            "Visualiza a quienes necesitas liberar envueltos en una esfera de luz rosa."
        ], 5),
        ("Decretos de Unidad y Perdón", [
            "Estoy en paz con todos los seres del universo.",
            "El amor divino fluye en mí, a través de mí y hacia todos mis vínculos.",
            "Perdono. Libero. Amo. Y soy libre."
        ], 5)
    ],
    "🧭 Propósito y Dirección": [
        ("Sintonía con la Voluntad Superior", [
            "Permite que tu mente descanse en silencio. Respira y siente que eres guiado.",
            "Inhala confianza… Exhala confusión… (x3)",
            "Visualiza un sendero claro ante ti, guiado por la luz de tu alma."
        ], 5),
        ("Decretos de Alineación Divina", [
            "El plan perfecto para mi vida se despliega ahora con gracia.",
            "Cada paso que doy es guiado por la Sabiduría interior que sabe.",
            "Estoy en el lugar correcto, haciendo lo correcto, guiado por el Amor divino."
        ], 5)
    ]
}

seleccion = st.radio("Selecciona un camino para tu práctica de hoy:", list(areas.keys()), index=None)

if seleccion:
    st.markdown(f"<div class='subtitle'>Has elegido: {seleccion}</div>", unsafe_allow_html=True)
    contenedor = st.empty()

    for paso in areas[seleccion]:
        titulo, frases, pausa = paso
        for i in range(len(frases)):
            with contenedor:
                st.markdown(f"### {titulo}")
                st.markdown(f"<div class='step'>{'<br><br>'.join(frases[:i+1])}</div>", unsafe_allow_html=True)
            time.sleep(pausa)

    contenedor.success("✨ Has sembrado semillas de verdad en tu subconsciente. Permanece en gratitud unos momentos más.")
