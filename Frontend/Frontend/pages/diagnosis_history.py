import streamlit as st
import mysql.connector
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Diagnosis History | PneumoScan AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DATABASE CONFIGURATION
# =========================================================

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "System"
MYSQL_DATABASE = "pneumonia_project"

# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# =========================================================
# FIND PATIENT NAME COLUMN AUTOMATICALLY
# =========================================================

def get_patient_name_column():

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SHOW COLUMNS FROM patients
        """)

        columns = [row[0] for row in cursor.fetchall()]

        possible_columns = [
            "patient_name",
            "name",
            "full_name",
            "patientName",
            "fullName"
        ]

        for column in possible_columns:

            if column in columns:
                return column

        return None

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

# =========================================================
# GET DIAGNOSIS HISTORY
# =========================================================

def get_diagnosis_history():

    name_column = get_patient_name_column()

    conn = None
    cursor = None

    try:

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if name_column:

            query = f"""
                SELECT
                    dr.patient_id,
                    p.`{name_column}` AS patient_name,
                    dr.created_at,
                    dr.final_diagnosis
                FROM diagnosis_reports dr
                INNER JOIN patients p
                    ON dr.patient_id = p.patient_id
                ORDER BY dr.created_at DESC
            """

        else:

            query = """
                SELECT
                    dr.patient_id,
                    'Patient Name Not Available' AS patient_name,
                    dr.created_at,
                    dr.final_diagnosis
                FROM diagnosis_reports dr
                ORDER BY dr.created_at DESC
            """

        cursor.execute(query)

        return cursor.fetchall()

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()

# =========================================================
# ATTRACTIVE CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN BACKGROUND
       ===================================================== */

    .stApp {

        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(14,165,233,0.16),
                transparent 32%
            ),

            radial-gradient(
                circle at 90% 20%,
                rgba(99,102,241,0.15),
                transparent 30%
            ),

            radial-gradient(
                circle at 50% 100%,
                rgba(20,184,166,0.10),
                transparent 35%
            ),

            linear-gradient(
                135deg,
                #07111f 0%,
                #0f172a 45%,
                #111827 100%
            );

        color: white;

        font-family:
            "Segoe UI",
            sans-serif;
    }


    /* =====================================================
       HIDE STREAMLIT DEFAULT UI
       ===================================================== */

    #MainMenu {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* =====================================================
       MAIN CONTAINER
       ===================================================== */

    .block-container {

        padding-top: 45px !important;

        padding-bottom: 40px !important;

        max-width: 1250px !important;
    }


    /* =====================================================
       PAGE TITLE
       ===================================================== */

    .page-title {

        color: white;

        font-size: 36px;

        font-weight: 800;

        letter-spacing: -0.5px;

        margin-bottom: 8px;

        text-shadow:
            0px 4px 20px rgba(0,0,0,0.35);
    }


    .page-subtitle {

        color: #94a3b8;

        font-size: 15px;

        margin-bottom: 25px;
    }


    /* =====================================================
       BACK HOME BUTTON
       ===================================================== */

    div.stButton > button {

        background:
            linear-gradient(
                135deg,
                #ffffff,
                #e2e8f0
            ) !important;

        color: #1e293b !important;

        border:
            1px solid rgba(255,255,255,0.5) !important;

        border-radius:
            12px !important;

        height:
            45px;

        font-size:
            14px;

        font-weight:
            700;

        transition:
            all 0.25s ease;

        box-shadow:
            0px 5px 18px rgba(0,0,0,0.20);
    }


    div.stButton > button:hover {

        transform:
            translateY(-2px);

        box-shadow:
            0px 8px 25px rgba(14,165,233,0.25);

        border-color:
            #38bdf8 !important;
    }


    /* =====================================================
       GLASS CONTAINERS
       ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.075),
                rgba(255,255,255,0.025)
            ) !important;

        border:
            1px solid rgba(148,163,184,0.18) !important;

        border-radius:
            18px !important;

        box-shadow:
            0px 12px 35px rgba(0,0,0,0.20);

        backdrop-filter:
            blur(12px);

        transition:
            all 0.25s ease;
    }


    div[data-testid="stVerticalBlockBorderWrapper"]:hover {

        border-color:
            rgba(56,189,248,0.30) !important;

        box-shadow:
            0px 15px 40px rgba(0,0,0,0.30);
    }


    /* =====================================================
       SECTION TITLE
       ===================================================== */

    .section-title {

        color: white;

        font-size: 24px;

        font-weight: 800;

        margin-top: 38px;

        margin-bottom: 6px;

        letter-spacing: -0.3px;
    }


    .section-subtitle {

        color: #94a3b8;

        font-size: 14px;

        margin-bottom: 20px;
    }


    /* =====================================================
       INFORMATION BOX
       ===================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] h3 {

        color: white !important;

        font-size: 21px !important;

        font-weight: 800 !important;
    }


    /* =====================================================
       SUMMARY METRICS
       ===================================================== */

    [data-testid="stMetric"] {

        padding:
            18px 20px;

        border-radius:
            16px;

        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.07),
                rgba(255,255,255,0.025)
            );

        border:
            1px solid rgba(148,163,184,0.16);

        min-height:
            125px;

        transition:
            all 0.25s ease;
    }


    [data-testid="stMetric"]:hover {

        transform:
            translateY(-5px);

        border-color:
            rgba(56,189,248,0.45);

        box-shadow:
            0px 12px 30px rgba(0,0,0,0.25);
    }


    /* Metric labels */

    [data-testid="stMetricLabel"] {

        color:
            #cbd5e1 !important;

        font-size:
            14px !important;

        font-weight:
            800 !important;
    }


    /* Metric values */

    [data-testid="stMetricValue"] {

        color:
            white !important;

        font-size:
            32px !important;

        font-weight:
            900 !important;

        margin-top:
            5px;
    }


    /* =====================================================
       PATIENT NAME
       ===================================================== */

    .patient-name {

        color:
            white;

        font-size:
            20px;

        font-weight:
            800;

        margin-bottom:
            8px;
    }


    /* =====================================================
       PATIENT ID
       ===================================================== */

    .patient-id {

        color:
            #cbd5e1;

        font-size:
            14px;

        margin-bottom:
            5px;
    }


    /* =====================================================
       DATE
       ===================================================== */

    .date-text {

        color:
            #94a3b8;

        font-size:
            13px;
    }


    /* =====================================================
       POSITIVE RESULT
       ===================================================== */

    .positive-result {

        display:
            inline-block;

        color:
            #fecaca;

        background:
            rgba(239,68,68,0.13);

        border:
            1px solid rgba(239,68,68,0.25);

        padding:
            10px 18px;

        border-radius:
            12px;

        font-size:
            17px;

        font-weight:
            800;

        margin-top:
            15px;

        margin-bottom:
            14px;

        box-shadow:
            0px 5px 20px rgba(239,68,68,0.08);
    }


    /* =====================================================
       NEGATIVE RESULT
       ===================================================== */

    .negative-result {

        display:
            inline-block;

        color:
            #bbf7d0;

        background:
            rgba(34,197,94,0.12);

        border:
            1px solid rgba(34,197,94,0.25);

        padding:
            10px 18px;

        border-radius:
            12px;

        font-size:
            17px;

        font-weight:
            800;

        margin-top:
            15px;

        margin-bottom:
            14px;

        box-shadow:
            0px 5px 20px rgba(34,197,94,0.08);
    }


    /* =====================================================
       EXPLANATION
       ===================================================== */

    .explanation {

        color:
            #cbd5e1;

        font-size:
            14px;

        line-height:
            1.7;

        padding:
            8px 2px;
    }


    /* =====================================================
       ALERT BOXES
       ===================================================== */

    div[data-testid="stAlert"] {

        border-radius:
            12px !important;

        border:
            1px solid rgba(255,255,255,0.12) !important;

        backdrop-filter:
            blur(8px);
    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .custom-footer {

        text-align:
            center;

        color:
            #64748b;

        font-size:
            12px;

        margin-top:
            50px;

        padding:
            25px;

        line-height:
            1.8;

        border-top:
            1px solid rgba(148,163,184,0.10);
    }


    .custom-footer b {

        color:
            #94a3b8;
    }


    /* =====================================================
       SCROLLBAR
       ===================================================== */

    ::-webkit-scrollbar {

        width:
            8px;
    }


    ::-webkit-scrollbar-track {

        background:
            #0f172a;
    }


    ::-webkit-scrollbar-thumb {

        background:
            #334155;

        border-radius:
            10px;
    }


    ::-webkit-scrollbar-thumb:hover {

        background:
            #475569;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LOAD HISTORY
# =========================================================

try:

    history = get_diagnosis_history()

except mysql.connector.Error as e:

    st.error(
        "❌ Unable to connect to the database."
    )

    with st.expander("Technical details"):
        st.code(str(e))

    st.stop()

except Exception as e:

    st.error(
        "❌ Unable to load diagnosis history."
    )

    with st.expander("Technical details"):
        st.code(str(e))

    st.stop()

# =========================================================
# HEADER
# =========================================================

col1, col2 = st.columns([5, 1])

with col1:

    st.markdown(
        """
        <div class="page-title">
            🩺 My Diagnosis History
        </div>

        <div class="page-subtitle">
            View your previous pneumonia screening results
            in a simple and easy-to-understand format.
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    if st.button(
        "⬅ Back to Home",
        use_container_width=True
    ):

        st.switch_page("app.py")

