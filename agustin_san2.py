import streamlit as st
import random
import re

# ────────────────────────────────
#  LISTA DE FILÓSOFOS INCLUIDA
# ────────────────────────────────
FILOSOFOS = [
    {"filosofo": "Tales", "nacimiento": -624},
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
#  UTILIDADES
# ────────────────────────────────
AC_PAT = re.compile(r'\b(a\.?\s*c\.?|ac|a\s*c)\b', re.IGNORECASE)
DC_PAT = re.compile(r'\b(d\.?\s*c\.?|dc|d\s*c)\b', re.IGNORECASE)
DIGITS_PAT = re.compile(r'-?\d{1,4}')

def to_human(year: int) -> str:
    if year < 0:
        return f"{abs(year)} a. C."
    elif year == 0:
        return "1 d. C."
    return f"{year} d. C."

def parse_user_year(text: str):
    """
    Admite entradas como: '-427', '427 a.C.', '427 ac', '370 d.C.', '370', etc.
    Devuelve un int (años a.C. negativos) o None si no entiende.
    """
    if not text:
        return None
    s = text.strip().lower()
    # Marca explícita a.C. -> negativo
    if AC_PAT.search(s):
        m = DIGITS_PAT.search(s)
        if not m: 
            return None
        y = int(m.group())
        if y == 0:
            return -1
        return -abs(y)
    # Marca explícita d.C. -> positivo
    if DC_PAT.search(s):
        m = DIGITS_PAT.search(s)
        if not m:
            return None
        y = int(m.group())
        return 1 if y == 0 else abs(y)
    # Si solo hay número con posible signo
    m = DIGITS_PAT.search(s)
    if not m:
        return None
    y = int(m.group())
    # Evita 0 histórico
    if y == 0:
        return 1
    return y

def nueva_pregunta():
    return random.choice(FILOSOFOS)

# ────────────────────────────────
#  APP
# ────────────────────────────────
st.set_page_config(page_title="Quiz Filosofía (respuesta escrita)", page_icon="✍️", layout="centered")
st.title("✍️ Quiz de Filosofía: escribe el año de nacimiento")
st.write("Escribe el año (ej.: `-427` o `427 a.C.`). **+1** si aciertas, **−1** si fallas.")

# Estado inicial
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.hechas = 0
    st.session_state.objetivo = 10
    st.session_state.preg = nueva_pregunta()
    st.session_state.feedback = ""
    st.session_state.last_correct = None

# Panel superior
colA, colB = st.columns(2)
with colA:
    rondas = st.slider("Número de preguntas", 5, len(FILOSOFOS), 10)
with colB:
    if st.button("🔄 Reiniciar partida", use_container_width=True):
        st.session_state.score = 0
        st.session_state.hechas = 0
        st.session_state.objetivo = rondas
        st.session_state.preg = nueva_pregunta()
        st.session_state.feedback = ""
        st.session_state.last_correct = None

st.markdown(f"**Puntuación:** {st.session_state.score} | **Pregunta {st.session_state.hechas + 1}/{st.session_state.objetivo}**")

# Pregunta
st.subheader(f"¿En qué año nació **{st.session_state.preg['filosofo']}**?")

resp = st.text_input("Escribe aquí el año (ej.: -427, 427 a.C., 370 d.C.)", value="", label_visibility="collapsed")

col1, col2 = st.columns([1,1])

with col1:
    if st.button("Responder ✅", use_container_width=True):
        year_user = parse_user_year(resp)
        if year_user is None:
            st.session_state.feedback = "❓ No he entendido el año. Usa formatos como `-427`, `427 a.C.`, `370 d.C.`."
        else:
            correcto = st.session_state.preg["nacimiento"]
            if year_user == correcto:
                st.session_state.score += 1
                st.session_state.feedback = f"✅ ¡Correcto! Era **{to_human(correcto)}**. (+1)"
            else:
                st.session_state.score -= 1
                st.session_state.feedback = f"❌ Incorrecto. Era **{to_human(correcto)}**. (−1)"
            st.session_state.last_correct = correcto

with col2:
    if st.button("Siguiente ➡️", use_container_width=True):
        # avanzar de ronda solo si ya hubo feedback (evita saltar sin intentar)
        if st.session_state.feedback == "":
            st.warning("Primero intenta responder.")
        else:
            st.session_state.hechas += 1
            if st.session_state.hechas >= st.session_state.objetivo:
                st.balloons()
                st.success(f"🎉 ¡Fin! Puntuación final: **{st.session_state.score}**")
                # reset suave
                st.session_state.score = 0
                st.session_state.hechas = 0
            st.session_state.preg = nueva_pregunta()
            st.session_state.feedback = ""
            st.session_state.last_correct = None

# Feedback
if st.session_state.feedback:
    st.info(st.session_state.feedback)

# Ayudita opcional (pista de rango por época, desactivado por defecto)
with st.expander("💡 ¿Necesitas una pista? (opcional)"):
    st.markdown("""
- **Antigua (Grecia/Roma):** aprox. 600 a. C. → 400 d. C.  
- **Medieval:** aprox. 400 → 1500 d. C.  
- **Baja Edad Media / Renacimiento temprano:** 1200 → 1500 d. C.  
""")
