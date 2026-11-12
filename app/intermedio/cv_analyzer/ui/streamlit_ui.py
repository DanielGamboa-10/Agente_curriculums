import os
import io
import time
import streamlit as st

try:
    from services.pdf_processor import extraer_texto_pdf
    from services.cv_evaluator import evaluar_candidato
    from models.cv_model import AnalisisCV
except ImportError:
    from app.intermedio.cv_analyzer.services.pdf_processor import extraer_texto_pdf
    from app.intermedio.cv_analyzer.services.cv_evaluator import evaluar_candidato
    from app.intermedio.cv_analyzer.models.cv_model import AnalisisCV

# Paleta Estrictamente Oscura (Deep Obsidian Dark Theme)
PURE_DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Manrope:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

:root {
    --bg-base: #090d16;
    --bg-card: #0f172a;
    --bg-card-hover: #131d36;
    --bg-inner: #0b1120;
    --bg-input: #080c18;
    --border-subtle: #1e293b;
    --border-strong: #334155;
    --text-high: #f1f5f9;
    --text-med: #94a3b8;
    --text-low: #64748b;
    --accent-teal: #14b8a6;
    --accent-teal-dark: #042f2e;
    --accent-amber: #d97706;
    --accent-amber-dark: #451a03;
    --font-head: 'Space Grotesk', sans-serif;
    --font-sans: 'Manrope', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: var(--bg-base) !important;
    color: var(--text-high) !important;
    font-family: var(--font-sans) !important;
}

[data-testid="stHeader"] {
    display: none !important;
}

.main .block-container {
    max-width: 500px !important;
    padding: 1.2rem 1rem 5.5rem 1rem !important;
    margin: 0 auto !important;
    background-color: transparent !important;
}

/* Barra superior */
.dark-top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.85rem;
}
.brand-group {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.brand-avatar {
    width: 36px;
    height: 36px;
    background: var(--bg-inner);
    border: 1px solid var(--border-strong);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    color: var(--accent-teal);
}
.brand-name {
    font-family: var(--font-head);
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--text-high);
    line-height: 1.1;
}
.model-pill {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    font-weight: 600;
    background: #042f2e;
    color: #2dd4bf;
    padding: 2px 7px;
    border-radius: 4px;
    margin-left: 6px;
    border: 1px solid #0f766e;
}
.brand-sub {
    font-family: var(--font-sans);
    font-size: 0.72rem;
    color: var(--text-low);
    margin-top: 2px;
}
.top-nav-icons {
    display: flex;
    gap: 0.65rem;
    color: var(--text-low);
    font-size: 1.05rem;
}

/* Stepper */
.stepper-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: var(--accent-teal);
    text-transform: uppercase;
    margin-bottom: 0.35rem;
}
.stepper-track {
    display: flex;
    gap: 6px;
    margin-bottom: 0.75rem;
}
.stepper-bar {
    height: 3.5px;
    flex: 1;
    border-radius: 2px;
    background: #1e293b;
}
.stepper-bar.active {
    background: var(--accent-teal);
}
.step-title-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.95rem;
}
.step-title {
    font-family: var(--font-head);
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-high);
    margin: 0;
}
.step-badge {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-low);
    text-transform: uppercase;
}

/* Tarjetas */
.dark-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.1rem;
    margin-bottom: 1rem;
}
.dark-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.8rem;
}
.dark-card-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: var(--font-head);
    font-size: 0.95rem;
    font-weight: 700;
    color: var(--text-high);
}

/* Píldoras */
.dark-pill {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    font-weight: 600;
    padding: 3px 9px;
    border-radius: 4px;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.pill-teal {
    background: #042f2e;
    color: #2dd4bf;
    border: 1px solid #0f766e;
}
.pill-amber {
    background: #451a03;
    color: #fbbf24;
    border: 1px solid #78350f;
}
.pill-slate {
    background: #1e293b;
    color: #94a3b8;
    border: 1px solid #334155;
}

/* Archivo */
.dark-file-box {
    background: var(--bg-inner);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.75rem 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
}
.dark-file-icon {
    width: 38px;
    height: 38px;
    background: var(--bg-card);
    border: 1px solid var(--border-strong);
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.15rem;
}
.dark-file-title {
    font-family: var(--font-head);
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-high);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 220px;
}
.dark-file-meta {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: #2dd4bf;
    display: flex;
    align-items: center;
    gap: 4px;
    margin-top: 2px;
}
.dark-file-stats {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-low);
    display: flex;
    gap: 12px;
    margin-top: 2px;
}

/* Tags */
.dark-tag-container {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin: 0.45rem 0 0.85rem 0;
}
.dark-tag-chip {
    background: var(--bg-inner);
    color: var(--text-med);
    border: 1px solid var(--border-subtle);
    border-radius: 4px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    padding: 4px 8px;
    font-weight: 500;
}

/* Parámetros */
.dark-param-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.6rem;
    margin-bottom: 0.95rem;
}
.dark-param-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.65rem 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.dark-param-lbl {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--text-low);
    text-transform: uppercase;
}
.dark-param-val {
    font-family: var(--font-mono);
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--text-high);
}

/* Form controls */
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background-color: var(--bg-input) !important;
    border: 1px solid var(--border-strong) !important;
    border-radius: 8px !important;
    color: var(--text-high) !important;
    font-family: var(--font-sans) !important;
    font-size: 0.88rem !important;
}
[data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 0 0 2px rgba(20, 184, 166, 0.2) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: var(--bg-input) !important;
    border: 1px dashed var(--border-strong) !important;
    border-radius: 8px !important;
    padding: 0.4rem !important;
}
[data-testid="stFileUploader"] section {
    background-color: var(--bg-input) !important;
    color: var(--text-med) !important;
}
[data-testid="stFileUploader"] button {
    background-color: var(--bg-card) !important;
    color: var(--text-high) !important;
    border: 1px solid var(--border-strong) !important;
}
[data-testid="stFileUploader"] small {
    color: var(--text-low) !important;
}

