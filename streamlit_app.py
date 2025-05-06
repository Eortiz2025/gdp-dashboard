import streamlit as st

# Afirmaciones con lenguaje más neutral y universal
afirmaciones_dia = {
    1: {"mañana": "Mi subconsciente coopera conmigo y responde con precisión a las instrucciones que le doy.",
        "noche": "Cada pensamiento que cultivo crea condiciones a mi favor. Me hago responsable de lo que pienso y siento."},
    2: {"mañana": "Mis palabras y pensamientos son semillas de poder que mi subconsciente transforma en realidades armoniosas y perfectas.",
        "noche": "Cuando pienso con claridad y paz, mi subconsciente responde con acciones constructivas y equilibradas."},
    3: {"mañana": "Reemplazo viejas creencias por ideas nuevas, positivas y llenas de vida que mi subconsciente acepta.",
        "noche": "Dirijo mi mente con intención y mi subconsciente obedece mis pensamientos claros y positivos."},
    4: {"mañana": "Libero toda creencia limitante y dejo espacio para nuevas ideas que reflejan bienestar y confianza.",
        "noche": "Uso un lenguaje consciente y empoderador que impulsa a mi subconsciente a actuar a mi favor."},
    5: {"mañana": "Instalo en mi mente pensamientos de salud, bienestar, abundancia y plenitud que forman mi nueva realidad.",
        "noche": "Mis pensamientos crean mi mundo. Elijo alimentar mi mente con ideas de éxito, bienestar y propósito."},
    6: {"mañana": "Transformo mis palabras para transformar mis experiencias. Elijo hablar con claridad, optimismo y verdad.",
        "noche": "Renuevo mi vida renovando mi forma de pensar. Cada pensamiento positivo me acerca a mi propósito."},
    7: {"mañana": "Deseo lo mejor para los demás, y ese mismo bienestar fluye naturalmente hacia mí.",
        "noche": "Mi mente subconsciente acepta toda idea que repito con convicción. Por eso cultivo pensamientos de bienestar."},
    8: {"mañana": "Tengo acceso a la claridad y tomo decisiones alineadas con lo mejor para mí.",
        "noche": "Selecciono cuidadosamente mis pensamientos, permitiendo solo los que construyen mi bienestar."},
    9: {"mañana": "Fortalezco mi fe a través de la práctica diaria de pensamientos confiados y amables.",
        "noche": "Tengo el poder de elegir pensamientos que me elevan. Elijo vida, amor, salud y claridad."},
    10: {"mañana": "La armonía comienza dentro de mí y se refleja en cada aspecto de mi entorno.",
         "noche": "Nutro mi mente subconsciente con ideas que sanan, expanden y elevan mi consciencia."},
    11: {"mañana": "Elijo soltar el pasado y abro espacio al bienestar, la reconciliación y el crecimiento interior.",
         "noche": "Mi mente subconsciente actúa según las ideas que mantengo con claridad y decisión."},
    12: {"mañana": "Declaro con certeza que mi camino se revela fácilmente y con éxito.",
         "noche": "Transformo todo pensamiento que limita y fortalezco los que me conectan con mi propósito."},
    13: {"mañana": "Mi voz interior tiene el poder de transformar el miedo en confianza.",
         "noche": "Confío en mi intuición. Me guía paso a paso hacia el cumplimiento de mis objetivos."},
    14: {"mañana": "Reconozco la energía vital en todo lo que hago y en cada situación que experimento.",
         "noche": "Incluso mientras descanso, mi subconsciente continúa organizando mi vida hacia el bienestar."},
    15: {"mañana": "Confío en el proceso de la vida. Suelto el control y permito que lo mejor fluya hacia mí.",
         "noche": "Declaro con claridad lo que deseo y lo entrego a mi subconsciente, que actúa mientras duermo."},
    16: {"mañana": "Estoy conectada con la energía de la abundancia. Todo lo que necesito llega a mí con facilidad.",
         "noche": "Mi mente crea lo que imagina. Por eso elijo imágenes mentales llenas de éxito, gratitud y paz."},
    17: {"mañana": "Visualizo mi deseo cumplido y agradezco su realización. Ya está sucediendo.",
         "noche": "Siento la certeza de que mis pensamientos constructivos están dando fruto ahora mismo."},
    18: {"mañana": "Doy gracias por todo lo bueno que ya es parte de mi vida, visible o invisible.",
         "noche": "Al entrar en el descanso, siembro ideas de plenitud, salud y alegría en mi subconsciente."},
    19: {"mañana": "Permanezco firme en mis convicciones. Mi fe es clara, constante y confiada.",
         "noche": "Durante el sueño, mi mente sigue trabajando a favor de mis deseos y aspiraciones más elevadas."},
    20: {"mañana": "Suelto lo que me preocupa y recibo con apertura nuevas soluciones y caminos.",
         "noche": "Me inundo de pensamientos de verdad, alegría, esperanza y claridad antes de dormir."},
    21: {"mañana": "Planto pensamientos positivos en mi mente cada día, y mi realidad florece con ellos.",
         "noche": "Mi subconsciente cuida de mí, reestableciendo equilibrio, salud y bienestar continuo."},
}

