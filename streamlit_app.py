import streamlit as st
import datetime

# Diccionario completo del plan de 21 días
daily_plan = {
    1: {"tema": "El Tesoro Interior y el Poder del Subconsciente", "afirmacion": "El tesoro está dentro de mí. La Inteligencia Infinita de mi subconsciente conoce todas las respuestas y está trabajando para mí ahora."},
    2: {"tema": "La Mente como Jardín", "afirmacion": "Mi mente es un jardín fértil. Hoy siembro semillas de paz, salud, alegría y prosperidad."},
    3: {"tema": "La Ley de la Acción y Reacción (Pensamiento Habitual)", "afirmacion": "Mis pensamientos habituales son positivos y constructivos. Mi subconsciente responde ahora a la naturaleza de mis pensamientos de bien."},
    4: {"tema": "Superando el Miedo y la Duda", "afirmacion": "El Padre que hay en mí actúa ahora. Estoy bajo la inspiración directa, liberado de todo miedo y duda. La inteligencia infinita me guía."},
    5: {"tema": "El Poder de Elegir", "afirmacion": "Yo tengo el poder de elegir. Elijo la salud, la felicidad, la paz y la abundancia. Elijo creer que algo bueno me sucederá ahora."},
    6: {"tema": "La Fe y la No Resistencia", "afirmacion": "Reposo en el Señor y espero con tranquilidad. Me fío de Él y Él me satisfará. Mi fe es inquebrantable."},
    7: {"tema": "El Poder de la Gratitud", "afirmacion": "Gracias te doy, Padre, por la prosperidad / la salud / la guía / el bien que ya he recibido."},
    8: {"tema": "Salud Perfecta", "afirmacion": "Una divina perfección se expresa ahora a través de mí. La idea de la salud perfecta llena mi mente subconsciente. Mi subconsciente recrea mi cuerpo de acuerdo con la imagen perfecta de la salud."},
    9: {"tema": "Curación Específica", "afirmacion": "Cada célula, tejido, músculo y nervio de mi cuerpo se está rehaciendo totalmente ahora. Quedan sanos y perfectos."},
    10: {"tema": "Prosperidad y Riqueza (Convicción Interna)", "afirmacion": "Mis asuntos prosperan más día y noche. La riqueza fluye hacia mí."},
    11: {"tema": "Atraer el Dinero Necesario", "afirmacion": "El espíritu nunca se retrasa. La riqueza está siempre al alcance de mis manos. El dinero necesario fluye hacia mí ahora."},
    12: {"tema": "Éxito y Propósito Divino", "afirmacion": "La inteligencia infinita de mi mente subconsciente me revela mi verdadero sitio en la vida y me guía al éxito y la expresión de mi propósito divino."},
    13: {"tema": "Superando Obstáculos Mentales", "afirmacion": "El poder omnisapiente y omnipotente del subconsciente toma el mando y me guía al éxito."},
    14: {"tema": "Visualizando Deseos Cumplidos", "afirmacion": "Esto o algo mejor, según el designio divino, se manifiesta ahora."},
    15: {"tema": "Buscando Guía Divina", "afirmacion": "La Inteligencia Creadora de mi mente subconsciente sabe qué me conviene más. Doy gracias por la respuesta que me llegará."},
    16: {"tema": "El Subconsciente y el Sueño", "afirmacion": "Duermo en paz y me despierto alegre. Mi subconsciente trabaja para mi bien durante la noche."},
    17: {"tema": "Atraer la Pareja Ideal / Relaciones Armoniosas", "afirmacion": "Estoy atrayendo a la persona que armoniza conmigo. Irradio amor y buena voluntad hacia todos."},
    18: {"tema": "El Perdón (Lavar el Alma)", "afirmacion": "Perdono y libero. La paz inunda mi mente."},
    19: {"tema": "Superando Hábitos Negativos", "afirmacion": "Estoy completamente libre de este hábito. Mi mente está llena de paz, alegría y libertad."},
    20: {"tema": "La Verdad sobre la Edad", "afirmacion": "La edad es el nacimiento de la sabiduría en mi mente. Soy tan joven como mis pensamientos."},
    21: {"tema": "Vivir la Verdad (Mantenimiento Continuo)", "afirmacion": "Pienso bien y el bien me sigue. Elijo pensamientos de salud, felicidad y abundancia en cada momento. Practico la Presencia de Dios (la Inteligencia Infinita) a cada minuto."}
}