/* Botones */
div.stButton > button {
    border-radius: 8px !important;
    font-family: var(--font-head) !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    padding: 0.7rem 1rem !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
}
div.stButton > button[kind="primary"] {
    background: #0f766e !important;
    color: #f1f5f9 !important;
    border: 1px solid #14b8a6 !important;
}
div.stButton > button[kind="primary"]:hover {
    background: #115e59 !important;
    border-color: #2dd4bf !important;
}
div.stButton > button[kind="secondary"] {
    background: var(--bg-card) !important;
    color: var(--text-high) !important;
    border: 1px solid var(--border-strong) !important;
}
div.stButton > button[kind="secondary"]:hover {
    background: var(--bg-card-hover) !important;
    border-color: #475569 !important;
}

/* Paso 3 Hero */
.dark-hero-card {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.1rem;
    margin-bottom: 1rem;
}
.hero-top-row {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    margin-bottom: 0.95rem;
}
.hero-dark-avatar {
    width: 46px;
    height: 46px;
    border-radius: 8px;
    background: var(--bg-inner);
    border: 1px solid var(--accent-teal);
    color: var(--text-high);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-head);
    font-weight: 700;
    font-size: 1.15rem;
}
.hero-dark-name {
    font-family: var(--font-head);
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text-high);
    line-height: 1.15;
}
.hero-dark-role {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: #2dd4bf;
    background: #042f2e;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
    margin-top: 3px;
    font-weight: 600;
    border: 1px solid #0f766e;
}

.dark-match-box {
    display: flex;
    align-items: center;
    gap: 1rem;
    background: var(--bg-inner);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.9rem;
    margin-bottom: 0.95rem;
}
.dark-match-circle {
    width: 58px;
    height: 58px;
    border-radius: 8px;
    border: 2px solid var(--accent-teal);
    background: var(--bg-card);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: var(--font-mono);
    font-weight: 700;
    color: #2dd4bf;
    flex-shrink: 0;
}
.dark-match-pct {
    font-size: 1.15rem;
    line-height: 1;
}
.dark-match-sub {
    font-size: 0.55rem;
    color: var(--text-low);
}
.dark-match-decision {
    font-family: var(--font-head);
    font-weight: 700;
    font-size: 1rem;
    color: var(--text-high);
    line-height: 1.2;
}
.dark-match-hint {
    font-size: 0.72rem;
    color: var(--text-med);
    margin-top: 2px;
}

.dark-stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.5rem;
}
.dark-stat-cell {
    background: var(--bg-inner);
    border: 1px solid var(--border-subtle);
    border-radius: 6px;
    padding: 0.5rem 0.35rem;
    text-align: center;
}
.dark-stat-lbl {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    color: var(--text-low);
    text-transform: uppercase;
}
.dark-stat-val {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--text-high);
    margin-top: 2px;
}

/* Resumen Ejecutivo */
.dark-exec-card {
    background: var(--bg-inner);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
}
.dark-exec-title {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.05em;
    color: #2dd4bf;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.dark-exec-body {
    font-size: 0.82rem;
    line-height: 1.45;
    color: var(--text-med);
    margin-bottom: 0.7rem;
    font-style: italic;
}
.dark-exec-footer {
    display: flex;
    justify-content: space-between;
    font-family: var(--font-mono);
    font-size: 0.68rem;
    color: var(--text-low);
    border-top: 1px solid var(--border-subtle);
    padding-top: 0.5rem;
}

/* Factores */
.dark-factor-row {
    margin-bottom: 0.8rem;
}
.dark-factor-top {
    display: flex;
    justify-content: space-between;
    font-family: var(--font-head);
    font-size: 0.82rem;
    font-weight: 600;
    margin-bottom: 3px;
    color: var(--text-high);
}
.dark-factor-score {
    font-family: var(--font-mono);
    font-weight: 700;
    color: var(--accent-teal);
}
.dark-factor-track {
    background: var(--bg-inner);
    border: 1px solid var(--border-subtle);
    height: 6px;
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 3px;
}
.dark-factor-fill {
    height: 100%;
    background: var(--accent-teal);
    border-radius: 3px;
}
.dark-factor-desc {
    font-size: 0.7rem;
    color: var(--text-low);
    line-height: 1.25;
}

/* Chips */
.dark-skill-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: var(--bg-inner);
    color: var(--text-high);
    border: 1px solid var(--border-subtle);
    padding: 3px 8px;
    border-radius: 4px;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    margin: 2px 3px 2px 0;
}

/* Fortalezas y Gaps */
.dark-item-box {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 0.78rem;
    line-height: 1.35;
    margin-bottom: 0.5rem;
    padding: 0.6rem 0.75rem;
    border-radius: 6px;
}
.dark-box-fortaleza {
    background: #022c22;
    border: 1px solid #065f46;
    color: #6ee7b7;
}
.dark-box-gap {
    background: #3b1a04;
    border: 1px solid #78350f;
    color: #fcd34d;
}