st.set_page_config(page_title="42 Afirmaciones: 21 días", layout="centered")
st.title("🌄 Afirmaciones Mañana y Noche")

# Inicializar progreso si no existe
if 'progreso' not in st.session_state:
    st.session_state.progreso = {d: {"mañana": False, "noche": False} for d in range(1, 22)}

# Selección de día y momento
dia = st.number_input("Selecciona el día (1-21):", 1, 21, 1)
momento = st.radio("¿Cuál afirmación deseas ver?", ("mañana", "noche"))

# Mostrar afirmación correspondiente
if afirmaciones_dia.get(dia):
    afirmacion = afirmaciones_dia[dia][momento]
    st.subheader(f"Día {dia} - {'🌞' if momento == 'mañana' else '🌙'} Afirmación de la {momento.capitalize()}")
    st.markdown(f"> *{afirmacion}*")
    st.success("Lee esta afirmación en voz alta, repítela con convicción y siéntela como si ya fuera real.")

    # Checkbox de progreso
    checkbox_key = f"check_{dia}_{momento}"
    completado = st.checkbox("✅ Marcar este momento como completado", value=st.session_state.progreso[dia][momento], key=checkbox_key)
    st.session_state.progreso[dia][momento] = completado
else:
    st.warning("Selecciona un día válido entre 1 y 21.")

# Mostrar progreso general
total_completado = sum([1 for d in st.session_state.progreso for m in ["mañana", "noche"] if st.session_state.progreso[d][m]])
st.progress(total_completado / 42.0)
st.caption(f"Progreso: {total_completado} de 42 sesiones completadas")

# Botón de ayuda práctica diaria
if st.button("¿Cómo debo hacer la práctica diaria?"):
    st.markdown("""
### 🧘‍♀️ Cómo debo hacer la práctica diaria:

1. Practica al despertar y antes de dormir.
2. Relájate profundamente antes de comenzar.
3. Repite la afirmación con emoción y convicción.
4. Siéntela como una verdad presente.
5. Visualiza el resultado cumplido.
6. Termina con gratitud.
""")

# Botón para abrir guía extendida
if st.button("🧠 Guía completa para sembrar ideas en el subconsciente"):
    with st.expander("1. Vigila tus pensamientos y palabras"):
        st.write("Tu subconsciente graba literalmente cada palabra y pensamiento. Usa palabras constructivas y evita frases como 'no puedo'.")
    with st.expander("2. Usa afirmaciones y decretos con convicción"):
        st.write("Rompe patrones mentales negativos repitiendo afirmaciones en voz alta, lenta y con sentimiento.")
    with st.expander("3. Formula tus peticiones correctamente"):
        st.write("Haz afirmaciones como: 'por la gracia y de una manera perfecta'. No supliques: agradece como si ya hubieras recibido.")
    with st.expander("4. Visualiza y usa la imaginación"):
        st.write("Imagina el resultado cumplido. Sé constante y específico. Usa la imaginación como si ya lo vivieras.")
    with st.expander("5. Siente la fe y la convicción"):
        st.write("Cree que tu deseo ya se ha cumplido. No uses frases débiles. Reafirma tu fe con emoción y certeza.")
    with st.expander("6. Utiliza el estado de somnolencia"):
        st.write("Poco antes de dormir o al despertar, repite afirmaciones o visualiza. El subconsciente está más receptivo.")
    with st.expander("7. Practica la relajación y el no esfuerzo"):
        st.write("No fuerces mentalmente. Relájate y confía en la Inteligencia Infinita. La calma activa el poder interior.")
    with st.expander("8. Sé persistente y no desistas"):
        st.write("Una vez hecha la petición, mantén tu posición. No te contradigas ni dudes.")
    with st.expander("9. Pide guía divina/intuición"):
        st.write("Pide dirección clara y actúa según la intuición. La guía llega en pensamientos, libros, personas.")
    with st.expander("10. Libérate de obstáculos mentales y emocionales"):
        st.write("Perdona, elimina el rencor, deja de criticar y supera los miedos. Estos bloquean tu bien.")
    with st.expander("11. Da y recibe con alegría"):
        st.write("Dar activa el flujo de la abundancia. Da con alegría y recibe con gratitud.")
    with st.expander("12. Mantén tu mente en armonía"):
        st.write("Mantén pensamientos de paz, salud y fe. La armonía interior se refleja en el exterior.")
