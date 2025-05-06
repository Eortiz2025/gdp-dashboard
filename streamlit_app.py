import streamlit as st

# Afirmaciones clasificadas por día y momento (mañana/noche)
afirmaciones_dia = {
    1: {"mañana": "Mi subconsciente es un fiel servidor, y yo le doy órdenes convenientes.",
        "noche": "Cada uno de mis pensamientos es una causa y una condición, y cada condición es un efecto. Tomo responsabilidad de mis pensamientos."},
    2: {"mañana": "Cada palabra que digo y cada cosa que pienso se graba dentro de mi subconsciente y se realiza en detalles sorprendentes.",
        "noche": "Cuando mi mente piensa correctamente, cuando entiendo la verdad, cuando los pensamientos depositados en mi subconsciente son constructivos, armoniosos y llenos de paz, el poder de trabajo de mi subconsciente responde."},
    3: {"mañana": "Yo rompo y demuelo los discos malos y viejos de mi subconsciente y los sustituyo por los nuevos y bonitos.",
        "noche": "Soy como el capitán de mi buque, dando órdenes correctas (pensamientos e imágenes) a mi mente subconsciente."},
    4: {"mañana": "Yo quiebro y demuelo (por mis palabras) todo lo que, dentro de mi subconsciente, es falso. Todo eso regresará a la nada.",
        "noche": "Yo nunca uso los términos 'yo no puedo hacerlo', 'no puedo comprarlo'. Mi mente subconsciente lo acatará literalmente. Yo digo: 'Puedo hacer todas las cosas a través del poder de mi mente subconsciente'."},
    5: {"mañana": "Ahora, grabo los nuevos discos por el poder de Cristo que hay en mí, que es la salud, la riqueza, el amor y la expresión perfecta de mi Ser. Ahí está la cuadratura de mi vida, el juego completo.",
        "noche": "La ley de mi vida es la ley de creer en algo. Mi creencia es un pensamiento en mi mente. Yo creo en el poder de mi mente subconsciente para curar, inspirar, fortalecer y prosperar. A medida que aumento mi fe, mis resultados aumentan también."},
    6: {"mañana": "Yo puedo cambiar las condiciones de mi vida cambiando las palabras que utilizo. La muerte y la Vida son el poder de mi lengua.",
        "noche": "Yo cambio mis pensamientos, y así cambio mi destino."},
    7: {"mañana": "Yo no juzgo a fin de no ser juzgado. Aquello que deseo para el prójimo, eso es lo que atraigo para mí mismo.",
        "noche": "Tan pronto mi mente subconsciente acepta una idea, comienza a ejecutarla. La ley de mi subconsciente puede trabajar del mismo modo para ideas buenas o malas."},
    8: {"mañana": "La indecisión es una piedra de obstáculo para mí; por eso repito: 'Yo siempre tengo la inspiración directa, y tomo rápidamente las buenas decisiones'.",
        "noche": "Mi mente consciente es el vigilante en la puerta, que tiene como función fundamental proteger mi mente subconsciente de las impresiones falsas."},
    9: {"mañana": "Reconozco que es mucho más fácil temer que tener fe, por eso hago el esfuerzo de mi voluntad para tener fe.",
        "noche": "Una sugerencia no tiene poder por sí misma, excepto si es mentalmente aceptada por mí. Yo tengo la capacidad para elegir, y elijo la vida, elijo el amor, elijo la salud."},
    10: {"mañana": "Todo lo que se halla en discordancia a mi alrededor se corresponde con una desarmonía mental dentro de mí, y yo elijo la armonía.",
        "noche": "Debo dar a mi subconsciente solamente las sugestiones que curan, que elevan y que me inspiran a altos ideales. Mi mente subconsciente no entiende una broma, sino que toma mis palabras al pie de la letra."},
    11: {"mañana": "Yo niego la pérdida; sé que no hay pérdida alguna en el Entendimiento Divino. Yo libero el rencor y el rechazo a perdonar, que cierran las puertas de mi bien.",
        "noche": "Cualquiera que sea la premisa que mi mente consciente acepta como verdadera, esto determina la conclusión a la cual llega mi mente subconsciente."},
    12: {"mañana": "Yo pido directrices nítidas y el camino me es trazado, con facilidad y lleno de éxito.",
        "noche": "Mi subconsciente no discute ni me replica. Yo estoy bloqueando mi propia bondad y mi propio éxito con pensamientos negativos, pero ahora elijo pensar de manera positiva."},
    13: {"mañana": "Mi miedo puede superarse por medio de la palabra pronunciada o por el tratamiento.",
        "noche": "Para llevar a cabo mi deseo y terminar con la frustración, me digo: 'La inteligencia infinita que me sugirió este propósito me guía y me revela el plan perfecto'."},
    14: {"mañana": "Practico la Presencia de Dios a cada minuto. Le reconozco en todas las direcciones, porque nada es insignificante, ni demasiado importante.",
        "noche": "Mi subconsciente nunca duerme, nunca descansa. Está siempre trabajando. Controla mis funciones vitales."},
    15: {"mañana": "Mi resistencia o el querer elegir mi propio camino limitan mi fe y paralizan la manifestación. Yo me entrego a la Inteligencia Infinita, diciendo '¡Mis caminos y no tus caminos!'.",
        "noche": "Le digo a mi subconsciente antes de dormirme que quiero que se realice cierto asunto, y me sorprenderé al descubrir que mis fuerzas internas empiezan a trabajar."},
    16: {"mañana": "Tengo la conciencia del oro, de la riqueza, y eso atrae la riqueza a mi vida.",
        "noche": "Lo que yo imprimo en mi mente subconsciente, se proyecta en la pantalla del espacio como acontecimientos y experiencias. Por lo tanto, escojo cuidadosamente las mejores ideas y los pensamientos."},
    17: {"mañana": "Al formular mis peticiones, empiezo por el fin, declarando haber recibido ya. Antes de que yo llame, Él responderá.",
        "noche": "Para obtener los efectos deseados, los imagino y los siento una realidad, esperando que el principio vital infinito responda a mi petición consciente."},
    18: {"mañana": "Doy gracias constantemente por aquello que ya he recibido. El hecho de alegrarme mientras aún estoy en el desierto abre la vía de mi liberación.",
        "noche": "El estado de somnolencia antes de dormir o poco antes de despertar es el mejor momento para impregnar mi subconsciente porque en este momento tiene el mayor grado de lucidez."},
    19: {"mañana": "Yo no vacilo en mi fe. Aquel que vacila no pensará que recibirá lo que es del Señor. Yo no transijo nunca. Una vez que he hecho lo necesario, mantengo mi posición.",
        "noche": "La acción dinámica de mi mente subconsciente continúa y es mayor durante el sueño. Puedo darle a mi mente subconsciente un buen trabajo mientras caigo en la somnolencia y ella lo ejecutará."},
    20: {"mañana": "Cuando yo me libero de mi problema y entrego la carga, obtengo una manifestación instantánea.",
        "noche": "Lleno mi mente con la gran verdad vital y avanzo con luminosa alegría."},
    21: {"mañana": "Yo soy el jardinero que está plantando semillas (pensamientos) en mi subconsciente basado en mi pensamiento habitual. Tal como siembro, así cosecharé.",
        "noche": "Mi subconsciente busca preservar mi vida y restaurar mi salud a cualquier precio."},
}

st.set_page_config(page_title="42 Afirmaciones: 21 días", layout="centered")
st.title("🌄 Afirmaciones Mañana y Noche")

# Selección de día y momento
dia = st.number_input("Selecciona el día (1-21):", 1, 21, 1)
momento = st.radio("¿Cuál afirmación deseas ver?", ("mañana", "noche"))

# Mostrar afirmación correspondiente
if afirmaciones_dia.get(dia):
    afirmacion = afirmaciones_dia[dia][momento]
    st.subheader(f"Día {dia} - {'🌞' if momento == 'mañana' else '🌙'} Afirmación de la {momento.capitalize()}")
    st.markdown(f"> *{afirmacion}*")
    st.success("Lee esta afirmación en voz alta, repítela con convicción y siéntela como si ya fuera real.")
else:
    st.warning("Selecciona un día válido entre 1 y 21.")
