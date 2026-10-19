import streamlit as st
import webbrowser
from urllib.parse import urlencode


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Patient Information",
    page_icon="",
    layout="centered"
)


# ---------------- FAST API URL ----------------
FASTAPI_URL = "http://127.0.0.1:8000/"


# ---------------- CSS ----------------
st.markdown("""
<style>

/* Background */
.stApp{
    background: linear-gradient(135deg,#1f4037,#99f2c8);
    font-family:'Segoe UI',sans-serif;
}


/* Hide Streamlit */
#MainMenu{
    visibility:hidden;
}

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}


/* Title */
.title{
    text-align:center;
    color:white;
    font-size:42px;
    font-weight:700;
    margin-top:20px;
}


.subtitle{
    text-align:center;
    color:white;
    font-size:22px;
    margin-bottom:30px;
}


/* Labels */
label{
    color:white !important;
    font-weight:600 !important;
}


/* Inputs */
.stTextInput input,
.stNumberInput input{

    background:white !important;

    color:black !important;

    border-radius:10px !important;

    height:45px;

    border:none !important;

}


/* Select box */
div[data-baseweb="select"]{

    border-radius:10px;

}



/* Button */
div.stButton > button{

    background:#007BFF !important;

    color:white !important;

    width:100%;

    height:50px;

    border-radius:12px;

    font-size:18px;

    font-weight:bold;

    border:none;

    transition:0.3s;

}


div.stButton > button:hover{

    background:#0056b3 !important;

    transform:scale(1.02);

    box-shadow:0px 5px 15px rgba(0,0,0,0.3);

}


/* Messages */
div[data-testid="stAlert"]{

    border-radius:10px;

}


/* Footer */
.footer{

    text-align:center;

    color:white;

    margin-top:40px;

    font-size:14px;

}


.footer a{

    color:white;

    text-decoration:none;

    font-weight:bold;

}


.footer a:hover{

    text-decoration:underline;

}


</style>

""", unsafe_allow_html=True)



# ---------------- TITLE ----------------

st.markdown("""
<div class="title">
 PneumoScan AI
</div>

<div class="subtitle">
Patient Information
</div>

""", unsafe_allow_html=True)



# ---------------- PATIENT DETAILS ----------------


st.markdown("### 👤 Enter Patient Details")


col1,col2 = st.columns(2)


with col1:

    name = st.text_input(
        "Full Name"
    )


with col2:

    age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=25
    )



col3,col4 = st.columns(2)


with col3:

    gender = st.selectbox(
        "Gender",
        [
            "Male",
            "Female",
            "Other"
        ]
    )


with col4:

    mobile = st.text_input(
        "Mobile Number"
    )



st.write("")



# ---------------- START DIAGNOSIS ----------------


if st.button("🩺 Start Diagnosis"):


    if name.strip()=="":


        st.error(
            "⚠️ Please enter patient name"
        )


    elif not mobile.isdigit() or len(mobile)!=10:


        st.error(
            "⚠️ Enter valid 10 digit mobile number"
        )


    else:

        # Store Patient Data
        st.session_state.name = name
        st.session_state.age = age
        st.session_state.gender = gender
        st.session_state.mobile = mobile

        # Build the FastAPI URL WITH the patient details attached,
        # so the diagnosis page opens with these fields already filled in.
        query = urlencode({
            "patient_name": name,
            "age": age,
            "gender": gender,
        })
        diagnosis_url = f"{FASTAPI_URL}?{query}"

        # Open FastAPI Diagnosis Page
        try:

            webbrowser.open(diagnosis_url)

            st.success(
                "✅ Patient information saved"
            )

            st.info(
                "Opening FastAPI Diagnosis System..."
            )

        except Exception as e:

            st.error(
                f"❌ Unable to open FastAPI\n\n{e}"
            )


# ---------------- FOOTER ----------------


st.markdown("""

<div class="footer">

Powered by <b>PneumoScan AI</b><br>

AI-Assisted Pneumonia Screening System<br><br>



</div>

""", unsafe_allow_html=True)