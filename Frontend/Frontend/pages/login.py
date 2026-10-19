import streamlit as st
from database import add_user, check_user

st.set_page_config(page_title="PneumoScan AI", layout="wide")

# ---------- SESSION INIT ----------
if "page" not in st.session_state:
    st.session_state.page = "login"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

# ---------- CSS ----------
st.markdown("""
<style>
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.stApp {
    background: linear-gradient(to right, #e3f2fd, #f5f7fa);
}

.title {
    text-align: center;
    font-size: 30px;
    font-weight: 700;
    color: #0b3c5d;
    margin-bottom: 20px;
}

.main-heading {
    text-align: center;
    font-size: 40px;
    font-weight: 800;
    color: #0b3c5d;
    margin-top: 10px;
}

.sub-heading {
    text-align: center;
    font-size: 16px;
    color: #555;
    margin-bottom: 25px;
}

input[type="text"], input[type="password"] {
    border: 2px solid #1e90ff !important;
    border-radius: 6px !important;
}

div.stButton > button {
    width: 140px;
    height: 42px;
    border-radius: 8px;
    background: #1e90ff;
    color: white;
    font-weight: 600;
    border: none;
}

div.stButton > button:hover {
    background: #0077cc;
}

.footer {
    text-align: center;
    font-size: 12px;
    color: #777;
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("""
<div class="main-heading">🫁 PneumoScan AI</div>
<div class="sub-heading">AI-powered Pneumonia Detection System</div>
<hr style="height:3px;border:none;background-color:black;">
""", unsafe_allow_html=True)

# ---------- LOGIN ----------
def login():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="title"> Login</div>', unsafe_allow_html=True)

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        st.markdown("<br>", unsafe_allow_html=True)

        b1, b2 = st.columns(2)

        with b1:
            if st.button("Login"):
                if username.strip() == "" or password.strip() == "":
                    st.error("Please fill all fields")
                else:
                    user = check_user(username, password)
                    if user:
                        st.success("Login successful 🎉")

                        # ✅ STORE SESSION VALUES
                        st.session_state.logged_in = True
                        st.session_state.username = username

                        st.rerun()
                    else:
                        st.error("Invalid username or password")

        with b2:
            if st.button("Signup"):
                st.session_state.page = "signup"
                st.rerun()

# ---------- SIGNUP ----------
def signup():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="title"> Sign Up</div>', unsafe_allow_html=True)

        username = st.text_input("Username", key="su_user")
        password = st.text_input("Password", type="password", key="su_pass")
        confirm_password = st.text_input("Confirm Password", type="password", key="su_confirm")

        st.markdown("<br>", unsafe_allow_html=True)

        b1, b2 = st.columns(2)

        with b1:
            if st.button("Create Account"):
                if username.strip() == "" or password.strip() == "" or confirm_password.strip() == "":
                    st.error("All fields are required")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    success = add_user(username, password)
                    if success:
                        st.success("Account created ")
                        st.session_state.page = "login"
                        st.rerun()
                    else:
                        st.error("Username already exists")

        with b2:
            if st.button("Back to Login"):
                st.session_state.page = "login"
                st.rerun()

# ---------- ROUTING ----------
if not st.session_state.logged_in:
    if st.session_state.page == "login":
        login()
    else:
        signup()
else:
    # ✅ SAFE REDIRECT AFTER LOGIN
    st.switch_page("pages/patient_input.py")

# ---------- FOOTER ----------
st.markdown('<div class="footer">© PneumoScan AI</div>', unsafe_allow_html=True)