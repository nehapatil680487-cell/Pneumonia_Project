import streamlit as st
import mysql.connector
import requests
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Patient Lookup | PneumoScan AI",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# LOGIN CHECK
# =========================================================

if "doctor_login" not in st.session_state:
    st.session_state.doctor_login = False

if not st.session_state.doctor_login:

    st.warning(" Please login as doctor first.")

    if st.button(" Go to Doctor Login"):
        st.switch_page("pages/doctor_login.py")

    st.stop()


# =========================================================
# CONFIGURATION
# =========================================================

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
# GET ALL REPORTS (same query shape as the main dashboard,
# so patient_id / report_id / etc. line up between pages)
# =========================================================

def get_reports():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                dr.report_id,
                dr.report_code,
                p.patient_id,
                p.full_name,
                p.age,
                p.gender,
                p.phone,
                dr.final_diagnosis,
                dr.confidence,
                dr.image_name,
                dr.pdf_path,
                dr.created_at
            FROM diagnosis_reports dr
            INNER JOIN patients p
                ON dr.patient_id = p.patient_id
            ORDER BY dr.created_at DESC
        """)
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()


# =========================================================
# CSS (shared look with the main dashboard)
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

.stTextInput input {
    background: white !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
    height: 44px !important;
}

.patient-card {
    background: white;
    border-radius: 18px;
    padding: 24px;
    margin-top: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
    border: 1px solid #e2e8f0;
}

.patient-name {
    color: #0f172a;
    font-size: 22px;
    font-weight: 800;
    margin-bottom: 12px;
}

.patient-info {
    color: #475569;
    font-size: 14px;
    line-height: 2;
}

.pneumonia-badge {
    background: #fee2e2;
    color: #b91c1c;
    border: 1px solid #fecaca;
    padding: 8px 15px;
    border-radius: 20px;
    font-weight: 700;
    display: inline-block;
}

.normal-badge {
    background: #dcfce7;
    color: #15803d;
    border: 1px solid #bbf7d0;
    padding: 8px 15px;
    border-radius: 20px;
    font-weight: 700;
    display: inline-block;
}

.match-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 14px;
    padding: 16px 18px;
    margin-top: 10px;
}

.match-name {
    color: white;
    font-size: 16px;
    font-weight: 700;
}

.match-sub {
    color: #94a3b8;
    font-size: 12.5px;
    margin-top: 3px;
}

.search-result {
    background: rgba(14,165,233,0.10);
    border: 1px solid rgba(14,165,233,0.25);
    color: #bae6fd;
    border-radius: 10px;
    padding: 12px 15px;
    margin-top: 12px;
}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

try:
    records = get_reports()
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
        '🔎 Patient Lookup</div>'
        '<div style="color:#94a3b8;font-size:13px;margin-top:5px;">'
        'Search once, then open one patient\'s full record history.</div>',
        unsafe_allow_html=True
    )

with head_col2:
    if st.button("⬅ Back to Dashboard", use_container_width=True):
        st.switch_page("pages/docter_dashboard.py")

st.markdown(
    '<hr style="border:none;height:1px;background:#334155;margin:20px 0 30px 0;">',
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE FOR SELECTED PATIENT
# =========================================================

if "selected_patient_id" not in st.session_state:
    st.session_state.selected_patient_id = None


# =========================================================
# SEARCH BOX
# =========================================================

search = st.text_input(
    "Patient Search",
    placeholder="Search by Patient ID, name, contact number, Report ID or Report Code",
    label_visibility="collapsed"
)

# A fresh search should clear any previously selected patient, so typing
# a new query always goes back to the disambiguation list first.
if "last_search" not in st.session_state:
    st.session_state.last_search = ""

if search.strip() != st.session_state.last_search:
    st.session_state.selected_patient_id = None
    st.session_state.last_search = search.strip()


# =========================================================
# BUILD MATCHES (grouped by patient, not by report, so the
# same patient's multiple reports don't show up as multiple
# separate "results" to pick between)
# =========================================================

def matches_search(record, search_text):
    # If the doctor typed a plain number, treat it as an exact
    # Patient ID match only -- not Report ID, and not substring.
    # Report ID is a separate global counter, so matching it here
    # too could pull in an unrelated patient's report just because
    # its Report ID happens to equal the number typed.
    if search_text.isdigit():
        return search_text == str(record.get("patient_id", "")).lower()

    fields = [
        str(record.get("full_name", "")),
        str(record.get("phone", "")),
        str(record.get("report_code", "")),
    ]
    return any(search_text in f.lower() for f in fields)


matched_patients = {}   # patient_id -> {info + report_count}
matched_reports_by_patient = {}  # patient_id -> list of report records

if search.strip():
    search_text = search.strip().lower()
    for r in records:
        if matches_search(r, search_text):
            pid = r.get("patient_id")
            matched_reports_by_patient.setdefault(pid, []).append(r)
            if pid not in matched_patients:
                matched_patients[pid] = r
else:
    for r in records:
        pid = r.get("patient_id")
        matched_reports_by_patient.setdefault(pid, []).append(r)
        if pid not in matched_patients:
            matched_patients[pid] = r


# =========================================================
# STEP 1: DISAMBIGUATION LIST
# Shown when there's no search yet, or the search matches
# more than one distinct patient and none has been picked.
# =========================================================

def render_match_list():
    st.markdown(
        '<div class="search-result">'
        f'Found <b>{len(matched_patients)}</b> matching patient(s). '
        'Select one to view their full record.</div>',
        unsafe_allow_html=True
    )

    for pid, r in matched_patients.items():
        name_safe = html.escape(str(r.get("full_name", "N/A")))
        phone_safe = html.escape(str(r.get("phone", "N/A")))
        age = r.get("age", "N/A")
        gender_safe = html.escape(str(r.get("gender", "N/A")))
        report_count = len(matched_reports_by_patient.get(pid, []))

        col_info, col_btn = st.columns([5, 1])

        with col_info:
            st.markdown(
                '<div class="match-card">'
                f'<div class="match-name">👤 {name_safe}</div>'
                f'<div class="match-sub">Patient ID: {pid} &nbsp;|&nbsp; '
                f'Age: {age} &nbsp;|&nbsp; Gender: {gender_safe} &nbsp;|&nbsp; '
                f'Contact: {phone_safe} &nbsp;|&nbsp; '
                f'{report_count} report(s) on file</div>'
                '</div>',
                unsafe_allow_html=True
            )

        with col_btn:
            st.write("")
            if st.button("Open", key=f"open_{pid}", use_container_width=True):
                st.session_state.selected_patient_id = pid
                st.rerun()


# =========================================================
# STEP 2: SINGLE PATIENT DETAIL VIEW
# =========================================================

def render_patient_detail(pid):
    patient_reports = matched_reports_by_patient.get(pid) or [
        r for r in records if r.get("patient_id") == pid
    ]

    if not patient_reports:
        st.error("❌ No records found for this patient.")
        return

    # Reports are already ordered by created_at DESC from the query,
    # so the first one is the most recent.
    latest = patient_reports[0]

    name_safe = html.escape(str(latest.get("full_name", "N/A")))
    phone_safe = html.escape(str(latest.get("phone", "N/A")))
    gender_safe = html.escape(str(latest.get("gender", "N/A")))
    age = latest.get("age", "N/A")

    top_col1, top_col2 = st.columns([5, 1])

    with top_col1:
        st.markdown(
            '<div style="color:white;font-size:22px;font-weight:800;">'
            f'👤 {name_safe}</div>'
            f'<div style="color:#94a3b8;font-size:13px;margin-top:4px;">'
            f'Patient ID: {pid} &nbsp;|&nbsp; Age: {age} &nbsp;|&nbsp; '
            f'Gender: {gender_safe} &nbsp;|&nbsp; Contact: {phone_safe} '
            f'&nbsp;|&nbsp; {len(patient_reports)} report(s) on file</div>',
            unsafe_allow_html=True
        )

    with top_col2:
        if st.button("← Change Patient", use_container_width=True):
            st.session_state.selected_patient_id = None
            st.rerun()

    st.markdown(
        '<hr style="border:none;height:1px;background:#334155;margin:18px 0;">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="color:white;font-size:16px;font-weight:700;margin-bottom:6px;">'
        'Report History</div>',
        unsafe_allow_html=True
    )

    for r in patient_reports:
        report_id = r.get("report_id", "N/A")
        report_code = r.get("report_code", "")
        diagnosis = str(r.get("final_diagnosis", "N/A"))
        diagnosis_safe = html.escape(diagnosis)
        created_at_safe = html.escape(str(r.get("created_at", "N/A")))

        try:
            confidence_display = f"{float(r.get('confidence', 0)):.2f}%"
        except (TypeError, ValueError):
            confidence_display = html.escape(str(r.get("confidence", "N/A")))

        if "pneumonia" in diagnosis.strip().lower():
            badge_html = f'<span class="pneumonia-badge">🔴 {diagnosis_safe}</span>'
        else:
            badge_html = f'<span class="normal-badge">🟢 {diagnosis_safe}</span>'

        report_id_safe = html.escape(str(report_id))
        report_code_safe = html.escape(str(report_code))

        card_html = "".join([
            '<div class="patient-card">',
            '<div class="patient-info">',
            f'<b>Report ID:</b> {report_id_safe}',
            '&nbsp;&nbsp;|&nbsp;&nbsp;',
            f'<b>Report Code:</b> {report_code_safe}',
            '&nbsp;&nbsp;|&nbsp;&nbsp;',
            f'<b>Date:</b> {created_at_safe}',
            '<br><br>',
            badge_html,
            '&nbsp;&nbsp;',
            f'<b>Confidence:</b> {confidence_display}',
            '</div>',
            '</div>',
        ])

        st.markdown(card_html, unsafe_allow_html=True)

        act_col1, act_col2 = st.columns(2)

        with act_col1:
            if st.button(
                " Download PDF",
                key=f"detail_download_{report_id}",
                use_container_width=True
            ):
                if not report_code:
                    st.error("❌ Report code is missing.")
                else:
                    pdf_url = f"{FASTAPI_BASE_URL}/download/{report_code}"
                    try:
                        response = requests.get(pdf_url, timeout=30)
                        if response.status_code == 200:
                            st.download_button(
                                label="Save PDF",
                                data=response.content,
                                file_name=f"Report_{report_code}.pdf",
                                mime="application/pdf",
                                key=f"detail_save_{report_id}",
                                use_container_width=True
                            )
                        else:
                            st.error(
                                f"❌ PDF could not be retrieved. "
                                f"Status: {response.status_code}"
                            )
                    except requests.exceptions.ConnectionError:
                        st.error(
                            "❌ FastAPI is not running. "
                            "Start your FastAPI server first."
                        )
                    except requests.exceptions.Timeout:
                        st.error("❌ FastAPI request timed out.")
                    except Exception as e:
                        st.error(f"❌ PDF error: {e}")

        with act_col2:
            if report_code:
                pdf_url = f"{FASTAPI_BASE_URL}/download/{report_code}"
                st.markdown(
                    f'<a href="{pdf_url}" target="_blank" '
                    'style="display:block;text-align:center;padding:11px;'
                    'background:#0ea5e9;color:white;border-radius:10px;'
                    'text-decoration:none;font-weight:700;margin-top:1px;">'
                    ' View PDF</a>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("PDF unavailable")


# =========================================================
# ROUTING: which step to show
# =========================================================

if not matched_patients:
    st.info(" No matching patient records found.")

elif st.session_state.selected_patient_id is not None and \
        st.session_state.selected_patient_id in matched_patients:
    render_patient_detail(st.session_state.selected_patient_id)

elif len(matched_patients) == 1:
    # Exactly one match (e.g. searched an exact Report Code or Patient ID)
    # -- skip the extra click and go straight to the detail view.
    only_pid = next(iter(matched_patients))
    render_patient_detail(only_pid)

else:
    render_match_list()