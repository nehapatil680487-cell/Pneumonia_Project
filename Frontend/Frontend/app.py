import streamlit as st
import base64
import mysql.connector


# ---------- PAGE CONFIG ----------

st.set_page_config(
    page_title="PneumoScan AI",
    page_icon="🏥",
    layout="wide"
)



# ---------- LOAD IMAGE AS BASE64 ----------

def get_base64(file_path):

    with open(file_path, "rb") as f:

        return base64.b64encode(
            f.read()
        ).decode()


img_base64 = get_base64(
    "images/final.jpeg"
)


# ---------- SYSTEM PROGRESS CONFIG ----------
#
# MODEL_ACCURACY_PERCENT -> the real accuracy of your trained model
# from your validation/test evaluation (not the live per-prediction
# "confidence" score, which is a different number). Update this
# whenever you retrain/re-evaluate.
#
# USAGE_TARGET_PATIENTS -> the "goal" number of patients you are
# tracking usage against (e.g. a pilot target, monthly goal, or
# system capacity). The usage ring fills up as your real patient
# count approaches this target.

MODEL_ACCURACY_PERCENT = 97.5      # TODO: set to your real evaluated accuracy
USAGE_TARGET_PATIENTS = 50         # TODO: set your target/capacity number

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "System"
MYSQL_DATABASE = "pneumonia_project"


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )


def get_stats():
    """Lightweight aggregate query -- just the counts we need."""

    conn = None
    cursor = None

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                COUNT(DISTINCT p.patient_id) AS total_patients,
                COUNT(*) AS total_reports,
                SUM(
                    CASE WHEN LOWER(dr.final_diagnosis) LIKE '%pneumonia%'
                    THEN 1 ELSE 0 END
                ) AS pneumonia_count
            FROM diagnosis_reports dr
            INNER JOIN patients p
                ON dr.patient_id = p.patient_id
        """)
        row = cursor.fetchone() or {}
        # MySQL's SUM()/COUNT() can come back as Decimal instead of a
        # plain int, which breaks float math later (e.g. building the
        # ring animations). Cast everything to int right here.
        total_patients = int(row.get("total_patients") or 0)
        total_reports = int(row.get("total_reports") or 0)
        pneumonia_count = int(row.get("pneumonia_count") or 0)
        normal_count = total_reports - pneumonia_count
        return total_patients, total_reports, pneumonia_count, normal_count

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# Stats are optional decoration on the landing page -- if the DB
# isn't reachable yet, don't break the whole homepage over it.
try:
    total_patients, total_reports, pneumonia_count, normal_count = get_stats()
    stats_available = True
except Exception:
    total_patients = total_reports = pneumonia_count = normal_count = 0
    stats_available = False



# ---------- STYLING ----------

st.markdown(f"""

<style>

/* Remove padding */

.block-container {{
    padding:0;
}}


/* Background */

.stApp {{

    background:
    url("data:image/png;base64,{img_base64}")
    no-repeat center center fixed;

    background-size:cover;

}}



/* Dark Overlay */

.stApp::before {{

    content:"";

    position:fixed;

    top:0;

    left:0;

    right:0;

    bottom:0;

    background:rgba(0,0,0,0.6);

    z-index:0;

}}



/* Main Content */

.main-content {{

    position:relative;

    z-index:1;

    padding-top:200px;

    max-width:900px;

    margin:auto;

    text-align:left;

    padding-left:60px;

}}



/* Title */

.title {{

    font-size:60px;

    font-weight:700;

    color:white;

    margin-bottom:20px;

}}



/* Subtitle */

.subtitle {{

    font-size:22px;

    color:#ddd;

    margin-bottom:40px;

}}




/* Next Button */

div.stButton > button {{

    background:#007BFF !important;

    color:white !important;

    border-radius:8px;

    height:42px;

    width:170px;

    font-size:15px;

    font-weight:bold;

    border:none;

}}



div.stButton > button:hover {{

    background:#0056b3 !important;

}}





/* Doctor Icon */

.doctor-icon {{

    position:fixed;

    bottom:30px;

    right:40px;

    width:65px;

    height:65px;

    background:white;

    border-radius:50%;

    display:flex;

    align-items:center;

    justify-content:center;

    font-size:35px;

    box-shadow:
    0px 5px 15px rgba(0,0,0,0.5);

    z-index:10;

    cursor:pointer;

}}



.doctor-icon:hover {{

    transform:scale(1.1);

}}


/* Progress Section */

.progress-section {{

    position:relative;

    z-index:1;

    max-width:1000px;

    margin:70px auto 90px auto;

    padding:0 40px;

}}


.progress-section-title {{

    text-align:center;

    color:white;

    font-size:28px;

    font-weight:800;

    margin-bottom:8px;

}}


.progress-section-sub {{

    text-align:center;

    color:#cbd5e1;

    font-size:14px;

    margin-bottom:35px;

}}


.progress-card {{

    background:rgba(255,255,255,0.08);

    border:1px solid rgba(255,255,255,0.18);

    border-radius:20px;

    padding:26px 18px 22px 18px;

    text-align:center;

    backdrop-filter:blur(6px);

    height:100%;

}}


