import streamlit as st

st.set_page_config(page_title="Guía 9 Días de Activación Subconsciente", layout="centered")
st.title("🧠 Guía de 9 Días para Activar tu Mente Subconsciente")

# Texto dividido por pasos
guia_9_dias = {
    1: {
        "titulo": "Paso 1: Comprende la Naturaleza de tu Mente",
        "contenido": """
Tienes dos niveles de mente: la consciente (que piensa y razona) y la subconsciente (que acepta y crea).  
Tu subconsciente no discute; acepta lo que tu mente consciente le imprime con convicción.  
Tu pensamiento habitual es la causa; tus condiciones (salud, dinero, relaciones) son los efectos."
        """
    },
    2: {
        "titulo": "Paso 2: Define Clara y Específicamente tu Deseo o Meta",
        "contenido": """
Ten una idea o propósito definido: salud, abundancia, relaciones, solución específica.  
Sé detallado. Visualiza cómo se ve y se siente tu deseo ya cumplido."
        """
    },
    3: {
        "titulo": "Paso 3: Impresiona tu Mente Subconsciente (Técnicas)",
        "contenido": """
Relajación/Somnolencia: practica en calma, al despertar y antes de dormir.  
Visualización: imagina tu deseo cumplido como una película mental.  
Afirmaciones: repite frases positivas como: “Riqueza”, “Gracias Padre por mi prosperidad”.  
Agradecimiento anticipado: siente gratitud como si ya lo hubieras recibido.  
Argumentación: razona con fe: Mi mente subconsciente sabe cómo lograr esto.  
Plegaria: no formal, sino sincera. Pide y cree que ya has recibido."
        """
    },
    4: {
        "titulo": "Paso 4: Cultiva la Fe y la Convicción",
        "contenido": """
Cree que tu subconsciente está actuando a tu favor ahora.  
Siente que tu deseo ya es real, aquí y ahora.  
La fe con entendimiento es más poderosa que la fe ciega."
        """
    },
    5: {
        "titulo": "Paso 5: Evita el Esfuerzo Mental y el Conflicto",
        "contenido": """
No intentes forzar resultados con voluntad.  
El esfuerzo indica duda. Relájate y confía.  
Repite interiormente: Esto también pasará."
        """
    },
    6: {
        "titulo": "Paso 6: Elimina los Obstáculos Internos",
        "contenido": """
Identifica y reemplaza pensamientos negativos.  
Perdona: la crítica y el resentimiento bloquean tu bien.  
No aceptes sugestiones negativas externas.  
Cambia hábitos destructivos sustituyéndolos por pensamientos elevados."
        """
    },
    7: {
        "titulo": "Paso 7: Sé Constante y Persistente",
        "contenido": """
La repetición diaria con fe y emoción es clave.  
Si no ves resultados rápidos, continúa con paciencia y alegría."
        """
    },
    8: {
        "titulo": "Paso 8: Vive la Realidad de tu Deseo Ahora",
        "contenido": """
Siéntelo ahora. Vive como si ya lo tuvieras.  
Permite que tu subconsciente lo haga realidad."
        """
    },
    9: {
        "titulo": "Paso 9: Busca un Propósito Mayor y Sirve a Otros",
        "contenido": """
Alinea tus metas con el bien de otros.  
El verdadero éxito incluye crecimiento espiritual, servicio y comprensión."
        """
    }
}

for i in range(1, 10):
    st.markdown(f"## {guia_9_dias[i]['titulo']}")
    st.markdown(guia_9_dias[i]['contenido'])
    st.markdown("---")

st.success("✨ Lee cada paso con calma. Reflexiona, vuelve cuando lo necesites, y aplica diariamente en tu vida.")
