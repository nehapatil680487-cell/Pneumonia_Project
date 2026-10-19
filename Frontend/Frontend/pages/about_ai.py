import streamlit as st

st.set_page_config(page_title="About PneumoScan AI", page_icon="", layout="wide")

st.markdown("""
<style>
/* GLOBAL */
.stApp {
    background: #f7f9fc;
    color: #172033;
    font-family: "Segoe UI", Arial, sans-serif;
}
#MainMenu, header, footer { visibility: hidden; }
.block-container { max-width: 1200px; padding-top: 45px; padding-bottom: 50px; }

/* TOP LINE & BRAND */
.top-line { border-top: 4px solid #123b6d; margin-bottom: 32px; }
.brand {
    font-size: 14px; font-weight: 700; letter-spacing: 2px;
    color: #123b6d; margin-bottom: 12px; text-transform: uppercase;
}
.main-title {
    font-size: 46px; font-weight: 700; color: #102a43;
    margin-bottom: 12px; line-height: 1.2;
}
.main-title span { color: #1677b8; }
.subtitle {
    max-width: 850px; font-size: 18px; line-height: 1.7; color: #617083;
}

/* SECTIONS */
.section {
    margin-top: 55px; padding-top: 22px;
    border-top: 1px solid #d8e0e8;
}
.section-number {
    font-size: 12px; font-weight: 800; letter-spacing: 2px;
    color: #1677b8; margin-bottom: 7px; text-transform: uppercase;
}
.section-title {
    font-size: 27px; font-weight: 700; color: #102a43; margin-bottom: 15px;
}
.section-text {
    max-width: 950px; font-size: 15px; line-height: 1.8; color: #617083;
}

/* WORKFLOW */
.workflow {
    display: flex; align-items: center; margin-top: 30px; gap: 12px; flex-wrap: wrap;
}
.workflow-item { flex: 1; text-align: center; min-width: 180px; }
.workflow-number {
    font-size: 12px; font-weight: 800; color: #1677b8;
    margin-bottom: 7px; letter-spacing: 1px;
}
.workflow-name { font-size: 16px; font-weight: 700; color: #172033; }
.workflow-desc {
    margin-top: 5px; font-size: 13px; line-height: 1.5; color: #7a8796;
}
.workflow-arrow { color: #aab6c2; font-size: 22px; font-weight: 700; }

/* CLINICAL PARAMETERS */
.parameters {
    display: grid; grid-template-columns: repeat(3, 1fr);
    margin-top: 28px; border-top: 1px solid #d8e0e8;
    border-bottom: 1px solid #d8e0e8; gap: 0;
}
.parameter { padding: 22px 18px; border-right: 1px solid #d8e0e8; }
.parameter:last-child { border-right: none; }
.parameter-type {
    font-size: 10px; font-weight: 800; letter-spacing: 1.5px;
    color: #1677b8; margin-bottom: 7px; text-transform: uppercase;
}
.parameter-name { font-size: 17px; font-weight: 700; color: #172033; margin-bottom: 8px; }
.parameter-desc { font-size: 13px; line-height: 1.6; color: #718096; }

/* MODEL TABLE */
.model-table {
    width: 100%; border-collapse: collapse; margin-top: 25px;
    background: #ffffff; border: 1px solid #dce3eb;
    border-radius: 6px; overflow: hidden;
}
.model-table th {
    text-align: left; padding: 13px 10px;
    border-bottom: 2px solid #123b6d; font-size: 11px;
    letter-spacing: 1px; color: #123b6d;
    text-transform: uppercase; background: #f4f7fb;
}
.model-table td {
    padding: 15px 10px; border-bottom: 1px solid #dce3eb;
    font-size: 14px; color: #617083;
}
.model-table td:first-child { font-weight: 700; color: #172033; }
.model-table tr:last-child td { border-bottom: none; }

/* SCREENING DECISION */
.decision-row {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: 35px; margin-top: 25px;
}
.decision-item {
    background: #ffffff; padding: 22px 25px;
    border-left: 3px solid #1677b8;
    box-shadow: 0 2px 8px rgba(20, 50, 80, 0.06);
    border-radius: 6px;
}
.decision-title { font-size: 18px; font-weight: 700; color: #102a43; margin-bottom: 9px; }
.decision-text { font-size: 14px; line-height: 1.7; color: #617083; }

/* GRAD CAM */
.gradcam-box {
    margin-top: 25px; background: #ffffff; padding: 24px 28px;
    border-left: 3px solid #1677b8;
    box-shadow: 0 2px 8px rgba(20, 50, 80, 0.06);
    border-radius: 6px;
}
.gradcam-label {
    font-size: 10px; font-weight: 800; letter-spacing: 2px;
    color: #1677b8; margin-bottom: 8px; text-transform: uppercase;
}
.gradcam-title { font-size: 18px; font-weight: 700; color: #102a43; margin-bottom: 8px; }
.gradcam-text { font-size: 14px; line-height: 1.7; color: #617083; }

/* REPORT */
.report-text {
    max-width: 950px; background: #ffffff; padding: 22px 25px;
    border-left: 3px solid #14a38b;
    box-shadow: 0 2px 8px rgba(20, 50, 80, 0.06);
    font-size: 14px; line-height: 1.8; color: #617083;
    border-radius: 6px;
}

/* MEDICAL NOTICE */
.medical-notice {
    margin-top: 48px; background: #eef5fa;
    border-top: 1px solid #cbdce9; border-bottom: 1px solid #cbdce9;
    padding: 20px 25px; border-radius: 6px;
}
.notice-heading {
    font-size: 12px; font-weight: 800; letter-spacing: 1.5px;
    color: #123b6d; margin-bottom: 7px; text-transform: uppercase;
}
.notice-text { font-size: 13px; line-height: 1.7; color: #617083; }

/* BUTTON */
div.stButton > button {
    margin-top: 32px; background: #123b6d !important; color: white !important;
    border: none !important; border-radius: 6px !important;
    padding: 10px 25px !important; font-size: 14px !important;
    font-weight: 600 !important; cursor: pointer;
    transition: background 0.2s ease;
}
div.stButton > button:hover { background: #1677b8 !important; }

/* FOOTER */
.footer {
    margin-top: 55px; padding-top: 18px;
    border-top: 1px solid #dce3eb; text-align: center;
    color: #8a97a6; font-size: 12px;
}

/* MOBILE */
@media (max-width: 900px) {
    .main-title { font-size: 35px; }
    .workflow { flex-direction: column; align-items: flex-start; }
    .workflow-item { text-align: left; width: 100%; }
    .workflow-arrow { display: none; }
    .parameters { grid-template-columns: 1fr; }
    .parameter { border-right: none; border-bottom: 1px solid #d8e0e8; }
    .decision-row { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div class="top-line"></div>
<div class="brand">PNEUMOSCAN AI / SYSTEM OVERVIEW</div>
<div class="main-title">Intelligent <span>Pneumonia Screening</span></div>
<div class="subtitle">
    An AI-assisted multimodal system that combines chest X-ray
    analysis with clinical parameters to support preliminary
    pneumonia screening and severity assessment.
</div>
""", unsafe_allow_html=True)

