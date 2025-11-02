import streamlit as st
import random

# ────────────────────────────────
#  LISTA DE FILÓSOFOS INCLUIDA
# ────────────────────────────────
FILOSOFOS = [
    {"filosofo": "Tales", "nacimiento": -24},
    {"filosofo": "Anaximandro", "nacimiento": -610},
    {"filosofo": "Anaxímenes", "nacimiento": -590},
    {"filosofo": "Pitágoras", "nacimiento": -570},
    {"filosofo": "Heráclito", "nacimiento": -540},
    {"filosofo": "Parménides", "nacimiento": -540},
    {"filosofo": "Empédocles", "nacimiento": -495},
    {"filosofo": "Anaxágoras", "nacimiento": -500},
    {"filosofo": "Demócrito", "nacimiento": -460},
    {"filosofo": "Protágoras", "nacimiento": -485},
    {"filosofo": "Gorgias", "nacimiento": -483},
    {"filosofo": "Sócrates", "nacimiento": -470},
    {"filosofo": "Aspasia", "nacimiento": -470},
    {"filosofo": "Platón", "nacimiento": -427},
    {"filosofo": "Aristóteles", "nacimiento": -384},
    {"filosofo": "Hipatia", "nacimiento": 370},
    {"filosofo": "Euclides", "nacimiento": -325},
    {"filosofo": "Arquímedes", "nacimiento": -287},
    {"filosofo": "Claudio Ptolomeo", "nacimiento": 100},
    {"filosofo": "Eratóstenes de Cirene", "nacimiento": -276},
    {"filosofo": "Al-Khwarizmi", "nacimiento": 780},
    {"filosofo": "Avicena", "nacimiento": 980},
    {"filosofo": "Averroes", "nacimiento": 1126},
    {"filosofo": "Agustín de Hipona", "nacimiento": 354},
    {"filosofo": "Tomás de Aquino", "nacimiento": 1225},
    {"filosofo": "Ockham", "nacimiento": 1300},
    {"filosofo": "Hildegard von Bingen", "nacimiento": 1098},
    {"filosofo": "Christine de Pizan", "nacimiento": 1364},
    {"filosofo": "Isabel de Villena", "nacimiento": 1430},
]

# ────────────────────────────────
#  FUNCIONES AUXILIARES
# ────────────────────────────────
def format_year(year):
    if year < 0:
        return f"{abs(year)} a.C."
    else:
        return f"{year} d.C."

def generar_distractores(year_correcto, k=3):
    """Genera k años distintos del correcto."""
    distractores = set()
    while len(distractores) < k:
        offset = random.choice([5, 10, 20, 30, 50, 100, 200]) * random.choice([-1, 1])
        nuevo = year_correcto + offset
        if nuevo != year_correcto and nuevo != 0:
            distractores.add(nuevo)
    return list(distractores)

def nueva_pregunta():
    item = random.choice(FILOSOFOS)
    correcto = item["nacimiento"]
    opciones = [correcto] + generar_distractores(correcto, 3)
    random.shuffle(opciones)
    return {"filosofo": item["filosofo"], "correcto": correcto, "opciones": opciones}

# ────────────────────────────────
#  INTERFAZ STREAMLIT
# ────────────────────────────────
st.set_page_config(page_title="Quiz Filosofía", page_icon="🧠", layout="centered")
st.title("🧠 Juego: Historia de la Filosofía – Fechas de nacimiento")
st.write("Adivina la fecha de nacimiento de cada filósofo. +1 punto si aciertas, −1 si fallas.")

# Inicialización de sesión
if "score" not in st.session_state:
    st.session_state["score"] = 0
    st.session_state["hechas"] = 0
    st.session_state["objetivo"] = 10
    st.session_state["pregunta"] = nueva_pregunta()
    st.session_state["respondida"] = False

# Configuración
colA, colB = st.columns([1, 1])
with colA:
    rondas = st.slider("Número de preguntas", 5, len(FILOSOFOS), 10)
with colB:
    if st.button("🔄 Reiniciar partida", use_container_width=True):
        st.session_state["score"] = 0
        st.session_state["hechas"] = 0
        st.session_state["objetivo"] = rondas
        st.session_state["pregunta"] = nueva_pregunta()
        st.session_state["respondida"] = False

# Mostrar estado
st.markdown(f"**Puntuación:** {st.session_state['score']} | **Pregunta {st.session_state['hechas']+1}/{st.session_state['objetivo']}**")

# Pregunta actual
preg = st.session_state["pregunta"]
st.subheader(f"¿En qué año nació **{preg['filosofo']}**?")
opciones_etq = [format_year(o) for o in preg["opciones"]]
idx_sel = st.radio("Elige una opción:", list(range(4)), format_func=lambda i: opciones_etq[i])

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Responder ✅", use_container_width=True, disabled=st.session_state["respondida"]):
        elegida = preg["opciones"][idx_sel]
        if elegida == preg["correcto"]:
            st.success("¡Correcto! +1 punto")
            st.session_state["score"] += 1
        else:
            st.error(f"Incorrecto. La respuesta era **{format_year(preg['correcto'])}**. −1 punto")
            st.session_state["score"] -= 1
        st.session_state["respondida"] = True

with col2:
    if st.button("Siguiente ➡️", use_container_width=True):
        if not st.session_state["respondida"]:
            st.warning("Primero pulsa **Responder**.")
        else:
            st.session_state["hechas"] += 1
            if st.session_state["hechas"] >= st.session_state["objetivo"]:
                st.balloons()
                st.success(f"¡Fin del juego! Puntuación final: {st.session_state['score']}")
                st.session_state["score"] = 0
                st.session_state["hechas"] = 0
            st.session_state["pregunta"] = nueva_pregunta()
            st.session_state["respondida"] = False
