import streamlit as st
import mysql.connector
import requests
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Model Insights | PneumoScan AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CONFIGURATION
#
# Keep MODEL_ACCURACY_PERCENT and MODEL_VERSION in sync with the
# ring shown on your homepage (app.py). This isn't stored in the
# database because it comes from your offline model evaluation,
# not from live predictions. Update it whenever you retrain.
#
# REVIEW_CONFIDENCE_THRESHOLD controls the "Cases to Review"
# list below -- any report with confidence under this value is
# flagged as worth a second look.
# =========================================================

MODEL_ACCURACY_PERCENT = 97.5      # TODO: set to your real evaluated accuracy
MODEL_VERSION = "v1.0"             # TODO: set your actual model version/date
REVIEW_CONFIDENCE_THRESHOLD = 90.0

FASTAPI_BASE_URL = "http://127.0.0.1:8000"

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "System"
MYSQL_DATABASE = "pneumonia_project"


# =========================================================
# MYSQL CONNECTION
# =========================================================

def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )


# =========================================================
# GET CONFIDENCE DATA
# (all reports with the fields we need for this page only)
# =========================================================

def get_confidence_data():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                dr.report_id,
                dr.report_code,
                dr.confidence,
                dr.final_diagnosis,
                dr.created_at,
                p.patient_id,
                p.full_name
            FROM diagnosis_reports dr
            INNER JOIN patients p
                ON dr.patient_id = p.patient_id
            ORDER BY dr.confidence ASC
        """)
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# =========================================================
# CSS (matches the doctor-portal dark theme used across
# docter_dashboard.py / patient_search.py)
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(14,165,233,0.14), transparent 35%),
        radial-gradient(circle at 90% 90%, rgba(34,197,94,0.10), transparent 35%),
        linear-gradient(135deg, #0f172a, #1e293b);
    font-family: "Segoe UI", Arial, sans-serif;
}

#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }

div.stButton > button {
    border-radius: 10px !important;
    border: none !important;
    font-weight: 700 !important;
    min-height: 42px !important;
}

.stat-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 18px;
    padding: 20px;
    min-height: 100px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}

.stat-title {
    color: #cbd5e1;
    font-size: 13px;
}

.stat-number {
    color: white;
    font-size: 28px;
    font-weight: 800;
    margin-top: 6px;
}

.big-ring-wrap {
    position: relative;
    width: 220px;
    height: 220px;
    margin: 10px auto 0 auto;
}

.big-ring-wrap svg {
    width: 220px;
    height: 220px;
    display: block;
}

.big-ring-center {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.big-ring-value {
    font-size: 42px;
    font-weight: 800;
    color: white;
}

.big-ring-sub {
    font-size: 13px;
    color: #94a3b8;
    margin-top: 4px;
}

.dist-row {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}

.dist-label {
    width: 90px;
    color: #cbd5e1;
    font-size: 13px;
    text-align: right;
}

.dist-track {
    flex: 1;
    background: rgba(255,255,255,0.08);
    border-radius: 8px;
    height: 18px;
    overflow: hidden;
}

.dist-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 1s ease-out;
}

.dist-count {
    width: 40px;
    color: white;
    font-size: 13px;
    font-weight: 700;
}

.review-card {
    background: white;
    border-radius: 14px;
    padding: 16px 20px;
    margin-top: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
    border: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.review-name {
    color: #0f172a;
    font-weight: 700;
    font-size: 15px;
}

.review-sub {
    color: #64748b;
    font-size: 12.5px;
    margin-top: 3px;
}

.confidence-pill {
    background: #fef3c7;
    color: #92400e;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 13px;
    white-space: nowrap;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

try:
    records = get_confidence_data()
except mysql.connector.Error as e:
    st.error("❌ Unable to connect to MySQL database.")
    st.code(str(e))
    st.stop()
except Exception as e:
    st.error("❌ An unexpected error occurred.")
    st.code(str(e))
    st.stop()


# =========================================================
# HEADER
# =========================================================

head_col1, head_col2 = st.columns([5, 1])

with head_col1:
    st.markdown(
        '<div style="color:white;font-size:28px;font-weight:800;">'
        ' Model Insights</div>'
        '<div style="color:#94a3b8;font-size:13px;margin-top:5px;">'
        f'Model version {html.escape(MODEL_VERSION)} • Accuracy and '
        'live prediction confidence stats.</div>',
        unsafe_allow_html=True
    )

with head_col2:
    if st.button("⬅ Back to Home", use_container_width=True):
        st.switch_page("app.py")

st.markdown(
    '<hr style="border:none;height:1px;background:#334155;margin:20px 0 35px 0;">',
    unsafe_allow_html=True
)


# =========================================================
# COMPUTE STATS
# =========================================================

confidences = []

for r in records:
    try:
        confidences.append(float(r.get("confidence") or 0))
    except (TypeError, ValueError):
        pass

total_predictions = len(confidences)

if total_predictions > 0:
    avg_confidence = sum(confidences) / total_predictions
    max_confidence = max(confidences)
    min_confidence = min(confidences)
else:
    avg_confidence = max_confidence = min_confidence = 0.0


# =========================================================
# BIG ACCURACY RING (animated, same style as homepage)
# =========================================================

RING_RADIUS = 90
RING_CIRCUMFERENCE = 2 * 3.14159265 * RING_RADIUS

accuracy_percent = max(0.0, min(100.0, float(MODEL_ACCURACY_PERCENT)))
ring_offset = RING_CIRCUMFERENCE * (1 - accuracy_percent / 100)

big_ring_html = f"""
<div class="big-ring-wrap">
    <svg viewBox="0 0 200 200">
        <circle cx="100" cy="100" r="{RING_RADIUS}" fill="none"
            stroke="rgba(255,255,255,0.12)" stroke-width="14"/>
        <circle cx="100" cy="100" r="{RING_RADIUS}" fill="none"
            stroke="#0ea5e9" stroke-width="14" stroke-linecap="round"
            stroke-dasharray="{RING_CIRCUMFERENCE:.2f}"
            stroke-dashoffset="{RING_CIRCUMFERENCE:.2f}"
            transform="rotate(-90 100 100)"
            style="animation:fillModelAccuracyRing 1.8s ease-out forwards;"/>
    </svg>
    <div class="big-ring-center">
        <div class="big-ring-value">{accuracy_percent:.1f}%</div>
        <div class="big-ring-sub">Evaluated Accuracy</div>
    </div>
