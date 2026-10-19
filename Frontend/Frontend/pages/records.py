import streamlit as st
import requests
import streamlit.components.v1 as components

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Patient Records",
    page_icon="📋",
    layout="wide"
)

FASTAPI_URL = "http://127.0.0.1:8000"

HISTORY_URL = f"{FASTAPI_URL}/history"

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {

    background:
    linear-gradient(
        135deg,
        #1f4037,
        #99f2c8
    );

    font-family:
    'Segoe UI', sans-serif;
}

h1, h2, h3 {

    color: white !important;
}

div.stButton > button {

    background: #007BFF !important;

    color: white !important;

    width: 100%;

    height: 45px;

    border-radius: 10px;

    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================

st.title("📋 Patient Records")

st.markdown("---")

# =========================================================
# LOAD HISTORY
# =========================================================

try:

    response = requests.get(
        HISTORY_URL,
        timeout=30
    )

except requests.exceptions.ConnectionError:

    st.error(
        "❌ FastAPI is not running."
    )

    st.stop()

except Exception as e:

    st.error(
        f"❌ Error connecting to FastAPI: {e}"
    )

    st.stop()

# =========================================================
# DISPLAY
# =========================================================

if response.status_code == 200:

    components.html(
        response.text,
        height=1000,
        scrolling=True
    )

else:

    st.error(
        f"❌ Could not load records. "
        f"Status: {response.status_code}"
    )

# =========================================================
# NAVIGATION
# =========================================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    if st.button("🏠 Home"):

        st.switch_page(
            "pages/landing.py"
        )

with col2:

    if st.button("🩺 New Diagnosis"):

        st.switch_page(
            "pages/patient_input.py"
        )