.clickable-card {{

    cursor:pointer;

    transition:transform 0.25s ease, border-color 0.25s ease;

}}


.clickable-card:hover {{

    transform:translateY(-6px);

    border-color:rgba(14,165,233,0.6);

}}


.click-hint {{

    font-size:11.5px;

    color:#38bdf8;

    font-weight:700;

    margin-top:12px;

    opacity:0;

    transition:opacity 0.25s ease;

}}


.clickable-card:hover .click-hint {{

    opacity:1;

}}


.progress-ring-wrap {{

    position:relative;

    width:150px;

    height:150px;

    margin:0 auto;

}}


.progress-ring-wrap svg {{

    width:150px;

    height:150px;

    display:block;

}}


.progress-ring-center {{

    position:absolute;

    top:0;

    left:0;

    right:0;

    bottom:0;

    display:flex;

    flex-direction:column;

    align-items:center;

    justify-content:center;

}}


.progress-value {{

    font-size:30px;

    font-weight:800;

    color:white;

    line-height:1.1;

}}


.progress-sub {{

    font-size:14px;

    color:#cbd5e1;

    margin-top:5px;

    font-weight:600;

}}


.progress-title {{

    font-size:15px;

    font-weight:800;

    color:white;

    margin-top:18px;

}}


.progress-desc {{

    font-size:12px;

    color:#cbd5e1;

    margin-top:5px;

    line-height:1.5;

}}


.legend-row {{

    display:flex;

    justify-content:center;

    gap:14px;

    margin-top:12px;

    font-size:11.5px;

    color:#e2e8f0;

}}


.legend-dot {{

    display:inline-block;

    width:9px;

    height:9px;

    border-radius:50%;

    margin-right:5px;

    vertical-align:middle;

}}


</style>

