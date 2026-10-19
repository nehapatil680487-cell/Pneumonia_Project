import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Pneumonia Precautions",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at top left, #dffcf0 0%, transparent 35%),
            linear-gradient(135deg, #073b4c 0%, #118ab2 48%, #06d6a0 100%);
        color: #ffffff;
    }

    /* Remove default top spacing */
    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hide Streamlit menu and footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* Header */
    .hero {
        padding: 2rem 2.3rem;
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 25px;
        background: rgba(255, 255, 255, 0.14);
        backdrop-filter: blur(14px);
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.20);
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 0.7rem;
        color: white;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        line-height: 1.7;
        color: #eafff8;
        max-width: 800px;
    }

    .badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 999px;
        background: #ffd166;
        color: #17324d;
        font-weight: 700;
        font-size: 0.85rem;
        margin-bottom: 1rem;
    }

    /* Section headings */
    .section-heading {
        color: white;
        font-size: 1.65rem;
        font-weight: 800;
        margin: 1.8rem 0 1rem 0;
    }

    .section-description {
        color: #e7fff8;
        font-size: 1rem;
        margin-top: -0.5rem;
        margin-bottom: 1.2rem;
    }

    /* Information cards */
    .info-card {
        min-height: 190px;
        padding: 1.35rem;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.94);
        color: #17324d;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        margin-bottom: 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .info-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.22);
    }

    .card-title {
        font-size: 1.12rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
        color: #073b4c;
    }

    .card-text {
        font-size: 0.95rem;
        line-height: 1.55;
        color: #40566b;
    }

    /* Emergency card */
    .emergency-card {
        padding: 1.4rem 1.6rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #ff6b6b, #d62828);
        color: white;
        box-shadow: 0 10px 25px rgba(120, 0, 0, 0.25);
        margin: 1.2rem 0;
    }

    .emergency-title {
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 0.6rem;
    }

    .emergency-text {
        line-height: 1.65;
        font-size: 0.98rem;
    }

    /* AI reminder */
    .ai-card {
        padding: 1.5rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #8338ec, #3a86ff);
        color: white;
        box-shadow: 0 10px 25px rgba(38, 0, 100, 0.25);
        margin-top: 1.2rem;
    }

    .ai-title {
        font-size: 1.35rem;
        font-weight: 800;
        margin-bottom: 0.8rem;
    }

    .ai-list {
        margin: 0;
        padding-left: 1.2rem;
        line-height: 1.8;
    }

    /* Buttons */
    div.stButton > button {
        width: 100%;
        min-height: 45px;
        border: 0;
        border-radius: 12px;
        background: #ffd166;
        color: #17324d;
        font-size: 1rem;
        font-weight: 800;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background: #ffe29a;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.18);
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.25);
        color: #eafff8;
        font-size: 0.9rem;
    }

    /* Mobile adjustments */
    @media (max-width: 700px) {
        .hero {
            padding: 1.4rem;
        }

        .hero-subtitle {
            font-size: 0.98rem;
        }

        .info-card {
            min-height: auto;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns([5, 1], vertical_alignment="center")

with header_col1:
    st.markdown(
        """
        <div class="hero">
            <div class="badge">🛡️ HEALTH & SAFETY GUIDE</div>
            <div class="hero-title">Pneumonia Precautions</div>
            <div class="hero-subtitle">
                Simple, practical steps to support respiratory health,
                reduce infection risks, and recognize warning signs early.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_col2:
    st.write("")
    if st.button(" Home", use_container_width=True):
        st.switch_page("pages/landing.py")

# =========================================================
# GENERAL PRECAUTIONS
# =========================================================

st.markdown(
    '<div class="section-heading">🩺 Everyday Precautions</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    "Small daily habits can help protect your lungs and overall wellbeing."
    "</div>",
    unsafe_allow_html=True,
)

precautions = [
    ("Wear a mask when appropriate",
     "Consider wearing a well-fitting mask in crowded or poorly ventilated places."),

    ("Wash your hands regularly",
     "Clean your hands with soap and water, especially before eating and after coughing or sneezing."),

    ("Avoid smoke and pollution",
     "Do not smoke, and minimize exposure to tobacco smoke, dust, and polluted air."),

    ("Stay hydrated",
     "Drink enough fluids unless a healthcare professional has advised you to restrict them."),

    ("Eat a balanced diet",
     "Include a variety of nutritious foods to support general health and recovery."),

    ("Rest properly",
     "Adequate sleep and rest can support your body while it is recovering."),

    ("Cover coughs and sneezes",
     "Use a tissue or your elbow and dispose of used tissues safely."),

    ("Improve ventilation",
     "Keep indoor spaces clean and well ventilated whenever possible."),
]

for row_start in range(0, len(precautions), 4):
    columns = st.columns(4, gap="medium")

    for column, item in zip(columns, precautions[row_start:row_start + 4]):
        title, description = item

        with column:
            st.markdown(
                f"""
                <div class="info-card">
                    <div class="card-title">{title}</div>
                    <div class="card-text">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# =========================================================
# WARNING SIGNS
# =========================================================

st.markdown(
    '<div class="section-heading"> Warning Signs</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="emergency-card">
        <div class="emergency-title">Seek medical help promptly if symptoms are severe.</div>
        <div class="emergency-text">
            Be especially alert for difficulty breathing, severe or persistent
            chest pain, high fever with chills, a worsening cough, unusually low
            oxygen readings, extreme weakness, or confusion.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

warning_col1, warning_col2, warning_col3 = st.columns(3)

with warning_col1:
    st.markdown("###  Breathing")
    st.markdown("Difficulty breathing or shortness of breath.")

with warning_col2:
    st.markdown("###  Fever")
    st.markdown("High or persistent fever, particularly with chills.")

with warning_col3:
    st.markdown("###  Confusion")
    st.markdown("Confusion, extreme weakness, or unusual drowsiness.")

# =========================================================
# PNEUMOSCAN AI SECTION
# =========================================================

st.markdown(
    """
    <div class="ai-card">
        <div class="ai-title"> Using PneumoScan AI?</div>
        <ul class="ai-list">
            <li>Upload a clear and properly positioned chest X-ray.</li>
            <li>Enter medical information as accurately as possible.</li>
            <li>Use the result only as a screening aid.</li>
            <li>Do not use the result as a diagnosis.</li>
            <li>Discuss medical decisions with a qualified healthcare professional.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# FOOTER AND BACK BUTTON
# =========================================================

st.markdown(
    """
    <div class="footer">
        PneumoScan AI • Screening assistance only • Not a replacement for medical advice
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

if st.button("← Back to Home", use_container_width=True):
    st.switch_page("pages/landing.py")