# 01 — HOW IT WORKS
st.markdown("""
<div class="section">
<div class="section-number">01 / HOW IT WORKS</div>
<div class="section-title">From patient data to screening result</div>
<div class="section-text">
    PneumoScan AI analyzes different sources of patient information
    using specialized machine learning models. The individual
    predictions are then combined to provide a more comprehensive
    screening assessment.
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="workflow">
    <div class="workflow-item">
        <div class="workflow-number">01</div>
        <div class="workflow-name">Patient Data</div>
        <div class="workflow-desc">Patient information and clinical parameters</div>
    </div>
    <div class="workflow-arrow">→</div>
    <div class="workflow-item">
        <div class="workflow-number">02</div>
        <div class="workflow-name">AI Analysis</div>
        <div class="workflow-desc">Individual models analyze each input</div>
    </div>
    <div class="workflow-arrow">→</div>
    <div class="workflow-item">
        <div class="workflow-number">03</div>
        <div class="workflow-name">Multimodal Fusion</div>
        <div class="workflow-desc">Model outputs are combined</div>
    </div>
    <div class="workflow-arrow">→</div>
    <div class="workflow-item">
        <div class="workflow-number">04</div>
        <div class="workflow-name">Screening Result</div>
        <div class="workflow-desc">Pneumonia and severity assessment</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 02 — AI MODELS
st.markdown("""
<div class="section">
<div class="section-number">02 / AI MODELS</div>
<div class="section-title">Machine learning components</div>
<div class="section-text">
    PneumoScan AI uses different models for different types of
    medical information.
</div>
<table class="model-table">
<tr><th>MODEL</th><th>TYPE</th><th>INPUT</th><th>PURPOSE</th></tr>
<tr><td>Chest X-Ray Model</td><td>CNN</td><td>Chest X-ray</td><td>Detects image patterns associated with pneumonia.</td></tr>
<tr><td>Blood Model</td><td>ANN</td><td>Blood parameters</td><td>Analyzes numerical blood-count information.</td></tr>
<tr><td>Oxygen Model</td><td>ANN</td><td>Oxygen data</td><td>Analyzes physiological oxygen information.</td></tr>
</table>
</div>
""", unsafe_allow_html=True)

# 03 — CLINICAL PARAMETERS
st.markdown("""
<div class="section">
<div class="section-number">03 / CLINICAL PARAMETERS</div>
<div class="section-title">Multiple sources of clinical evidence</div>
<div class="parameters">
    <div class="parameter">
        <div class="parameter-type">IMAGING</div>
        <div class="parameter-name">Chest X-Ray</div>
        <div class="parameter-desc">Provides visual information about lung abnormalities analyzed by the CNN model.</div>
    </div>
    <div class="parameter">
        <div class="parameter-type">LABORATORY</div>
        <div class="parameter-name">Blood Parameters</div>
        <div class="parameter-desc">Numerical blood measurements are processed by the blood analysis model.</div>
    </div>
    <div class="parameter">
        <div class="parameter-type">PHYSIOLOGICAL</div>
        <div class="parameter-name">Oxygen Level</div>
        <div class="parameter-desc">Oxygen-related information provides additional physiological evidence.</div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# 04 — SCREENING DECISION
st.markdown("""
<div class="section">
<div class="section-number">04 / SCREENING DECISION</div>
<div class="section-title">How the system reaches a result</div>
<div class="decision-row">
    <div class="decision-item">
        <div class="decision-title">Pneumonia Screening</div>
        <div class="decision-text">
            The chest X-ray, blood and oxygen analysis provide
            complementary evidence. Their outputs are combined
            to determine the overall pneumonia screening result.
        </div>
    </div>
    <div class="decision-item">
        <div class="decision-title">Severity Assessment</div>
        <div class="decision-text">
            When pneumonia is detected, the system can further
            assess severity using X-ray involvement and
            relevant clinical parameters to support NSCAP or
            SCAP classification.
        </div>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# 05 — EXPLAINABLE AI
st.markdown("""
<div class="section">
<div class="section-number">05 / EXPLAINABLE AI</div>
<div class="section-title">Understanding the X-ray prediction</div>
<div class="gradcam-box">
    <div class="gradcam-label">GRAD-CAM</div>
    <div class="gradcam-title">Visual explanation of the AI prediction</div>
    <div class="gradcam-text">
        PneumoScan AI uses Gradient-weighted Class Activation
        Mapping to highlight regions of the chest X-ray that
        contributed to the CNN prediction. This helps users
        understand where the model focused during analysis.
    </div>
</div>
</div>
""", unsafe_allow_html=True)

# 06 — SCREENING REPORT
st.markdown("""
<div class="section">
<div class="section-number">06 / SCREENING REPORT</div>
<div class="section-title">A structured result for clinical review</div>
<div class="report-text">
    After analysis, PneumoScan AI generates a structured
    screening report containing patient information, prediction
    result, confidence, relevant clinical values, severity
    assessment and supporting AI information.
</div>
</div>
""", unsafe_allow_html=True)

# MEDICAL NOTICE
st.markdown("""
<div class="medical-notice">
    <div class="notice-heading">IMPORTANT MEDICAL NOTICE</div>
    <div class="notice-text">
        PneumoScan AI is an AI-assisted screening system and is
        not intended to replace a qualified medical professional.
        The generated result should be reviewed together with
        the patient's clinical condition and other appropriate
        medical investigations.
    </div>
</div>
""", unsafe_allow_html=True)

# BACK HOME
if st.button("← Back to Home"):
    st.switch_page("app.py")

# FOOTER
st.markdown("""
<div class="footer">
    PneumoScan AI · AI-Assisted Pneumonia Screening System
</div>
""", unsafe_allow_html=True)