""", unsafe_allow_html=True)




# ---------- HERO SECTION ----------


st.markdown(
    '<div class="main-content">',
    unsafe_allow_html=True
)



st.markdown(
    '<div class="title">'
    'AI-Powered Pneumonia Detection'
    '</div>',
    unsafe_allow_html=True
)



st.markdown(
    '<div class="subtitle">'
    'Transforming Medical Diagnosis with Artificial Intelligence'
    '</div>',
    unsafe_allow_html=True
)



# ---------- NEXT BUTTON ----------

if st.button("Next"):

    st.switch_page(
        "pages/landing.py"
    )



st.markdown(
    '</div>',
    unsafe_allow_html=True
)



# ---------- SYSTEM PROGRESS SECTION ----------
# Sits below the Next button, above the doctor icon, centered.
# Rings are animated SVG strokes (fill in on load), LeetCode
# acceptance-rate style, instead of static CSS backgrounds.

RING_RADIUS = 54
RING_CIRCUMFERENCE = 2 * 3.14159265 * RING_RADIUS


def single_ring_svg(percent, color, value_text, sub_text, anim_name):

    percent = float(percent)
    percent = max(0, min(100, percent))
    offset = RING_CIRCUMFERENCE * (1 - percent / 100)

    return f"""
    <div class="progress-ring-wrap">
        <svg viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="{RING_RADIUS}" fill="none"
                stroke="rgba(255,255,255,0.15)" stroke-width="10"/>
            <circle cx="60" cy="60" r="{RING_RADIUS}" fill="none"
                stroke="{color}" stroke-width="10" stroke-linecap="round"
                stroke-dasharray="{RING_CIRCUMFERENCE:.2f}"
                stroke-dashoffset="{RING_CIRCUMFERENCE:.2f}"
                transform="rotate(-90 60 60)"
                style="animation:{anim_name} 1.6s ease-out forwards;"/>
        </svg>
        <div class="progress-ring-center">
            <div class="progress-value">{value_text}</div>
            <div class="progress-sub">{sub_text}</div>
        </div>
    </div>
    <style>
    @keyframes {anim_name} {{
        from {{ stroke-dashoffset: {RING_CIRCUMFERENCE:.2f}; }}
        to {{ stroke-dashoffset: {offset:.2f}; }}
    }}
    </style>
    """


def dual_ring_svg(percent_a, color_a, color_b, value_text, sub_text,
                   anim_name_a, anim_name_b):

    percent_a = float(percent_a)
    percent_a = max(0, min(100, percent_a))
    percent_b = max(0, 100 - percent_a)

    len_a = RING_CIRCUMFERENCE * percent_a / 100
    len_b = RING_CIRCUMFERENCE * percent_b / 100

    return f"""
    <div class="progress-ring-wrap">
        <svg viewBox="0 0 120 120">
            <circle cx="60" cy="60" r="{RING_RADIUS}" fill="none"
                stroke="rgba(255,255,255,0.15)" stroke-width="10"/>
            <circle cx="60" cy="60" r="{RING_RADIUS}" fill="none"
                stroke="{color_a}" stroke-width="10"
                stroke-dashoffset="0"
                transform="rotate(-90 60 60)"
                style="animation:{anim_name_a} 1.6s ease-out forwards;"/>
            <circle cx="60" cy="60" r="{RING_RADIUS}" fill="none"
                stroke="{color_b}" stroke-width="10"
                stroke-dashoffset="{-len_a:.2f}"
                transform="rotate(-90 60 60)"
                style="animation:{anim_name_b} 1.6s ease-out forwards;"/>
        </svg>
        <div class="progress-ring-center">
            <div class="progress-value">{value_text}</div>
            <div class="progress-sub">{sub_text}</div>
        </div>
    </div>
    <style>
    @keyframes {anim_name_a} {{
        from {{ stroke-dasharray: 0 {RING_CIRCUMFERENCE:.2f}; }}
        to {{ stroke-dasharray: {len_a:.2f} {RING_CIRCUMFERENCE - len_a:.2f}; }}
    }}
    @keyframes {anim_name_b} {{
        from {{ stroke-dasharray: 0 {RING_CIRCUMFERENCE:.2f}; }}
        to {{ stroke-dasharray: {len_b:.2f} {RING_CIRCUMFERENCE - len_b:.2f}; }}
    }}
    </style>
    """


if stats_available:

    accuracy_ring = single_ring_svg(
        percent=MODEL_ACCURACY_PERCENT,
        color="#0ea5e9",
        value_text=f"{MODEL_ACCURACY_PERCENT:.1f}%",
        sub_text="Accuracy",
        anim_name="fillAccuracyRing"
    )

    if total_reports > 0:
        pneumonia_pct = (pneumonia_count / total_reports) * 100
    else:
        pneumonia_pct = 0

    normal_pct = 100 - pneumonia_pct

    diagnosis_ring = dual_ring_svg(
        percent_a=pneumonia_pct,
        color_a="#ef4444",
        color_b="#22c55e",
        value_text=str(total_reports),
        sub_text="Total Cases",
        anim_name_a="fillPneumoniaArc",
        anim_name_b="fillNormalArc"
    )

    if USAGE_TARGET_PATIENTS > 0:
        usage_pct = (total_patients / USAGE_TARGET_PATIENTS) * 100
    else:
        usage_pct = 0

    usage_ring = single_ring_svg(
        percent=usage_pct,
        color="#14b8a6",
        value_text=str(total_patients),
        sub_text=f"of {USAGE_TARGET_PATIENTS} target",
        anim_name="fillUsageRing"
    )

    st.markdown(
        '<div class="progress-section">'
        '<div class="progress-section-title">Our System at a Glance</div>'
        '<div class="progress-section-sub">'
        'Live numbers from real diagnosis activity</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown(
            '<a href="/model_insights" target="_self" style="text-decoration:none;">'
            '<div class="progress-card clickable-card">'
            f'{accuracy_ring}'
            '<div class="progress-title"> Model Accuracy</div>'
            '<div class="progress-desc">How reliably the AI model '
            'classifies chest X-rays correctly.</div>'
            '<div class="click-hint">Tap to view full model insights →</div>'
            '</div>'
            '</a>',
            unsafe_allow_html=True
        )

        with col2:
          st.markdown(
            '<a href="/diagnosis_history" target="_self" style="text-decoration:none;">'
            '<div class="progress-card clickable-card">'
            f'{diagnosis_ring}'
            '<div class="progress-title"> Diagnosis Split</div>'
            '<div class="progress-desc">Pneumonia vs Normal cases out of '
            'all reports generated.</div>'
            '<div class="legend-row">'
            '<span><span class="legend-dot" style="background:#ef4444;"></span>'
            f'Pneumonia: {pneumonia_count} ({pneumonia_pct:.1f}%)</span>'
            '<span><span class="legend-dot" style="background:#22c55e;"></span>'
            f'Normal: {normal_count} ({normal_pct:.1f}%)</span>'
            '</div>'
            '<div class="click-hint">Tap to view diagnosis history →</div>'
            '</div>'
            '</a>',
            unsafe_allow_html=True
        )

    with col3:
        about_ai_ring = single_ring_svg(
            percent=100,
            color="#14b8a6",
            value_text="AI",
            sub_text="Overview",
            anim_name="fillAboutAIRing"
        )

        st.markdown(
            '<a href="/about_ai" target="_self" style="text-decoration:none;">'
            '<div class="progress-card clickable-card">'
            f'{about_ai_ring}'
            '<div class="progress-title"> How PneumoScan AI Works</div>'
            '<div class="progress-desc">'
            'Learn how our AI system uses X-rays, blood counts, '
            'oxygen and CRP for pneumonia screening.'
            '</div>'
            '<div class="click-hint">'
            'Tap to learn how the AI works →'
            '</div>'
            '</div>'
            '</a>',
            unsafe_allow_html=True
        )
        
    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

else:

    # DB not reachable -- skip the section quietly so the
    # landing page still loads normally for visitors.
    pass



# ---------- CLICKABLE DOCTOR ICON ----------

st.markdown("""

<a href="/doctor_login" target="_self">

<div class="doctor-icon">

🩺

</div>

</a>

""", unsafe_allow_html=True)