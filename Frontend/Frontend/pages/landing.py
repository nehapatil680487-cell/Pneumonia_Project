import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PneumoScan AI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE
# =========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

/* ---------- Main App ---------- */

.stApp {
    background:
        radial-gradient(circle at top left, #e8f8ff 0%, transparent 35%),
        radial-gradient(circle at bottom right, #dff7f2 0%, transparent 35%),
        linear-gradient(135deg, #f7fbff 0%, #eef8f7 100%);
    font-family: "Segoe UI", Arial, sans-serif;
    color: #17324d;
}

/* Remove Streamlit top padding */

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 850px;
}

/* ---------- Header ---------- */

.logo {
    text-align: center;
    font-size: 52px;
    margin-bottom: 5px;
}

.main-title {
    text-align: center;
    font-size: 46px;
    font-weight: 800;
    color: #123b5d;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #5d7182;
    margin-bottom: 30px;
}

/* ---------- Medical Badge ---------- */

.badge-container {
    text-align: center;
    margin-bottom: 25px;
}

.badge {
    display: inline-block;
    background: #e2f5f1;
    color: #147d6f;
    padding: 8px 18px;
    border-radius: 30px;
    font-size: 14px;
    font-weight: 600;
    border: 1px solid #c7ebe4;
}

/* ---------- Cards ---------- */

.card {
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid #dceaf0;
    border-radius: 18px;
    padding: 24px 26px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px rgba(24, 63, 88, 0.08);
}

.card h3 {
    color: #164c70;
    font-size: 21px;
    margin-top: 0;
    margin-bottom: 10px;
}

.card p {
    color: #607383;
    font-size: 16px;
    line-height: 1.7;
}

/* ---------- Feature Row ---------- */

.feature-row {
    display: flex;
    gap: 15px;
    margin-bottom: 22px;
}

.feature {
    flex: 1;
    background: white;
    border: 1px solid #dceaf0;
    border-radius: 16px;
    padding: 20px 15px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(24, 63, 88, 0.06);
}

.feature-icon {
    font-size: 30px;
    margin-bottom: 8px;
}

.feature-title {
    color: #164c70;
    font-size: 15px;
    font-weight: 700;
}

.feature-text {
    color: #728392;
    font-size: 13px;
    margin-top: 5px;
}

/* ---------- Button ---------- */

div.stButton {
    display: flex;
    justify-content: center;
}

div.stButton > button {
    background: linear-gradient(
        135deg,
        #087f8c,
        #159a8c
    ) !important;

    color: white !important;
    border: none !important;
    border-radius: 12px !important;

    width: 240px !important;
    height: 52px !important;

    font-size: 17px !important;
    font-weight: 700 !important;

    box-shadow: 0 7px 18px rgba(8, 127, 140, 0.25);
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(8, 127, 140, 0.35);
}

/* ---------- Disclaimer ---------- */

.disclaimer {
    background: #fff8e6;
    border: 1px solid #f1dfaa;
    color: #735b1d;
    border-radius: 12px;
    padding: 15px 18px;
    margin-top: 28px;
    text-align: center;
    font-size: 14px;
    line-height: 1.5;
}

/* ---------- Footer ---------- */

.footer {
    text-align: center;
    color: #8796a3;
    font-size: 13px;
    margin-top: 25px;
}

/* ---------- Mobile ---------- */

@media (max-width: 650px) {

    .main-title {
        font-size: 36px;
    }

    .subtitle {
        font-size: 16px;
    }

    .feature-row {
        flex-direction: column;
    }

    .card {
        padding: 20px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="logo">🩺</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-title">PneumoScan AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-assisted pneumonia screening and patient diagnosis management'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="badge-container">'
    '<span class="badge">● AI-Powered Medical Screening</span>'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# WELCOME CARD
# =========================================================

st.markdown("""
<div class="card">

<h3> Welcome to PneumoScan AI</h3>

<p>
PneumoScan AI is a medical assistance platform designed to
support pneumonia screening using chest X-ray analysis
and patient medical parameters.
</p>

<p>
The system combines AI-based analysis with patient information
to generate a preliminary screening result and medical report.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# FEATURES
# =========================================================

st.markdown("""
<div class="feature-row">

<div class="feature">
    <div class="feature-icon"></div>
    <div class="feature-title">X-Ray Analysis</div>
    <div class="feature-text">
        AI-assisted chest X-ray screening
    </div>
</div>

<div class="feature">
    <div class="feature-icon"></div>
    <div class="feature-title">Medical Parameters</div>
    <div class="feature-text">
        Blood and oxygen parameter analysis
    </div>
</div>

<div class="feature">
    <div class="feature-icon"></div>
    <div class="feature-title">Medical Report</div>
    <div class="feature-text">
        Generate and download patient reports
    </div>
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# HOW IT WORKS
# =========================================================

st.markdown("""
<div class="card">

<h3> How It Works</h3>

<p>
<strong>01 — Login</strong><br>
Access the patient diagnosis system through the secure login.
</p>

<p>
<strong>02 — Patient Information</strong><br>
Enter the required patient details.
</p>

<p>
<strong>03 — Medical Data</strong><br>
Upload the chest X-ray and enter required medical parameters.
</p>

<p>
<strong>04 — AI Analysis</strong><br>
The system processes the available information using trained AI models.
</p>

<p>
<strong>05 — Result & Report</strong><br>
View the screening result and generate a PDF medical report.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# GET STARTED
# =========================================================

st.markdown(
    '<div style="text-align:center; color:#526879; '
    'font-size:15px; margin-bottom:10px;">'
    'Ready to begin the screening process?'
    '</div>',
    unsafe_allow_html=True
)

if st.button("  Get Started"):

    if st.session_state.logged_in:

        st.switch_page(
            "pages/patient_input.py"
        )

    else:

        st.switch_page(
            "pages/login.py"
        )





# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    🩺 PneumoScan AI &nbsp;•&nbsp;
    AI-Assisted Lung Disease Screening
</div>
""", unsafe_allow_html=True)