# =========================================================
# INFORMATION BOX
# =========================================================

with st.container(border=True):

    st.markdown(
        "### ℹ️ What does my diagnosis mean?"
    )

    st.write(
        "Your result is generated by the AI-assisted "
        "pneumonia screening system."
    )

    col1, col2 = st.columns(2)

    with col1:

        st.error(
            "🔴 Pneumonia Detected"
        )

        st.write(
            "The screening found signs that may be "
            "associated with pneumonia. Please consult "
            "a qualified doctor for confirmation."
        )

    with col2:

        st.success(
            "🟢 No Pneumonia Detected"
        )

        st.write(
            "The screening did not find signs strongly "
            "suggesting pneumonia during this test."
        )

    st.caption(
        "Important: This is an AI-assisted screening result "
        "and does not replace a doctor's medical diagnosis."
    )

# =========================================================
# CALCULATE SUMMARY
# =========================================================

total_tests = len(history)

pneumonia_tests = 0

normal_tests = 0

for row in history:

    diagnosis = str(
        row.get(
            "final_diagnosis",
            ""
        )
    ).strip().lower()

    # Check NO PNEUMONIA first

    if (
        "no pneumonia" in diagnosis
        or "normal" in diagnosis
        or "negative" in diagnosis
    ):

        normal_tests += 1

    elif "pneumonia" in diagnosis:

        pneumonia_tests += 1

    else:

        normal_tests += 1

