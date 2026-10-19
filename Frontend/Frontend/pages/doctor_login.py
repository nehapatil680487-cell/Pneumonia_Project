import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Doctor Login | PneumoScan AI",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# =========================================================
# SESSION STATE
# =========================================================

if "doctor_login" not in st.session_state:
    st.session_state.doctor_login = False

# =========================================================
# CSS
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(14,165,233,0.18),
            transparent 35%
        ),
        radial-gradient(
            circle at 90% 90%,
            rgba(34,197,94,0.12),
            transparent 35%
        ),
        linear-gradient(
            135deg,
            #0f172a,
            #1e293b
        );

    font-family: "Segoe UI", Arial, sans-serif;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* LOGIN CARD */

.login-wrapper {
    max-width: 500px;
    margin: 70px auto 0 auto;
    padding: 40px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 24px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.30);
}

/* LOGO */

.login-logo {
    width: 80px;
    height: 80px;
    margin: 0 auto 20px auto;
    border-radius: 22px;

    display: flex;
    align-items: center;
    justify-content: center;

    background: linear-gradient(
        135deg,
        #0ea5e9,
        #2563eb
    );

    font-size: 40px;

    box-shadow:
        0 12px 30px rgba(14,165,233,0.30);
}

/* TITLE */

.login-title {
    text-align: center;
    color: white;
    font-size: 32px;
    font-weight: 800;
}

.login-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 14px;
    margin-top: 7px;
    margin-bottom: 30px;
}

/* LABELS */

label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* INPUTS */

.stTextInput input {
    background: white !important;
    color: #0f172a !important;
    border: none !important;
    border-radius: 11px !important;
    height: 48px !important;
    padding-left: 15px !important;
}

/* BUTTON */

div.stButton > button {
    width: 100%;
    min-height: 45px;

    border-radius: 11px !important;
    border: none !important;

    background: linear-gradient(
        135deg,
        #0ea5e9,
        #2563eb
    ) !important;

    color: white !important;

    font-weight: 700 !important;
}

div.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 25px rgba(14,165,233,0.30);
}

/* INFO */

.demo-info {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 20px;
}

/* FOOTER */

.login-footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    margin-top: 35px;
    line-height: 1.7;
}

</style>
""",
    unsafe_allow_html=True
)

# =========================================================
# IF ALREADY LOGGED IN
# =========================================================

if st.session_state.doctor_login:

    st.markdown(
        """
        <div class="login-wrapper">

            <div class="login-logo">
                🩺
            </div>

            <div class="login-title">
                Welcome Doctor
            </div>

            <div class="login-subtitle">
                You are already logged in.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        "🩺 Open Doctor Dashboard",
        use_container_width=True
    ):
        st.switch_page(
            "pages/doctor_dashboard.py"
        )

    st.stop()

# =========================================================
# LOGIN HEADER
# =========================================================

st.markdown(
    """
<div class="login-wrapper">
<div class="login-logo">🩺</div>
<div class="login-title">Doctor Login</div>
<div class="login-subtitle">
PneumoScan AI Healthcare Portal
</div>
</div>
""",
    unsafe_allow_html=True
)

st.write("")

# =========================================================
# INPUTS
# =========================================================

doctor_id = st.text_input(
    "Doctor ID",
    placeholder="Enter Doctor ID"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter Password"
)

st.write("")

# =========================================================
# BUTTONS
# =========================================================

col1, col2 = st.columns(2)

with col1:

    login_button = st.button(
        " Login",
        use_container_width=True
    )

with col2:

    home_button = st.button(
        " Home",
        use_container_width=True
    )

# =========================================================
# LOGIN LOGIC
# =========================================================

if login_button:

    if doctor_id.strip() == "doctor" and password == "12345":

        # IMPORTANT
        # Save login state before switching page

        st.session_state.doctor_login = True

        st.switch_page(
            "pages/docter_dashboard.py"
        )

    else:

        st.error(
            " Invalid Doctor ID or Password"
        )

# =========================================================
# HOME
# =========================================================

if home_button:

    st.switch_page(
        "app.py"
    )

# =========================================================
# DEMO LOGIN
# =========================================================

st.markdown(
    """
<div class="demo-info">
Demo Login<br>
Doctor ID: <b>doctor</b>
&nbsp; | &nbsp;
Password: <b>12345</b>
</div>

<div class="login-footer">
Powered by <b>PneumoScan AI</b><br>
AI-Assisted Pneumonia Screening System
</div>
""",
    unsafe_allow_html=True
)