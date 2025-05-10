import streamlit as st
import random
from datetime import datetime

st.set_page_config(page_title="Manifiesta con el Subconsciente", layout="centered")
st.title("✨ Manifiesta con el Poder de tu Subconsciente")

# --- Afirmaciones Poderosas ---
afirmaciones = [
    "Estoy conectado con la inteligencia infinita de mi subconsciente y recibo guía perfecta.",
    "Cada célula de mi cuerpo vibra con salud, energía y vitalidad.",
    "Estoy guiado con claridad hacia mi propósito más elevado.",
    "Acepto pensamientos de abundancia y bienestar. La prosperidad fluye hacia mí.",
    "Mi subconsciente manifiesta soluciones perfectas a todos los desafíos.",
    "Soy merecedor de amor, paz y éxito. Lo acepto ahora.",
    "Visualizo mi éxito y lo siento como una realidad presente.",
    "Todo lo que necesito ya está dentro de mí.",
    "Cada día soy más fuerte, más claro y más inspirado.",
    "La paz interior guía cada decisión que tomo hoy."
]

# --- Momento del Día ---
momento = st.radio("¿Qué momento del día estás practicando?", ["🌞 Mañana", "🌇 Tarde (Refuerzo)", "🌙 Noche"])

# --- Inicio Diario ---
if momento == "🌞 Mañana":
    st.subheader("🔑 Tu afirmación para comenzar el día:")
    afirmacion = random.choice(afirmaciones)
    st.success(afirmacion)
    st.markdown("---")
    st.markdown("### 👁 Visualiza el resultado como si ya se cumpliera")
    st.markdown("Cierra los ojos 1 minuto y siéntelo como real.")
    st.markdown("---")
    st.text_input("✍️ Escribe tu intención del día en tiempo presente:", key="intencion")

elif momento == "🌇 Tarde (Refuerzo)":
    st.subheader("🔁 Refuerza tu afirmación del día")
    st.info("Repite tu afirmación con emoción al menos 3 veces")
    st.text_area("🔊 Repite aquí o en voz baja:", key="refuerzo")

elif momento == "🌙 Noche":
    st.subheader("😴 Último pensamiento antes de dormir")
    st.markdown("### Da gracias como si tu deseo ya fuera real")
    st.text_area("🙏 Escribe tu agradecimiento de hoy:", key="gratitud")
    st.markdown("---")
    st.markdown("🧘 Cierra los ojos. Repite tu deseo con paz. Entrégalo a tu mente subconsciente.")

# --- Guía Central (Resumen 9 pasos) ---
with st.expander("📘 Ver Guía para Activar tu Mente Subconsciente"):
    st.markdown("""
**1. Comprende tu mente:** Consciente = piensa. Subconsciente = crea. Repite con convicción.  
**2. Define tu deseo:** Claro, específico y visualízalo como ya cumplido.  
**3. Impresión subconsciente:** Visualización + afirmación + emoción + gratitud.  
**4. Fe y certeza:** No es esperanza, es convicción. Siente que ya es real.  
**5. Evita esfuerzo mental:** No fuerces, relájate. El subconsciente responde a calma.  
**6. Elimina bloqueos:** Perdona, suelta crítica, suelta miedo. Protege tu mente.  
**7. Sé constante:** Repite cada día. No te detengas si no ves resultados inmediatos.  
**8. Vive tu deseo ahora:** Siente cómo sería si ya lo tuvieras.  
**9. Da y sirve:** Tu éxito debe beneficiar a otros. Así cierras el ciclo de abundancia.
    """)

# --- Sección Especial: 3 Pasos del Éxito (Murphy) ---
with st.expander("🌟 Los 3 Pasos del Éxito (Joseph Murphy)"):
    st.markdown("""
**1. Descubre lo que amas hacer.** Pide guía si no sabes aún:  
`La inteligencia infinita me revela mi verdadero sitio en la vida.`

**2. Vuélvete experto en ello.** Lee, aprende, práctica.  

**3. Asegúrate de que lo que haces beneficie a otros.** El éxito real involucra propósito y servicio.
    """)

st.markdown("---")
st.caption("🌀 Repite con emoción. Cree con convicción. Vive con intención.")
