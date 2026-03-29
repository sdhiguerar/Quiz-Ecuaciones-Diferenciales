import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ── Configuración de página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Quiz · Ecuaciones Diferenciales",
    page_icon="📐",
    layout="centered"
)

# ── Estilos ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif;
}

/* Fondo general */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: #e8e8e8;
}

/* Tarjeta principal */
.card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    backdrop-filter: blur(10px);
    margin-bottom: 1.5rem;
}

/* Badge de puntaje */
.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #f7971e, #ffd200);
    color: #1a1a1a;
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    padding: 0.5rem 2rem;
    border-radius: 12px;
    margin: 1rem 0;
}

.correct   { color: #56e39f; font-weight: 600; }
.incorrect { color: #ff6b6b; font-weight: 600; }

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #f7971e, #ffd200) !important;
    color: #1a1a1a !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(247,151,30,0.4) !important;
}

/* Radio buttons */
.stRadio > div { gap: 0.4rem; }

/* Inputs */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 8px !important;
    color: #fff !important;
}

/* Tabla del dashboard */
.dataframe { font-size: 0.9rem; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15,32,39,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Divider */
hr { border-color: rgba(255,255,255,0.1); }
</style>
""", unsafe_allow_html=True)

# ── Datos del quiz ────────────────────────────────────────────────────────────
PREGUNTAS = [
    {
        "enunciado": (
            "**Pregunta 1.** ¿Cuál es la solución general de la ecuación diferencial "
            "ordinaria de primer orden $\\dfrac{dy}{dx} = 2x$?"
        ),
        "opciones": [
            "A) $y = x^2$",
            "B) $y = x^2 + C$",
            "C) $y = 2x^2 + C$",
            "D) $y = \\frac{x^2}{2} + C$",
        ],
        "correcta": "B) $y = x^2 + C$",
    },
    {
        "enunciado": (
            "**Pregunta 2.** La ecuación diferencial $\\dfrac{dy}{dx} + P(x)\\,y = Q(x)$ "
            "es de tipo:"
        ),
        "opciones": [
            "A) Separable",
            "B) No lineal de primer orden",
            "C) Lineal de primer orden",
            "D) Exacta",
        ],
        "correcta": "C) Lineal de primer orden",
    },
]

PUNTOS_POR_PREGUNTA = 2.5
ARCHIVO_REGISTROS  = "registros_quiz.csv"
CLAVE_PROFESOR     = "profe2024"   # ← cambia esta clave

# ── Utilidades de persistencia ────────────────────────────────────────────────
def cargar_registros():
    if os.path.exists(ARCHIVO_REGISTROS):
        return pd.read_csv(ARCHIVO_REGISTROS)
    return pd.DataFrame(columns=[
        "Fecha y Hora", "Nombre", "Calificación",
        "Respuesta P1", "Correcta P1",
        "Respuesta P2", "Correcta P2",
        "Juramento"
    ])

def guardar_registro(fila: dict):
    df = cargar_registros()
    df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
    df.to_csv(ARCHIVO_REGISTROS, index=False)

# ── Navegación por session_state ──────────────────────────────────────────────
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"   # inicio | quiz | resultado | profesor

# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR — acceso al panel del profesor
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🔒 Panel del Profesor")
    clave = st.text_input("Contraseña", type="password", key="clave_sidebar")
    if st.button("Acceder", key="btn_acceder"):
        if clave == CLAVE_PROFESOR:
            st.session_state.pantalla = "profesor"
            st.rerun()
        else:
            st.error("Contraseña incorrecta.")

    if st.session_state.pantalla == "profesor":
        if st.button("← Volver al quiz"):
            st.session_state.pantalla = "inicio"
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# PANTALLA: INICIO
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.pantalla == "inicio":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 📐 Quiz · Ecuaciones Diferenciales")
    st.markdown("Responde las **2 preguntas** de selección múltiple. Cada respuesta correcta vale **2.5 puntos**.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 👤 Datos del estudiante")
    nombre = st.text_input("Nombre completo", placeholder="Ej. María González")

    st.markdown("---")
    st.markdown("### ✋ Declaración de honestidad académica")
    juramento = st.checkbox(
        "Declaro formalmente, bajo mi palabra de honor, que las respuestas "
        "presentadas en este quiz son de mi autoría y que no recibí ayuda "
        "no autorizada de ninguna persona o medio durante su realización."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Iniciar quiz →"):
        if not nombre.strip():
            st.warning("Por favor ingresa tu nombre completo.")
        elif not juramento:
            st.warning("Debes aceptar la declaración de honestidad académica para continuar.")
        else:
            st.session_state.nombre   = nombre.strip()
            st.session_state.juramento = juramento
            st.session_state.pantalla = "quiz"
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# PANTALLA: QUIZ
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.pantalla == "quiz":

    st.markdown(f"## 📝 Quiz — {st.session_state.nombre}")
    respuestas = []

    for i, p in enumerate(PREGUNTAS):
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(p["enunciado"])
        resp = st.radio(
            f"Selecciona tu respuesta para la pregunta {i+1}:",
            p["opciones"],
            key=f"resp_{i}",
            index=None
        )
        respuestas.append(resp)
        st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Enviar respuestas ✓"):
        if any(r is None for r in respuestas):
            st.warning("Por favor responde todas las preguntas antes de enviar.")
        else:
            calificacion = 0.0
            resultados   = []
            for i, (p, r) in enumerate(zip(PREGUNTAS, respuestas)):
                correcta = (r == p["correcta"])
                if correcta:
                    calificacion += PUNTOS_POR_PREGUNTA
                resultados.append({
                    "respuesta": r,
                    "correcta":  correcta,
                    "esperada":  p["correcta"]
                })

            # Guardar en CSV
            guardar_registro({
                "Fecha y Hora":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nombre":        st.session_state.nombre,
                "Calificación":  calificacion,
                "Respuesta P1":  resultados[0]["respuesta"],
                "Correcta P1":   resultados[0]["correcta"],
                "Respuesta P2":  resultados[1]["respuesta"],
                "Correcta P2":   resultados[1]["correcta"],
                "Juramento":     "Sí" if st.session_state.juramento else "No",
            })

            st.session_state.calificacion = calificacion
            st.session_state.resultados   = resultados
            st.session_state.pantalla     = "resultado"
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# PANTALLA: RESULTADO
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.pantalla == "resultado":

    cal = st.session_state.calificacion
    res = st.session_state.resultados

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"## 🎓 Resultado — {st.session_state.nombre}")

    emoji = "🏆" if cal == 5.0 else ("👍" if cal >= 2.5 else "📚")
    st.markdown(f"### {emoji} Tu calificación:")
    st.markdown(f"<div class='score-badge'>{cal:.1f} / 5.0</div>", unsafe_allow_html=True)
    st.markdown("---")

    for i, (p, r) in enumerate(zip(PREGUNTAS, res)):
        st.markdown(p["enunciado"])
        if r["correcta"]:
            st.markdown(f"<span class='correct'>✅ Correcto — {r['respuesta']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span class='incorrect'>❌ Incorrecto — respondiste: {r['respuesta']}</span>", unsafe_allow_html=True)
            st.markdown(f"<span class='correct'>Respuesta correcta: {r['esperada']}</span>", unsafe_allow_html=True)
        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Realizar otro intento"):
        for k in ["nombre", "juramento", "calificacion", "resultados"]:
            st.session_state.pop(k, None)
        st.session_state.pantalla = "inicio"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# PANTALLA: PANEL DEL PROFESOR
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.pantalla == "profesor":

    st.markdown("## 📊 Panel del Profesor — Registros del Quiz")

    df = cargar_registros()

    if df.empty:
        st.info("Aún no hay registros de estudiantes.")
    else:
        # Métricas resumen
        col1, col2, col3 = st.columns(3)
        col1.metric("Total estudiantes", len(df))
        col2.metric("Promedio", f"{df['Calificación'].mean():.2f}")
        col3.metric("Nota máxima", f"{df['Calificación'].max():.1f}")

        st.markdown("### 📋 Tabla completa")
        st.dataframe(df, use_container_width=True)

        # Descarga CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar registros en CSV",
            data=csv,
            file_name="registros_quiz_ecuaciones.csv",
            mime="text/csv"
        )