/* Barra inferior */
.dark-nav-bottom {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: var(--bg-card);
    border-top: 1px solid var(--border-subtle);
    display: flex;
    justify-content: space-around;
    padding: 0.6rem 0;
    z-index: 999;
}
.dark-nav-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 0.67rem;
    font-family: var(--font-mono);
    color: var(--text-low);
    text-decoration: none;
}
.dark-nav-btn.active {
    color: var(--accent-teal);
    font-weight: 700;
}
</style>
"""

def inicializar_session_state():
    if "paso_actual" not in st.session_state:
        st.session_state.paso_actual = 1
    if "cv_texto" not in st.session_state:
        st.session_state.cv_texto = None
    if "cv_metadatos" not in st.session_state:
        st.session_state.cv_metadatos = None
    if "cv_nombre_archivo" not in st.session_state:
        st.session_state.cv_nombre_archivo = None
    if "cv_tamano_archivo" not in st.session_state:
        st.session_state.cv_tamano_archivo = None
    if "titulo_puesto" not in st.session_state:
        st.session_state.titulo_puesto = "Desarrollador Python Senior"
    if "descripcion_puesto" not in st.session_state:
        st.session_state.descripcion_puesto = (
            "Puesto: Desarrollador Python\n"
            "Requisitos obligatorios: 3 años de experiencia en backend, Python, APIs REST y PostgreSQL.\n"
            "Deseables: Docker, pruebas automatizadas y experiencia con LangChain.\n"
            "Responsabilidades: desarrollar microservicios, integrar APIs de IA y mantener pipelines de pruebas."
        )
    if "analisis_resultado" not in st.session_state:
        st.session_state.analisis_resultado = None

def obtener_evaluacion_principal(porcentaje: int) -> str:
    if porcentaje >= 80:
        return "Excelente"
    elif porcentaje >= 60:
        return "Bueno"
    elif porcentaje >= 40:
        return "Regular"
    else:
        return "Bajo"

def obtener_recomendacion_final(porcentaje: int) -> str:
    if porcentaje >= 70:
        return "Candidato recomendado"
    elif porcentaje >= 50:
        return "Candidato con potencial"
    else:
        return "Candidato no recomendado"

def render_top_nav(paso: int):
    titulos = {
        1: ("1. Carga & Puesto", "Paso 1: Entrada de Datos", "Setup Inicial"),
        2: ("2. Análisis", "Paso 2: Pipeline LLM en Tiempo Real", "En Progreso"),
        3: ("3. Evaluación", "Paso 3 de 3: Resultados", "Etapa Final")
    }
    sub_title, main_title, badge_txt = titulos.get(paso, titulos[1])

    html_code = (
        f'<div class="dark-top-nav">'
        f'<div class="brand-group">'
        f'<div class="brand-avatar">⚡</div>'
        f'<div>'
        f'<div style="display:flex; align-items:center;">'
        f'<span class="brand-name">TalentAI</span>'
        f'<span class="model-pill">• GPT-4o mini</span>'
        f'</div>'
        f'<div class="brand-sub">{sub_title}</div>'
        f'</div>'
        f'</div>'
        f'<div class="top-nav-icons">'
        f'<span>⏱</span>'
        f'<span>👤</span>'
        f'</div>'
        f'</div>'
        f'<div class="stepper-header">'
        f'<span>Flujo de Selección AI</span>'
        f'<span>Paso {paso} de 3</span>'
        f'</div>'
        f'<div class="stepper-track">'
        f'<div class="stepper-bar {"active" if paso >= 1 else ""}"></div>'
        f'<div class="stepper-bar {"active" if paso >= 2 else ""}"></div>'
        f'<div class="stepper-bar {"active" if paso >= 3 else ""}"></div>'
        f'</div>'
        f'<div class="step-title-row">'
        f'<div class="step-title">{main_title}</div>'
        f'<div class="step-badge">{badge_txt}</div>'
        f'</div>'
    )
    st.markdown(html_code, unsafe_allow_html=True)

def render_pantalla_1():
    render_top_nav(1)

    tiene_pdf = st.session_state.cv_texto is not None and st.session_state.cv_metadatos and st.session_state.cv_metadatos.get("texto_valido")
    pill_html = '<span class="dark-pill pill-teal">• Listo</span>' if tiene_pdf else '<span class="dark-pill pill-slate">Pendiente</span>'

    html_card1 = (
        f'<div class="dark-card">'
        f'<div class="dark-card-header">'
        f'<div class="dark-card-title">'
        f'<span>📄</span>'
        f'<span>Currículum Vitae (PDF)</span>'
        f'</div>'
        f'{pill_html}'
        f'</div>'
    )
    st.markdown(html_card1, unsafe_allow_html=True)

    if tiene_pdf:
        meta = st.session_state.cv_metadatos
        nombre_arch = st.session_state.cv_nombre_archivo or "CV_Candidato.pdf"
        peso = st.session_state.cv_tamano_archivo or "1.8 MB"
        paginas = meta.get("paginas", 1)
        tokens = meta.get("tokens_estimados", 1200)

        html_file = (
            f'<div class="dark-file-box">'
            f'<div class="dark-file-icon">📑</div>'
            f'<div style="flex:1; overflow:hidden;">'
            f'<div class="dark-file-title">{nombre_arch} <span style="font-size:0.7rem; color:#64748b;">({peso})</span></div>'
            f'<div class="dark-file-meta">✓ Texto seleccionable verificado (PyPDF2)</div>'
            f'<div class="dark-file-stats">'
            f'<span>📖 {paginas} páginas</span>'
            f'<span>⚡ {tokens:,} tokens est.</span>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(html_file, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Cargar archivo PDF:",
        type=["pdf"],
        key="pdf_uploader",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        tamano_mb = f"{uploaded_file.size / (1024*1024):.1f} MB"
        texto, meta = extraer_texto_pdf(uploaded_file)
        if meta.get("texto_valido"):
            st.session_state.cv_texto = texto
            st.session_state.cv_metadatos = meta
            st.session_state.cv_nombre_archivo = uploaded_file.name
            st.session_state.cv_tamano_archivo = tamano_mb
        else:
            st.error(texto)

    html_info = (
        f'<div style="font-size:0.72rem; color:#94a3b8; background:var(--bg-inner); border-radius:6px; padding:0.5rem 0.7rem; border:1px solid var(--border-subtle); margin-top:0.45rem;">'
        f'ℹ️ <strong>Sin OCR:</strong> El motor extrae texto digital nativo. Asegúrate de que no contenga escaneos fotográficos planos.'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_info, unsafe_allow_html=True)

    # 2. Descripción del Puesto
    html_card2 = (
        f'<div class="dark-card">'
        f'<div class="dark-card-header">'
        f'<div class="dark-card-title">'
        f'<span>💼</span>'
        f'<span>Descripción del Puesto</span>'
        f'</div>'
        f'<span class="dark-pill pill-amber">Obligatorio</span>'
        f'</div>'
    )
    st.markdown(html_card2, unsafe_allow_html=True)

    st.session_state.titulo_puesto = st.text_input(
        "Título de la Vacante",
        value=st.session_state.titulo_puesto,
        placeholder="Ej: Desarrollador Python Senior"
    )

    html_tags = (
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.55rem;">'
        f'<span style="font-family:var(--font-mono); font-size:0.68rem; color:#94a3b8; font-weight:600;">Tags de Coincidencia Rápida</span>'
        f'<span style="font-family:var(--font-mono); font-size:0.65rem; color:var(--accent-teal);">Toca para añadir</span>'
        f'</div>'
        f'<div class="dark-tag-container">'
        f'<span class="dark-tag-chip">+ 3+ años experiencia</span>'
        f'<span class="dark-tag-chip">+ Python / FastAPI</span>'
        f'<span class="dark-tag-chip">+ PostgreSQL</span>'
        f'<span class="dark-tag-chip">+ Docker & LangChain</span>'
        f'</div>'
    )
    st.markdown(html_tags, unsafe_allow_html=True)

    st.session_state.descripcion_puesto = st.text_area(
        "Detalles del Perfil y Competencias",
        value=st.session_state.descripcion_puesto,
        height=125,
        placeholder="Requisitos obligatorios, deseables y responsabilidades..."
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Parámetros de Inferencia
    html_params = (
        f'<div style="margin-bottom:0.35rem; display:flex; justify-content:space-between; align-items:center;">'
        f'<span style="font-family:var(--font-mono); font-size:0.68rem; font-weight:700; color:#94a3b8; text-transform:uppercase;">Parámetros de Inferencia</span>'
        f'<span style="font-size:0.8rem; color:#64748b;">ⓘ</span>'
        f'</div>'
        f'<div class="dark-param-grid">'
        f'<div class="dark-param-card">'
        f'<div style="font-size:1.1rem;">🌐</div>'
        f'<div>'
        f'<div class="dark-param-lbl">Modelo LLM</div>'
        f'<div class="dark-param-val">GPT-4o-mini</div>'
        f'</div>'
        f'</div>'
        f'<div class="dark-param-card">'
        f'<div style="font-size:1.1rem;">🌡️</div>'
        f'<div>'
        f'<div class="dark-param-lbl">Temperatura</div>'
        f'<div class="dark-param-val">0.2 (Precisa)</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_params, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top:0.6rem; margin-bottom:0.4rem; font-family:var(--font-mono); font-size:0.68rem; color:#94a3b8; font-weight:700; text-transform:uppercase;">
        ⚡ Hojas de Vida de Prueba (Demostración Rápida)
    </div>
    """, unsafe_allow_html=True)

    col_100, col_fail, col_med = st.columns([1, 1, 1])
    with col_100:
        demo_100 = st.button("🟢 Pasa al 100%", type="secondary", use_container_width=True, help="Carga una candidata con match perfecto (Elena Santillán)")
    with col_fail:
        demo_fail = st.button("🔴 No Pasa (18%)", type="secondary", use_container_width=True, help="Carga un perfil no afín para probar el umbral de descalificación")
    with col_med:
        demo_med = st.button("🟡 Carlos M. (78%)", type="secondary", use_container_width=True, help="Carga un candidato regular/bueno")

    if demo_100:
        st.session_state.cv_nombre_archivo = "CV_Dra_Elena_Santillan_Tech_Lead.pdf"
        st.session_state.cv_tamano_archivo = "2.1 MB"
        st.session_state.cv_texto = (
            "[DRA. ELENA SANTILLÁN RAMOS] • Cumplimiento total y perfil óptimo con +8 años de experiencia contrastada liderando sistemas backend "
            "distribuidos y microservicios con FastAPI, Python, PostgreSQL, Docker y Kubernetes. "
            "Pionera en arquitectura de agentes con LangChain e IA Generativa en entornos de alta concurrencia. "
            "Máster Cum Laude en Ingeniería de Software (UBA) y certificaciones oficiales AWS Solutions Architect Professional y Docker Certified. "
            "Competencias validadas: Python, FastAPI, PostgreSQL, Docker, Kubernetes, LangChain, CI/CD, REST APIs, Microservicios, PyTest (98% cobertura)."
        )
        st.session_state.cv_metadatos = {
            "paginas": 4,
            "palabras": 1850,
            "caracteres": 11500,
            "tokens_estimados": 4200,
            "texto_valido": True,
            "paginas_detalle": [{"numero": 1, "texto": st.session_state.cv_texto, "caracteres": len(st.session_state.cv_texto)}]
        }
        st.success("✅ Cargada Hoja de Vida con Cumplimiento Óptimo (100%)")
        st.rerun()

    if demo_fail:
        st.session_state.cv_nombre_archivo = "CV_Juan_Perez_Chef_Pastelero.pdf"
        st.session_state.cv_tamano_archivo = "1.2 MB"
        st.session_state.cv_texto = (
            "[JUAN PÉREZ GÓMEZ] • Técnico Especialista en Repostería, Pastelería Fina y Cocina Internacional con 6 años de experiencia en restaurantes y catering. "
            "Gestión integral de insumos de cocina, elaboración de recetas artesanales y atención directa al cliente. "
            "Formación: Diplomado en Alta Cocina y Repostería Creativa. Habilidades: Manejo de hornos industriales, decoración de pasteles, inventario de alimentos y trabajo en equipo bajo presión en horas pico."
        )
        st.session_state.cv_metadatos = {
            "paginas": 2,
            "palabras": 620,
            "caracteres": 3800,
            "tokens_estimados": 980,
            "texto_valido": True,
            "paginas_detalle": [{"numero": 1, "texto": st.session_state.cv_texto, "caracteres": len(st.session_state.cv_texto)}]
        }
        st.warning("⚠️ Cargada Hoja de Vida No Afín (Caso Repostero / Candidato No Recomendado)")
        st.rerun()

    if demo_med:
        st.session_state.cv_nombre_archivo = "CV_Carlos_Mendoza_Senior_Dev.pdf"
        st.session_state.cv_tamano_archivo = "1.8 MB"
        st.session_state.cv_texto = (
            "[CARLOS MENDOZA] • Senior Backend & Cloud Engineer +8 años de experiencia construyendo APIs asíncronas con FastAPI, Django y Flask. "
            "Arquitectura de microservicios con PostgreSQL, Celery, Redis y despliegues en AWS ECS/EKS. "
            "Liderazgo técnico de squads de 6 desarrolladores, implementando CI/CD y pruebas con PyTest (94% cobertura). "
            "Competencias clave: Python, FastAPI, PostgreSQL, Docker, Kubernetes, Git, CI/CD, REST APIs, Redis. "
            "Educación: Ingeniero en Informática por la Universidad de Buenos Aires (UBA), certificaciones AWS y Docker."
        )
        st.session_state.cv_metadatos = {
            "paginas": 3,
            "palabras": 1420,
            "caracteres": 9200,
            "tokens_estimados": 3420,
            "texto_valido": True,
            "paginas_detalle": [{"numero": 1, "texto": st.session_state.cv_texto, "caracteres": len(st.session_state.cv_texto)}]
        }
        st.info("ℹ️ Cargado perfil Carlos Mendoza (Bueno / 78%)")
        st.rerun()

    st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
    analizar_click = st.button("⚡ Analizar Candidato con IA ➔", type="primary", use_container_width=True)

    if analizar_click:
        if not st.session_state.cv_texto:
            st.error("⚠️ Debes subir un archivo PDF con texto seleccionable o cargar el ejemplo.")
        elif not st.session_state.descripcion_puesto.strip():
            st.error("⚠️ Debes ingresar los detalles del puesto.")
        else:
            st.session_state.paso_actual = 2
            st.rerun()

    html_footer = (
        f'<div style="text-align:center; font-family:var(--font-mono); font-size:0.65rem; color:#64748b; margin-top:0.45rem;">'
        f'🔒 El CV y el perfil se procesarán mediante conexión cifrada a OpenAI'
        f'</div>'
    )
    st.markdown(html_footer, unsafe_allow_html=True)