st.set_page_config(page_title="21 Días para el Subconsciente", layout="centered")
st.title("🌱 Plan de 21 Días para Reprogramar tu Subconsciente")

dia_actual = st.number_input("Selecciona el día (1 a 21):", min_value=1, max_value=21, step=1)
momento = st.radio("¿Es tu práctica de la mañana o de la noche?", ("Mañana", "Noche"))

if dia_actual in daily_plan:
    tema = daily_plan[dia_actual]["tema"]
    afirmacion = daily_plan[dia_actual]["afirmacion"]

    st.subheader(f"Día {dia_actual}: {tema}")

    if momento == "Mañana":
        st.markdown("### 🌞 Práctica Matutina")
        st.markdown("**1. Relájate. Respira profundo. Cierra los ojos si lo deseas.**")
        st.markdown("**2. Lee esta afirmación lentamente, varias veces:**")
    else:
        st.markdown("### 🌙 Práctica Nocturna")
        st.markdown("**1. Relaja cuerpo y mente. Entra en estado de somnolencia.**")
        st.markdown("**2. Repite la afirmación antes de dormir, con emoción.**")

    st.markdown(f"> 🧘‍♀️ *{afirmacion}*  ")

    st.success("Repite esta afirmación durante al menos 5-10 minutos. Siente la emoción detrás de las palabras. ¡Estás sembrando en tu subconsciente!")
else:
    st.warning("Por favor, selecciona un día válido entre 1 y 21.")

# Botón de ayuda
if st.button("¿Cómo debo hacer la práctica diaria?"):
    st.markdown("""
---
### 📘 Cómo debo hacer la práctica diaria:

**Lo crucial, según las fuentes, es la naturaleza y la calidad de las afirmaciones (o "palabras", "súplicas", "plegarias", "decretos", "sugestiones") y cómo se utilizan:**

1. **El Poder de la Palabra y el Pensamiento:** Tus palabras te justifican o condenan. Las palabras y pensamientos tienen una fuerza vibratoria tremenda y dan forma a tu vida y cuerpo. El subconsciente lo graba todo y lo realiza. Es como un disco que graba, y hay que romper los "discos malos" y grabar nuevos.

2. **La Importancia de la Fe y la Convicción:** Debes tener una fe integral en la palabra que pronuncias. La mente subconsciente responde a la naturaleza de tus pensamientos o sugerencias. No es la cosa en la que crees, sino la creencia en tu mente lo que trae resultados.

3. **Ser Específico y Positivo:** Pronuncia tus afirmaciones correctamente. Pide la "selección divina" y evita las "vanas palabras" o pensamientos como "no lo puedo comprar". No tengas duda o conflicto interno.

4. **Sentir como si Ya lo Tuvieras:** Declara que ya has recibido lo que deseas. Regocíjate y siéntelo.

5. **Repetición y Constancia:** La impresión en el subconsciente requiere repetición constante y con emoción. Mañana y noche son momentos ideales.

6. **Momentos Ideales (Mañana y Noche):** Poco antes de dormir y al despertar, la mente está más receptiva.

7. **Visualización e Imaginación:** Visualiza el resultado deseado con claridad y emoción.

8. **Relajación y Soltar:** La mente subconsciente responde a la confianza y no al esfuerzo excesivo. Relájate y permite que actúe.

**En resumen:** La clave es convicción, fe, especificidad, sentimiento real y repetición consistente.
---
""")

st.markdown("---")
st.markdown("Creado para tu práctica diaria consciente ✨")