</div>
<style>
@keyframes fillModelAccuracyRing {{
    from {{ stroke-dashoffset: {RING_CIRCUMFERENCE:.2f}; }}
    to {{ stroke-dashoffset: {ring_offset:.2f}; }}
}}
</style>
"""

st.markdown(big_ring_html, unsafe_allow_html=True)


# =========================================================
# STAT CARDS
# =========================================================

st.markdown('<div style="height:30px;"></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-title">Total Predictions</div>'
        f'<div class="stat-number">{total_predictions}</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-title">Average Confidence</div>'
        f'<div class="stat-number">{avg_confidence:.1f}%</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-title">Highest Confidence</div>'
        f'<div class="stat-number">{max_confidence:.1f}%</div>'
        '</div>',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        '<div class="stat-card">'
        '<div class="stat-title">Lowest Confidence</div>'
        f'<div class="stat-number">{min_confidence:.1f}%</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# CONFIDENCE DISTRIBUTION
# =========================================================

st.markdown(
    '<div style="color:white;font-size:20px;font-weight:700;'
    'margin-top:40px;margin-bottom:15px;">Confidence Distribution</div>',
    unsafe_allow_html=True
)

buckets = [
    ("Above 90%", lambda c: c >= 90, "#22c55e"),
    ("Below 90%", lambda c: c < 90, "#84cc16"),
    ("Less than 80%", lambda c: c < 80, "#f59e0b"),
    ("Less than 70%", lambda c: c < 70, "#ef4444"),
]

max_bucket_count = 1

bucket_counts = []

for label, condition, color in buckets:
    count = sum(1 for c in confidences if condition(c))
    bucket_counts.append((label, count, color))
    max_bucket_count = max(max_bucket_count, count)

for label, count, color in bucket_counts:
    width_pct = (count / max_bucket_count) * 100 if max_bucket_count > 0 else 0
    st.markdown(
        '<div class="dist-row">'
        f'<div class="dist-label">{label}</div>'
        '<div class="dist-track">'
        f'<div class="dist-fill" style="width:{width_pct:.1f}%;background:{color};"></div>'
        '</div>'
        f'<div class="dist-count">{count}</div>'
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# CASES TO REVIEW (lowest-confidence predictions)
# =========================================================

st.markdown(
    '<div style="color:white;font-size:20px;font-weight:700;'
    'margin-top:40px;margin-bottom:6px;"> Cases to Review</div>'
    '<div style="color:#94a3b8;font-size:13px;margin-bottom:15px;">'
    f'Predictions below {REVIEW_CONFIDENCE_THRESHOLD:.0f}% confidence -- '
    'worth a second look.</div>',
    unsafe_allow_html=True
)

review_records = [
    r for r in records
    if float(r.get("confidence") or 0) < REVIEW_CONFIDENCE_THRESHOLD
]

if not review_records:

    st.info(
        f" No predictions below {REVIEW_CONFIDENCE_THRESHOLD:.0f}% "
        "confidence right now."
    )

else:

    for r in review_records:

        name_safe = html.escape(str(r.get("full_name", "N/A")))
        diagnosis = str(r.get("final_diagnosis", "N/A"))
        diagnosis_safe = html.escape(diagnosis)
        report_id = r.get("report_id", "N/A")
        report_code = r.get("report_code", "")
        patient_id = r.get("patient_id", "N/A")

        try:
            confidence_val = float(r.get("confidence") or 0)
            confidence_display = f"{confidence_val:.1f}%"
        except (TypeError, ValueError):
            confidence_display = html.escape(str(r.get("confidence", "N/A")))

        st.markdown(
            '<div class="review-card">'
            '<div>'
            f'<div class="review-name">👤 {name_safe}</div>'
            f'<div class="review-sub">Patient ID: {patient_id} &nbsp;|&nbsp; '
            f'Report ID: {report_id} &nbsp;|&nbsp; Diagnosis: {diagnosis_safe}</div>'
            '</div>'
            f'<div class="confidence-pill"> {confidence_display}</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if report_code:
            pdf_url = f"{FASTAPI_BASE_URL}/download/{report_code}"
            st.markdown(
                f'<a href="{pdf_url}" target="_blank" '
                'style="display:inline-block;margin:6px 0 4px 0;padding:8px 16px;'
                'background:#0ea5e9;color:white;border-radius:8px;'
                'text-decoration:none;font-weight:700;font-size:13px;">'
                ' View PDF</a>',
                unsafe_allow_html=True
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div style="text-align:center;color:#64748b;font-size:12px;'
    'padding:35px 0 15px 0;line-height:1.7;">'
    'PneumoScan AI • AI-Assisted Pneumonia Screening System<br>'
    'Public Model Insights</div>',
    unsafe_allow_html=True
)