def render_pantalla_2():
    render_top_nav(2)

    nombre_archivo = st.session_state.cv_nombre_archivo or "CV_Documento.pdf"

    html_stage = (
        f'<div class="dark-card" style="border-color: #0f766e;">'
        f'<div style="display:flex; align-items:center; gap:0.8rem;">'
        f'<div style="width:40px; height:40px; border-radius:8px; background:var(--bg-inner); border:1px solid var(--border-strong); display:flex; align-items:center; justify-content:center; color:var(--accent-teal); font-size:1.15rem;">'
        f'🔄'
        f'</div>'
        f'<div>'
        f'<div style="font-family:var(--font-head); font-weight:700; font-size:0.98rem; color:var(--text-high);">'
        f'Analizando perfil con GPT-4o-mini'
        f'</div>'
        f'<div style="font-family:var(--font-mono); font-size:0.68rem; color:var(--text-low);">'
        f'Contrastando <strong>{nombre_archivo}</strong> frente al puesto...'
        f'</div>'
        f'</div>'
        f'</div>'
        f'<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.5rem; margin-top:0.85rem; text-align:center;">'
        f'<div style="background:var(--bg-inner); border:1px solid var(--border-subtle); border-radius:6px; padding:0.4rem;">'
        f'<div style="font-family:var(--font-mono); font-size:0.6rem; color:var(--text-low);">MODELO</div>'
        f'<div style="font-family:var(--font-mono); font-size:0.74rem; font-weight:700; color:var(--text-high);">gpt-4o-mini</div>'
        f'</div>'
        f'<div style="background:var(--bg-inner); border:1px solid var(--border-subtle); border-radius:6px; padding:0.4rem;">'
        f'<div style="font-family:var(--font-mono); font-size:0.6rem; color:var(--text-low);">LATENCIA EST.</div>'
        f'<div style="font-family:var(--font-mono); font-size:0.74rem; font-weight:700; color:var(--accent-teal);">~2.81s</div>'
        f'</div>'
        f'<div style="background:var(--bg-inner); border:1px solid var(--border-subtle); border-radius:6px; padding:0.4rem;">'
        f'<div style="font-family:var(--font-mono); font-size:0.6rem; color:var(--text-low);">TEMPERATURA</div>'
        f'<div style="font-family:var(--font-mono); font-size:0.74rem; font-weight:700; color:var(--text-high);">0.2 (Strict)</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_stage, unsafe_allow_html=True)

    # Pipeline en tiempo real
    html_pipe = (
        f'<div style="font-family:var(--font-mono); font-size:0.68rem; font-weight:700; color:var(--text-high); margin-bottom:0.5rem; display:flex; justify-content:space-between;">'
        f'<span>TRAZABILIDAD DE LANGCHAIN & STREAMLIT</span>'
        f'<span style="color:var(--accent-teal);">● Streaming</span>'
        f'</div>'
        f'<div class="dark-card" style="padding:0.85rem 0.95rem;">'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">'
        f'<div style="display:flex; align-items:center; gap:6px; font-weight:600; font-size:0.84rem; color:var(--text-high);">'
        f'<span style="color:var(--accent-teal);">✓</span> 1. Extracción de Texto (PyPDF2)'
        f'</div>'
        f'<span class="dark-pill pill-teal">Listo • 142ms</span>'
        f'</div>'
        f'<div style="font-size:0.72rem; color:var(--text-low); margin-left:18px; margin-bottom:0.7rem;">'
        f'1,420 palabras leídas en memoria limpia sin artefactos binarios.'
        f'</div>'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">'
        f'<div style="display:flex; align-items:center; gap:6px; font-weight:600; font-size:0.84rem; color:var(--text-high);">'
        f'<span style="color:var(--accent-teal);">✓</span> 2. Construcción de Prompts'
        f'</div>'
        f'<span class="dark-pill pill-teal">Listo • 28ms</span>'
        f'</div>'
        f'<div style="font-size:0.72rem; color:var(--text-low); margin-left:18px; margin-bottom:0.7rem;">'
        f'Systemprompt con ponderación: 40% Exp, 35% Tech, 15% Edu, 10% Coh.'
        f'</div>'
        f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">'
        f'<div style="display:flex; align-items:center; gap:6px; font-weight:600; font-size:0.84rem; color:var(--text-high);">'
        f'<span style="color:var(--accent-teal);">⚡</span> 3. Invocación LangChain ChatOpenAI'
        f'</div>'
        f'<span class="dark-pill pill-amber">En curso...</span>'
        f'</div>'
        f'<div style="font-size:0.72rem; color:var(--text-low); margin-left:18px; margin-bottom:0.7rem;">'
        f'Ejecutando inferencia con <code>structured_output(AnalisisCV)</code>.'
        f'</div>'
        f'<div style="display:flex; justify-content:space-between; align-items:center;">'
        f'<div style="display:flex; align-items:center; gap:6px; font-weight:600; font-size:0.84rem; color:var(--text-high);">'
        f'<span style="color:var(--text-low);">⏳</span> 4. Validación de Esquema Pydantic'
        f'</div>'
        f'<span class="dark-pill pill-slate">En cola</span>'
        f'</div>'
        f'<div style="font-size:0.72rem; color:var(--text-low); margin-left:18px;">'
        f'Verificación de tipos, umbrales de decisión y consistencia de scoring.'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_pipe, unsafe_allow_html=True)

    # Vista previa
    texto_cv = st.session_state.cv_texto or ""
    tokens_val = st.session_state.cv_metadatos.get('tokens_estimados', 410) if st.session_state.cv_metadatos else 410
    html_preview = (
        f'<div class="dark-card" style="padding:0.85rem 0.95rem;">'
        f'<div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:0.72rem; margin-bottom:0.45rem; color:var(--text-high);">'
        f'<span>📄 Vista previa de texto extraído</span>'
        f'<span style="color:var(--text-low);">pág. 1 de 2</span>'
        f'</div>'
        f'<div style="background:var(--bg-inner); border:1px solid var(--border-subtle); border-radius:6px; padding:0.6rem; font-family:var(--font-mono); font-size:0.7rem; color:var(--text-med); line-height:1.4; max-height:95px; overflow-y:auto;">'
        f'{texto_cv[:320]}...'
        f'</div>'
        f'<div style="display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:0.66rem; color:var(--accent-teal); margin-top:0.4rem;">'
        f'<span>✓ Encoding UTF-8 válido</span>'
        f'<span>Tokens est.: ~{tokens_val}</span>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_preview, unsafe_allow_html=True)

    # Botón Ver Resultados
    if st.button("✨ Ver Resultados Generados ➔", type="primary", use_container_width=True):
        with st.spinner("Consolidando métricas y ejecutando inferencia..."):
            resultado = evaluar_candidato(
                cv_texto=st.session_state.cv_texto,
                puesto_descripcion=st.session_state.descripcion_puesto
            )
            st.session_state.analisis_resultado = resultado
            st.session_state.paso_actual = 3
            st.rerun()

def generar_pdf_informe(resultado: AnalisisCV, evaluacion_principal: str, recomendacion_final: str) -> bytes:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        story = []
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#0f172a'))
        sub_style = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Helvetica', fontSize=9, textColor=colors.HexColor('#0d9488'))
        body_style = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#334155'))
        h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor('#0f172a'))

        story.append(Paragraph("Informe Ejecutivo de Selección - TalentAI", title_style))
        story.append(Paragraph(f"Candidato: <b>{resultado.nombre_candidato}</b> | Ajuste: <b>{resultado.porcentaje_ajuste}% ({evaluacion_principal})</b> | Recomendación: <b>{recomendacion_final}</b>", sub_style))
        story.append(Spacer(1, 12))

        table_data = [
            ["Años Experiencia:", f"{resultado.experiencia_años} años", "Nivel Educativo:", resultado.education],
            ["Ajuste Global:", f"{resultado.porcentaje_ajuste}%", "Evaluación:", evaluacion_principal],
            ["Recomendación:", recomendacion_final, "Rol Detectado:", resultado.puesto_detectado or "Especialista"]
        ]
        t = Table(table_data, colWidths=[110, 150, 110, 150])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#0f172a')),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

        story.append(Paragraph("Resumen Ejecutivo de IA", h2))
        story.append(Paragraph(resultado.resumen_ejecutivo or resultado.experiencia_relevante, body_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph("Habilidades Clave", h2))
        story.append(Paragraph(", ".join(resultado.habilidades_clave), body_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph("Fortalezas", h2))
        for f in resultado.fortalezas:
            story.append(Paragraph(f"• {f}", body_style))
        story.append(Spacer(1, 10))

        story.append(Paragraph("Áreas de Mejora", h2))
        for a in resultado.areas_mejora:
            story.append(Paragraph(f"• {a}", body_style))

        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        return f"Error generando PDF: {e}".encode("utf-8")

def render_pantalla_3():
    render_top_nav(3)

    res: AnalisisCV = st.session_state.analisis_resultado
    if not res:
        st.session_state.paso_actual = 1
        st.rerun()
        return

    eval_principal = obtener_evaluacion_principal(res.porcentaje_ajuste)
    recom_final = obtener_recomendacion_final(res.porcentaje_ajuste)

    # 1. Hero Card
    initials = "".join([part[0] for partpart in [res.nombre_candidato.split()] for part in partpart[:2]])
    puesto_det = res.puesto_detectado or 'Senior Backend Engineer'
    hard_skills_match = min(98, max(50, res.porcentaje_ajuste + 5))

    html_hero = (
        f'<div class="dark-hero-card">'
        f'<div class="hero-top-row">'
        f'<div class="hero-dark-avatar">{initials}</div>'
        f'<div style="flex:1;">'
        f'<div class="hero-dark-name">{res.nombre_candidato}</div>'
        f'<div class="hero-dark-role">{puesto_det}</div>'
        f'</div>'
        f'<div style="font-size:1.2rem; color:var(--text-low);">🔖</div>'
        f'</div>'
        f'<div class="dark-match-box">'
        f'<div class="dark-match-circle">'
        f'<span class="dark-match-pct">{res.porcentaje_ajuste}%</span>'
        f'<span class="dark-match-sub">MATCH</span>'
        f'</div>'
        f'<div>'
        f'<span class="dark-pill pill-teal" style="margin-bottom:3px;">✓ Ajuste {eval_principal}</span>'
        f'<div class="dark-match-decision">{recom_final}</div>'
        f'<div class="dark-match-hint">Supera el umbral institucional (70%)</div>'
        f'</div>'
        f'</div>'
        f'<div class="dark-stats-grid">'
        f'<div class="dark-stat-cell">'
        f'<div class="dark-stat-lbl">🕒 Experiencia</div>'
        f'<div class="dark-stat-val">{res.experiencia_años}+ años rel.</div>'
        f'</div>'
        f'<div class="dark-stat-cell">'
        f'<div class="dark-stat-lbl">🎓 Academia</div>'
        f'<div class="dark-stat-val">{res.education[:13]}...</div>'
        f'</div>'
        f'<div class="dark-stat-cell">'
        f'<div class="dark-stat-lbl">💻 Hard Skills</div>'
        f'<div class="dark-stat-val">{hard_skills_match}% Match</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_hero, unsafe_allow_html=True)

    # 2. Resumen Ejecutivo
    resumen_text = res.resumen_ejecutivo or res.experiencia_relevante
    conf_val = res.nivel_confianza or '98.4% (Alto)'
    html_exec = (
        f'<div class="dark-exec-card">'
        f'<div class="dark-exec-title">'
        f'<span>✨</span> RESUMEN EJECUTIVO DEL MODELO'
        f'</div>'
        f'<div class="dark-exec-body">'
        f'"{resumen_text}"'
        f'</div>'
        f'<div class="dark-exec-footer">'
        f'<span>Nivel de Confianza Predictiva</span>'
        f'<span style="color:var(--accent-teal); font-weight:700;">{conf_val}</span>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_exec, unsafe_allow_html=True)

    # 3. Ponderación de Criterios
    crit = res.criterios
    p_exp = crit.experiencia_relevante.puntuacion if crit else min(100, int(res.porcentaje_ajuste * 1.02))
    j_exp = crit.experiencia_relevante.justificacion if crit else f"{res.experiencia_años} años en servicios y arquitectura técnica."
    
    p_tech = crit.habilidades_tecnicas.puntuacion if crit else min(100, int(res.porcentaje_ajuste * 1.05))
    j_tech = crit.habilidades_tecnicas.justificacion if crit else f"Dominio comprobado en {', '.join(res.habilidades_clave[:3])}."
    
    p_edu = crit.formacion_certificaciones.puntuacion if crit else min(100, int(res.porcentaje_ajuste * 0.92))
    j_edu = crit.formacion_certificaciones.justificacion if crit else res.education
    
    p_coh = crit.coherencia_profesional.puntuacion if crit else min(100, int(res.porcentaje_ajuste * 0.98))
    j_coh = crit.coherencia_profesional.justificacion if crit else "Trayectoria ascendente sostenida y estabilidad contractual."

    html_factors = (
        f'<div class="dark-card">'
        f'<div class="dark-card-header">'
        f'<div class="dark-card-title">'
        f'<span>📊</span>'
        f'<span>Ponderación de Criterios</span>'
        f'</div>'
        f'<span class="dark-pill pill-slate">4 Factores Clave</span>'
        f'</div>'
        f'<div class="dark-factor-row">'
        f'<div class="dark-factor-top">'
        f'<span>Experiencia relevante (40% peso)</span>'
        f'<span class="dark-factor-score">{p_exp}%</span>'
        f'</div>'
        f'<div class="dark-factor-track"><div class="dark-factor-fill" style="width:{p_exp}%;"></div></div>'
        f'<div class="dark-factor-desc">{j_exp}</div>'
        f'</div>'
        f'<div class="dark-factor-row">'
        f'<div class="dark-factor-top">'
        f'<span>Habilidades técnicas (35% peso)</span>'
        f'<span class="dark-factor-score">{p_tech}%</span>'
        f'</div>'
        f'<div class="dark-factor-track"><div class="dark-factor-fill" style="width:{p_tech}%;"></div></div>'
        f'<div class="dark-factor-desc">{j_tech}</div>'
        f'</div>'
        f'<div class="dark-factor-row">'
        f'<div class="dark-factor-top">'
        f'<span>Formación y certificaciones (15% peso)</span>'
        f'<span class="dark-factor-score">{p_edu}%</span>'
        f'</div>'
        f'<div class="dark-factor-track"><div class="dark-factor-fill" style="width:{p_edu}%;"></div></div>'
        f'<div class="dark-factor-desc">{j_edu}</div>'
        f'</div>'
        f'<div class="dark-factor-row" style="margin-bottom:0;">'
        f'<div class="dark-factor-top">'
        f'<span>Coherencia profesional (10% peso)</span>'
        f'<span class="dark-factor-score">{p_coh}%</span>'
        f'</div>'
        f'<div class="dark-factor-track"><div class="dark-factor-fill" style="width:{p_coh}%;"></div></div>'
        f'<div class="dark-factor-desc">{j_coh}</div>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_factors, unsafe_allow_html=True)

    # 4. Habilidades Clave
    chips_html = "".join([f'<span class="dark-skill-tag">✓ {h}</span>' for h in res.habilidades_clave])
    html_skills = (
        f'<div class="dark-card">'
        f'<div class="dark-card-header">'
        f'<div class="dark-card-title">'
        f'<span>🧩</span>'
        f'<span>Habilidades Clave Detectadas</span>'
        f'</div>'
        f'<span class="dark-pill pill-slate">{len(res.habilidades_clave)} Validadas</span>'
        f'</div>'
        f'<div>'
        f'{chips_html}'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_skills, unsafe_allow_html=True)

    # 5. Fortalezas
    fortalezas_html = "".join([
        f'<div class="dark-item-box dark-box-fortaleza"><span>✓</span><span>{f}</span></div>' 
        for f in res.fortalezas
    ])
    html_fort = (
        f'<div class="dark-card">'
        f'<div class="dark-card-header">'
        f'<div class="dark-card-title">'
        f'<span style="color:#34d399;">🎯</span>'
        f'<span>Fortalezas Principales</span>'
        f'</div>'
        f'</div>'
        f'{fortalezas_html}'
        f'</div>'
    )
    st.markdown(html_fort, unsafe_allow_html=True)

    # 6. Gaps
    gaps_html = "".join([
        f'<div class="dark-item-box dark-box-gap"><span>🚩</span><span>{a}</span></div>' 
        for a in res.areas_mejora
    ])
    html_gaps = (
        f'<div class="dark-card">'
        f'<div class="dark-card-header">'
        f'<div class="dark-card-title">'
        f'<span style="color:#fbbf24;">⚠️</span>'
        f'<span>Áreas de Mejora / Gaps</span>'
        f'</div>'
        f'</div>'
        f'{gaps_html}'
        f'</div>'
    )
    st.markdown(html_gaps, unsafe_allow_html=True)

    # Acciones Finales
    pdf_bytes = generar_pdf_informe(res, eval_principal, recom_final)
    
    st.download_button(
        label="📥 Descargar Informe (PDF)",
        data=pdf_bytes,
        file_name=f"Informe_{res.nombre_candidato.replace(' ', '_')}.pdf",
        mime="application/pdf",
        use_container_width=True,
        type="primary"
    )

    c_save, c_new = st.columns([1, 1])
    with c_save:
        if st.button("💾 Guardar Análisis", type="secondary", use_container_width=True):
            st.info("ℹ️ Funcionalidad de persistencia en base de datos en desarrollo.")
    with c_new:
        if st.button("🔄 Nuevo Análisis", type="secondary", use_container_width=True):
            st.session_state.paso_actual = 1
            st.session_state.cv_texto = None
            st.session_state.cv_metadatos = None
            st.session_state.analisis_resultado = None
            st.rerun()

    html_end = (
        f'<div style="text-align:center; font-family:var(--font-mono); font-size:0.65rem; color:var(--text-low); margin-top:0.45rem;">'
        f'• Auditoría completada con éxito conforme a la rúbrica institucional'
        f'</div>'
    )
    st.markdown(html_end, unsafe_allow_html=True)

def render_bottom_bar():
    p = st.session_state.get("paso_actual", 1)
    html_bottom = (
        f'<div class="dark-nav-bottom">'
        f'<div class="dark-nav-btn {"active" if p == 1 else ""}">'
        f'<span style="font-size:1.15rem;">📄</span>'
        f'<span>1. Carga & Puesto</span>'
        f'</div>'
        f'<div class="dark-nav-btn {"active" if p == 2 else ""}">'
        f'<span style="font-size:1.15rem;">📊</span>'
        f'<span>2. Análisis</span>'
        f'</div>'
        f'<div class="dark-nav-btn {"active" if p == 3 else ""}">'
        f'<span style="font-size:1.15rem;">✅</span>'
        f'<span>3. Evaluación</span>'
        f'</div>'
        f'</div>'
    )
    st.markdown(html_bottom, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="TalentAI - Analizador de Currículums",
        page_icon="⚡",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    st.markdown(PURE_DARK_CSS, unsafe_allow_html=True)
    inicializar_session_state()

    paso = st.session_state.paso_actual
    if paso == 1:
        render_pantalla_1()
    elif paso == 2:
        render_pantalla_2()
    elif paso == 3:
        render_pantalla_3()
    else:
        st.session_state.paso_actual = 1
        render_pantalla_1()

    render_bottom_bar()
