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

# ── Estilos ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Sans+3:wght@300;400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
    color: #000000;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    color: #000000;
}

.stApp {
    background: linear-gradient(160deg, #f0f4ff 0%, #fef6fb 50%, #f0fff4 100%);
}

.card {
    background: #ffffff;
    border: 1px solid #e0e7ff;
    border-radius: 16px;
    padding: 2rem 2.5rem;
    box-shadow: 0 4px 24px rgba(99,102,241,0.07);
    margin-bottom: 1.5rem;
}

.score-badge {
    display: inline-block;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: #ffffff !important;
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    padding: 0.5rem 2rem;
    border-radius: 12px;
    margin: 1rem 0;
}

.correct   { color: #16a34a !important; font-weight: 600; }
.incorrect { color: #dc2626 !important; font-weight: 600; }

.pending-box {
    background: #fef9c3;
    border: 1px solid #fde68a;
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    color: #78350f !important;
    font-size: 1.05rem;
    margin-top: 1rem;
}

.btn-consultar > div > button {
    background: linear-gradient(135deg, #0ea5e9, #6366f1) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 1rem !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(99,102,241,0.35) !important;
}

.stRadio > div { gap: 0.4rem; }
.stRadio label { color: #000000 !important; }

.stTextInput > div > div > input {
    background: #f8faff !important;
    border: 1px solid #c7d2fe !important;
    border-radius: 8px !important;
    color: #000000 !important;
}

.stCheckbox label { color: #000000 !important; }

section[data-testid="stSidebar"] {
    background: #f8f7ff !important;
    border-right: 1px solid #e0e7ff;
}
section[data-testid="stSidebar"] * {
    color: #000000 !important;
}

p, span, div, label, .stMarkdown, .stText,
.stRadio div, .stCheckbox div, [class*="stMarkdown"] * {
    color: #000000 !important;
}

hr { border-color: #e0e7ff; }

[data-testid="metric-container"] {
    background: #f0f4ff;
    border-radius: 10px;
    padding: 0.8rem;
    border: 1px solid #e0e7ff;
}
</style>
""", unsafe_allow_html=True)

# ── Preguntas ─────────────────────────────────────────────────────────────────
PREGUNTAS = [
    {
        "enunciado": (
            "**Pregunta 7.** Considere la ecuación diferencial no homogénea\n\n"
            "$$y'' - 3y' + 2y = e^{x}.$$ \n\n"
            "Usando el método de coeficientes constantes, ¿cuál es la solución general?"
        ),
        "opciones": [
            "A) $y = C_1 e^{x} + C_2 e^{2x} + \\frac{1}{2} e^{x}$",
            "B) $y = C_1 e^{x} + C_2 e^{2x} + x e^{x}$",
            "C) $y = C_1 e^{-x} + C_2 e^{-2x} + x e^{x}$",
            "D) $y = C_1 e^{x} + C_2 e^{2x} + e^{x}$",
        ],
        "correctas": ["B) $y = C_1 e^{x} + C_2 e^{2x} + x e^{x}$"],
        "correcta_display": "B) $y = C_1 e^{x} + C_2 e^{2x} + x e^{x}$",
    },
    {
        "enunciado": (
            "**Pregunta 8.** Considere la ecuación diferencial\n\n"
            "$$x^2 y'' - 3x y' + 4y = 0, \\quad x>0,$$\n\n"
            "y se sabe que una solución es $y_1 = x^2$. "
            "Usando reducción de orden, ¿cuál es una segunda solución linealmente independiente $y_2$?"
        ),
        "opciones": [
            "A) $y_2 = x^2 \\ln x$",
            "B) $y_2 = x^3$",
            "C) $y_2 = x \\ln x$",
            "D) $y_2 = x^2 e^{x}$",
        ],
        "correctas": ["A) $y_2 = x^2 \\ln x$"],
        "correcta_display": "A) $y_2 = x^2 \\ln x$",
    }
]

PUNTOS_POR_PREGUNTA = 2.5
ARCHIVO_REGISTROS   = "registros_quiz.csv"
ARCHIVO_CONTROL     = "control_quiz.csv"
CLAVE_PROFESOR      = "UAN2026"

# ── Utilidades ────────────────────────────────────────────────────────────────
def cargar_registros():
    if os.path.exists(ARCHIVO_REGISTROS):
        return pd.read_csv(ARCHIVO_REGISTROS, dtype={"Documento": str})
    return pd.DataFrame(columns=[
        "Fecha y Hora", "Nombre", "Documento", "Calificación",
        "Respuesta P1", "Correcta P1",
        "Respuesta P2", "Correcta P2",
        "Juramento"
    ])

def guardar_registro(fila: dict):
    df = cargar_registros()
    df = pd.concat([df, pd.DataFrame([fila])], ignore_index=True)
    df.to_csv(ARCHIVO_REGISTROS, index=False)

def borrar_registros():
    if os.path.exists(ARCHIVO_REGISTROS):
        os.remove(ARCHIVO_REGISTROS)

def cargar_control():
    if os.path.exists(ARCHIVO_CONTROL):
        df = pd.read_csv(ARCHIVO_CONTROL)
        if not df.empty:
            row = df.iloc[0]
            return {"resultados_visibles": bool(int(row.get("resultados_visibles", 0)))}
    return {"resultados_visibles": False}

def guardar_control(estado: dict):
    pd.DataFrame([{
        "resultados_visibles": int(estado["resultados_visibles"])
    }]).to_csv(ARCHIVO_CONTROL, index=False)

def es_correcta(respuesta: str, pregunta: dict) -> bool:
    """Devuelve True si la respuesta está en la lista de correctas de la pregunta."""
    return respuesta in pregunta["correctas"]

def buscar_resultado_por_documento(documento: str):
    df = cargar_registros()
    if df.empty:
        return None
    coincidencia = df[df["Documento"].astype(str) == documento.strip()]
    if coincidencia.empty:
        return None
    return coincidencia.iloc[-1]

# ── Estado inicial ────────────────────────────────────────────────────────────
if "pantalla" not in st.session_state:
    st.session_state.pantalla = "inicio"

# ════════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Acceso profesor
# ════════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🔒 Acceso Profesor")
    clave = st.text_input("Contraseña", type="password", key="clave_sidebar")
    if st.button("Acceder"):
        if clave == CLAVE_PROFESOR:
            st.session_state.pantalla = "profesor"
            st.rerun()
        else:
            st.error("Contraseña incorrecta.")

    if st.session_state.pantalla == "profesor":
        if st.button("← Volver al inicio"):
            st.session_state.pantalla = "inicio"
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# PANTALLA: INICIO
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state.pantalla == "inicio":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 📐 Quiz · Ecuaciones Diferenciales")
    st.markdown("Cada respuesta correcta vale **2.5 puntos** sobre **5.0**.")
    st.markdown("</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Realizar quiz", use_container_width=True):
            st.session_state.pantalla = "registro"
            st.rerun()
    with col2:
        control = cargar_control()
        if control["resultados_visibles"]:
            if st.button("📊 Consultar mi resultado", use_container_width=True):
                st.session_state.pantalla = "consultar"
                st.rerun()
        else:
            st.info("🔒 La consulta de resultados aún no está disponible.")

# ════════════════════════════════════════════════════════════════════════════════
# PANTALLA: REGISTRO
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.pantalla == "registro":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 👤 Datos del estudiante")

    nombre    = st.text_input("Nombre completo", placeholder="Ej. María González")
    documento = st.text_input("Número de documento de identidad", placeholder="Ej. 1234567890")

    st.markdown("---")
    st.markdown("### ✋ Declaración de honestidad académica")
    juramento = st.checkbox(
        "Declaro formalmente, bajo mi palabra de honor, que las respuestas "
        "presentadas en este quiz son de mi autoría y que no recibí ayuda "
        "no autorizada de ninguna persona o medio durante su realización."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("← Volver"):
            st.session_state.pantalla = "inicio"
            st.rerun()
    with col_b:
        if st.button("Iniciar quiz →"):
            if not nombre.strip():
                st.warning("Por favor ingresa tu nombre completo.")
            elif not documento.strip():
                st.warning("Por favor ingresa tu número de documento.")
            elif not juramento:
                st.warning("Debes aceptar la declaración de honestidad académica.")
            else:
                st.session_state.nombre    = nombre.strip()
                st.session_state.documento = documento.strip()
                st.session_state.juramento = juramento
                st.session_state.pantalla  = "quiz"
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
            "Selecciona tu respuesta:",
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
            for p, r in zip(PREGUNTAS, respuestas):
                correcta = es_correcta(r, p)
                if correcta:
                    calificacion += PUNTOS_POR_PREGUNTA
                resultados.append({
                    "respuesta": r,
                    "correcta":  correcta,
                })

            guardar_registro({
                "Fecha y Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Nombre":       st.session_state.nombre,
                "Documento":    st.session_state.documento,
                "Calificación": calificacion,
                "Respuesta P1": resultados[0]["respuesta"],
                "Correcta P1":  resultados[0]["correcta"],
                "Respuesta P2": resultados[1]["respuesta"],
                "Correcta P2":  resultados[1]["correcta"],
                "Juramento":    "Sí" if st.session_state.juramento else "No",
            })

            st.session_state.pantalla = "enviado"
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# PANTALLA: ENVIADO
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.pantalla == "enviado":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"## ✅ ¡Quiz enviado, {st.session_state.nombre}!")
    st.markdown(
        "<div class='pending-box'>"
        "⏳ Tu calificación y retroalimentación estarán disponibles cuando el profesor "
        "las active. Cuando eso ocurra, regresa a la página principal y haz clic en "
        "<strong>Consultar mi resultado</strong> con tu número de documento."
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("Volver al inicio"):
        for k in ["nombre", "documento", "juramento"]:
            st.session_state.pop(k, None)
        st.session_state.pantalla = "inicio"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════════
# PANTALLA: CONSULTAR RESULTADO
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.pantalla == "consultar":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 📊 Consultar mi resultado")
    st.markdown("Ingresa tu número de documento para ver tu calificación y retroalimentación.")

    doc_consulta = st.text_input("Número de documento", placeholder="Ej. 1234567890")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("← Volver"):
            st.session_state.pantalla = "inicio"
            st.rerun()
    with col_b:
        if st.button("Buscar 🔍"):
            if not doc_consulta.strip():
                st.warning("Por favor ingresa tu número de documento.")
            else:
                registro = buscar_resultado_por_documento(doc_consulta.strip())
                if registro is None:
                    st.error("No se encontró ningún registro con ese número de documento.")
                else:
                    st.markdown("---")

                    # ── Recalcular nota con las reglas corregidas ──────────────
                    cal_recalculada = 0.0
                    for i, p in enumerate(PREGUNTAS):
                        resp_val = registro[f"Respuesta P{i+1}"]
                        if es_correcta(str(resp_val), p):
                            cal_recalculada += PUNTOS_POR_PREGUNTA

                    emoji = "🏆" if cal_recalculada == 5.0 else ("👍" if cal_recalculada >= 2.5 else "📚")

                    st.markdown(f"### {emoji} Resultado de **{registro['Nombre']}**")
                    st.markdown(
                        f"<div class='score-badge'>{cal_recalculada:.1f} / 5.0</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("---")

                    for i, p in enumerate(PREGUNTAS):
                        st.markdown(p["enunciado"])
                        resp_val = str(registro[f"Respuesta P{i+1}"])
                        es_ok    = es_correcta(resp_val, p)

                        if es_ok:
                            st.markdown(
                                f"<span class='correct'>✅ Correcto — {resp_val}</span>",
                                unsafe_allow_html=True
                            )
                        else:
                            st.markdown(
                                f"<span class='incorrect'>❌ Incorrecto — respondiste: {resp_val}</span>",
                                unsafe_allow_html=True
                            )
                            st.markdown(
                                f"<span class='correct'>Respuesta correcta: {p['correcta_display']}</span>",
                                unsafe_allow_html=True
                            )
                        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════════
# PANTALLA: PANEL DEL PROFESOR
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state.pantalla == "profesor":

    st.markdown("## 📊 Panel del Profesor")

    control = cargar_control()

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🎛️ Control de resultados para estudiantes")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        if control["resultados_visibles"]:
            st.success("✅ Los estudiantes **pueden consultar** su calificación y retroalimentación.")
        else:
            st.warning("🔒 Los estudiantes **NO pueden consultar** aún su calificación.")
    with col_b:
        if control["resultados_visibles"]:
            if st.button("🔒 Ocultar resultados"):
                guardar_control({"resultados_visibles": False})
                st.rerun()
        else:
            if st.button("🔓 Publicar resultados"):
                guardar_control({"resultados_visibles": True})
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📋 Registros del Quiz")

    df = cargar_registros()

    if df.empty:
        st.info("Aún no hay registros de estudiantes.")
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total estudiantes", len(df))
        col2.metric("Promedio", f"{df['Calificación'].mean():.2f}")
        col3.metric("Nota máxima", f"{df['Calificación'].max():.1f}")

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar CSV",
            data=csv,
            file_name="registros_quiz_ecuaciones.csv",
            mime="text/csv"
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🗑️ Limpiar registros para nuevo quiz")
    st.error(
        "⚠️ Esta acción borra **todos** los registros permanentemente. "
        "Descarga el CSV primero si deseas conservarlos."
    )
    confirmar = st.checkbox("Confirmo que deseo borrar todos los registros y comenzar un nuevo quiz.")
    if confirmar:
        if st.button("🗑️ Borrar todos los registros"):
            borrar_registros()
            guardar_control({"resultados_visibles": False})
            st.success("✅ Registros borrados. La app está lista para un nuevo quiz.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