# =========================================================
# SUMMARY
# =========================================================

st.markdown(
    """
    <div class="section-title">
         My Screening Summary
    </div>

    <div class="section-subtitle">
        A quick overview of your previous screening tests.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:

    with st.container(border=True):

        st.metric(
            "Total Tests",
            total_tests
        )

        st.caption(
            "Total screenings completed"
        )

with col2:

    with st.container(border=True):

        st.metric(
            "Pneumonia Detected",
            pneumonia_tests
        )

        st.caption(
            "Screenings with possible pneumonia signs"
        )

with col3:

    with st.container(border=True):

        st.metric(
            "No Pneumonia Detected",
            normal_tests
        )

        st.caption(
            "Screenings without strong pneumonia signs"
        )

# =========================================================
# PREVIOUS RESULTS
# =========================================================

st.markdown(
    """
    <div class="section-title">
         Previous Diagnosis Results
    </div>

    <div class="section-subtitle">
        Your latest screening result is shown first.
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# NO HISTORY
# =========================================================

if not history:

    st.info(
        "No diagnosis history is available yet. "
        "Complete a diagnosis to see your results here."
    )

# =========================================================
# DISPLAY HISTORY
# =========================================================

else:

    for row in history:

        # -------------------------------------------------
        # PATIENT NAME
        # -------------------------------------------------

        patient_name = str(
            row.get(
                "patient_name",
                "Patient Name Not Available"
            )
        )

        if not patient_name.strip():

            patient_name = "Patient Name Not Available"

        # -------------------------------------------------
        # PATIENT ID
        # -------------------------------------------------

        patient_id = str(
            row.get(
                "patient_id",
                "Not Available"
            )
        )

        # -------------------------------------------------
        # DIAGNOSIS
        # -------------------------------------------------

        diagnosis = str(
            row.get(
                "final_diagnosis",
                ""
            )
        ).strip().lower()

        # -------------------------------------------------
        # DETERMINE RESULT
        # -------------------------------------------------

        if (
            "no pneumonia" in diagnosis
            or "normal" in diagnosis
            or "negative" in diagnosis
        ):

            is_pneumonia = False

        elif "pneumonia" in diagnosis:

            is_pneumonia = True

        else:

            is_pneumonia = False

        # -------------------------------------------------
        # FORMAT DATE
        # -------------------------------------------------

        try:

            date_value = pd.to_datetime(
                row["created_at"]
            )

            formatted_date = date_value.strftime(
                "%d %B %Y, %I:%M %p"
            )

        except Exception:

            formatted_date = str(
                row["created_at"]
            )

        # -------------------------------------------------
        # PATIENT RESULT CARD
        # -------------------------------------------------

        with st.container(border=True):

            # Patient Name

            st.markdown(
                f"""
                <div class="patient-name">
                    👤 {patient_name}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Patient ID

            st.markdown(
                f"""
                <div class="patient-id">
                     Patient ID: {patient_id}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Test Date

            st.markdown(
                f"""
                <div class="date-text">
                     Test Date: {formatted_date}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            # -------------------------------------------------
            # PNEUMONIA
            # -------------------------------------------------

            if is_pneumonia:

                st.markdown(
                    """
                    <div class="positive-result">
                        🔴 Pneumonia Detected
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div class="explanation">

                    <b>What does this mean?</b><br>

                    The screening found signs that may be
                    associated with pneumonia.

                    <br><br>

                    <b>What should I do?</b><br>

                    Please consult a qualified doctor for
                    proper medical evaluation and confirmation.

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.warning(
                    "This is an AI screening result and should "
                    "not be used as a final medical diagnosis."
                )

            # -------------------------------------------------
            # NO PNEUMONIA
            # -------------------------------------------------

            else:

                st.markdown(
                    """
                    <div class="negative-result">
                        🟢 No Pneumonia Detected
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div class="explanation">

                    <b>What does this mean?</b><br>

                    The screening did not find signs strongly
                    suggesting pneumonia during this test.

                    <br><br>

                    <b>Important:</b><br>

                    If you have symptoms or feel unwell,
                    please consult a doctor even if the
                    screening result is normal.

                    </div>
                    """,
                    unsafe_allow_html=True
                )

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="custom-footer">

        🩺 <b>PneumoScan AI</b><br>

        AI-Assisted Pneumonia Screening System<br><br>

        This system is intended for screening assistance only.
        Please consult a qualified healthcare professional
        for medical advice and diagnosis.

    </div>
    """,
    unsafe_allow_html=True
)