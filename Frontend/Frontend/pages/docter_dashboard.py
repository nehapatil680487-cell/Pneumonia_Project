import streamlit as st
import mysql.connector
import requests
import html


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Doctor Dashboard | PneumoScan AI",
    page_icon="🩺",
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

        st.switch_page(
            "pages/doctor_login.py"
        )

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
# GET REPORTS FROM MYSQL
# =========================================================

def get_reports():

    conn = None
    cursor = None

    try:

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        query = """
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

        ORDER BY dr.report_id DESC
        """

        cursor.execute(query)

        return cursor.fetchall()

    finally:

        if cursor is not None:
            cursor.close()

        if conn is not None:
            conn.close()


# =========================================================
# CSS
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

.patient-card.duplicate-name {
    border: 2px solid #f59e0b;
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

.duplicate-id-highlight {
    background: #fef08a;
    color: #854d0e;
    padding: 2px 8px;
    border-radius: 6px;
    font-weight: 800;
}

.stat-card {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.13);
    border-radius: 18px;
    padding: 22px;
    min-height: 125px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}

.stat-title {
    color: #cbd5e1;
    font-size: 14px;
    margin-top: 10px;
}

.stat-number {
    color: white;
    font-size: 34px;
    font-weight: 800;
    margin-top: 5px;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 35px 0 15px 0;
    line-height: 1.7;
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
# LOAD DATABASE
# =========================================================

try:

    records = get_reports()

except mysql.connector.Error as e:

    st.error(
        "❌ Unable to connect to MySQL database."
    )

    st.code(str(e))

    st.stop()

except Exception as e:

    st.error(
        "❌ An unexpected error occurred."
    )

    st.code(str(e))

    st.stop()


# =========================================================
# HEADER
# =========================================================

header_col1, header_col2 = st.columns(
    [5, 1]
)


with header_col1:

    st.markdown(
        '<div style="color:white;font-size:32px;font-weight:800;letter-spacing:-0.5px;">'
        '🩺 PneumoScan AI</div>'
        '<div style="color:#94a3b8;font-size:14px;margin-top:5px;">'
        'Doctor Portal • Patient Diagnosis Management</div>',
        unsafe_allow_html=True
    )


with header_col2:

    st.markdown(
        '<div style="display:inline-block;background:rgba(16,185,129,0.15);'
        'border:1px solid rgba(16,185,129,0.40);color:#6ee7b7;padding:7px 14px;'
        'border-radius:20px;font-size:13px;font-weight:600;margin-bottom:8px;">'
        '● Doctor Access</div>',
        unsafe_allow_html=True
    )

    if st.button(
        " Logout",
        use_container_width=True
    ):

        st.session_state.doctor_login = False

        st.switch_page(
            "pages/doctor_login.py"
        )


# =========================================================
# LINE
# =========================================================

st.markdown(
    '<hr style="border:none;height:1px;background:#334155;margin:20px 0 35px 0;">',
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD HEADER
# =========================================================

title_col, lookup_col, refresh_col = st.columns(
    [5, 1.4, 1]
)


with title_col:

    st.markdown(
        '<div style="color:white;font-size:24px;font-weight:700;margin-top:10px;">'
        'Doctor Dashboard</div>'
        '<div style="color:#94a3b8;font-size:13px;margin-top:5px;">'
        'Monitor patient diagnosis results and access generated medical reports.</div>',
        unsafe_allow_html=True
    )


with lookup_col:

    if st.button(
        " Patient Lookup",
        use_container_width=True
    ):

        st.switch_page(
            "pages/patient_search.py"
        )


with refresh_col:

    if st.button(
        " Refresh Data",
        use_container_width=True
    ):

        st.rerun()


# =========================================================
# STATISTICS
# =========================================================

total_reports = len(records)


# ---------------------------------------------------------
# UNIQUE PATIENTS
# ---------------------------------------------------------

unique_patient_ids = set()

for record in records:

    patient_id = record.get(
        "patient_id"
    )

    if patient_id is not None:

        unique_patient_ids.add(
            patient_id
        )


total_patients = len(
    unique_patient_ids
)


# ---------------------------------------------------------
# DIAGNOSIS COUNT
# ---------------------------------------------------------

pneumonia_count = 0
normal_count = 0

for record in records:

    diagnosis = str(
        record.get(
            "final_diagnosis",
            ""
        )
    ).strip().lower()

    if "pneumonia" in diagnosis:

        pneumonia_count += 1

    else:

        normal_count += 1


# =========================================================
# STATISTIC CARDS
# =========================================================

def stat_card_html(title, number):
    return (
        '<div class="stat-card">'
        f'<div class="stat-title">{title}</div>'
        f'<div class="stat-number">{number}</div>'
        '</div>'
    )


col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(
        stat_card_html("Total Patients", total_patients),
        unsafe_allow_html=True
    )


with col2:
    st.markdown(
        stat_card_html("Total Reports", total_reports),
        unsafe_allow_html=True
    )


with col3:
    st.markdown(
        stat_card_html("Pneumonia Cases", pneumonia_count),
        unsafe_allow_html=True
    )


with col4:
    st.markdown(
        stat_card_html("Normal Cases", normal_count),
        unsafe_allow_html=True
    )


# =========================================================
# PATIENT RECORDS HEADER
# =========================================================

st.markdown(
    '<div style="color:white;font-size:22px;font-weight:700;margin-top:35px;margin-bottom:5px;">'
    ' Patient Records</div>'
    '<div style="color:#94a3b8;font-size:13px;margin-bottom:18px;">'
    'Search using Patient ID, patient name, contact number, '
    'Report ID or Report Code.</div>',
    unsafe_allow_html=True
)


# =========================================================
# SEARCH BOX
# =========================================================

search = st.text_input(
    "Patient Search",

    placeholder=(
        "Example: 10  |  Neha Patil  |  DB7C4CD405"
    ),

    label_visibility="collapsed"
)


# =========================================================
# FILTER RECORDS
# =========================================================

if search.strip():

    search_text = (
        search.strip()
        .lower()
    )

    # If the doctor typed a plain number, treat it as an exact
    # Patient ID / Report ID lookup instead of a substring match.
    # This avoids "10" also matching "100", "210", "1099", etc.
    is_numeric_search = search_text.isdigit()

    filtered_records = []

    for record in records:

        patient_name = str(
            record.get(
                "full_name",
                ""
            )
        ).lower()

        phone = str(
            record.get(
                "phone",
                ""
            )
        ).lower()

        patient_id = str(
            record.get(
                "patient_id",
                ""
            )
        ).lower()

        report_id = str(
            record.get(
                "report_id",
                ""
            )
        ).lower()

        report_code = str(
            record.get(
                "report_code",
                ""
            )
        ).lower()


        # -------------------------------------------------
        # SEARCH
        # -------------------------------------------------

        if is_numeric_search:

            # Exact match on Patient ID only. Report ID is a
            # separate global counter, so matching it here too
            # could pull in an unrelated patient's report just
            # because its Report ID happens to equal the number
            # typed. Patient ID must stay the sole numeric key.
            match = (
                search_text == patient_id
            )

        else:

            match = (

                search_text in patient_name

                or search_text in phone

                or search_text in patient_id

                or search_text in report_id

                or search_text in report_code

            )

        if match:

            filtered_records.append(
                record
            )

else:

    filtered_records = records


# =========================================================
# DETECT DUPLICATE NAMES
# Only counts as "duplicate" if the search text actually
# matched the patient's NAME (not id/phone/report_id/code).
# Otherwise a numeric search like "2" would falsely trigger
# this warning just because it matched unrelated records
# that happen to share a name by coincidence.
# =========================================================

search_text_for_names = (
    search.strip().lower()
    if search.strip()
    else ""
)

name_matched_records = [
    r for r in filtered_records
    if search_text_for_names
    and search_text_for_names in str(r.get("full_name", "")).lower()
]

name_to_patient_ids = {}

for record in name_matched_records:

    name_key = str(
        record.get("full_name", "")
    ).strip().lower()

    pid = record.get("patient_id")

    if name_key not in name_to_patient_ids:
        name_to_patient_ids[name_key] = set()

    if pid is not None:
        name_to_patient_ids[name_key].add(pid)

duplicate_names = {
    name for name, pids in name_to_patient_ids.items()
    if len(pids) > 1
}

if duplicate_names:

    st.warning(
        "⚠️ Multiple different patients share the same name in these "
        "results. Please confirm using **Patient ID**, **Contact Number**, "
        "or **Date** before opening a report."
    )


# =========================================================
# SORT RECORDS
# Group same-name records together, then by patient_id, then
# by most recent report first -- makes duplicate names easy
# to compare side by side instead of scattered.
# =========================================================

filtered_records = sorted(
    filtered_records,
    key=lambda r: (
        str(r.get("full_name", "")).strip().lower(),
        r.get("patient_id") or 0,
        -(r.get("report_id") or 0),
    )
)


# =========================================================
# SEARCH INFORMATION
# =========================================================

filtered_patient_ids = set()

for record in filtered_records:

    patient_id = record.get(
        "patient_id"
    )

    if patient_id is not None:

        filtered_patient_ids.add(
            patient_id
        )


if search.strip():

    st.markdown(
        '<div class="search-result"> Search: '
        f'<b>{html.escape(search.strip())}</b> &nbsp;→&nbsp; '
        f'Found <b>{len(filtered_records)}</b> report(s) from '
        f'<b>{len(filtered_patient_ids)}</b> patient(s)</div>',
        unsafe_allow_html=True
    )

else:

    st.markdown(
        '<div style="color:#64748b;font-size:13px;margin-top:10px;">'
        f'Showing <b>{len(filtered_records)}</b> report(s) from '
        f'<b>{len(filtered_patient_ids)}</b> patient(s)</div>',
        unsafe_allow_html=True
    )


# =========================================================
# NO RECORDS
# =========================================================

if not filtered_records:

    st.info(
        " No matching patient records found."
    )


# =========================================================
# DISPLAY PATIENT RECORDS
# =========================================================

for record in filtered_records:


    # =====================================================
    # GET DATA
    # =====================================================

    report_id = record.get(
        "report_id",
        "N/A"
    )

    report_code = record.get(
        "report_code",
        ""
    )

    patient_id = record.get(
        "patient_id",
        "N/A"
    )

    patient_name = record.get(
        "full_name",
        "N/A"
    )

    age = record.get(
        "age",
        "N/A"
    )

    gender = record.get(
        "gender",
        "N/A"
    )

    phone = record.get(
        "phone",
        "N/A"
    )

    diagnosis = record.get(
        "final_diagnosis",
        "N/A"
    )

    confidence = record.get(
        "confidence",
        0
    )

    created_at = record.get(
        "created_at",
        "N/A"
    )


    # =====================================================
    # ESCAPE HTML
    # =====================================================

    patient_name_safe = html.escape(
        str(patient_name)
    )

    diagnosis_safe = html.escape(
        str(diagnosis)
    )

    gender_safe = html.escape(
        str(gender)
    )

    phone_safe = html.escape(
        str(phone)
    )

    report_code_safe = html.escape(
        str(report_code)
    )

    created_at_safe = html.escape(
        str(created_at)
    )

    patient_id_safe = html.escape(str(patient_id))
    report_id_safe = html.escape(str(report_id))
    age_safe = html.escape(str(age))


    # =====================================================
    # DUPLICATE NAME CHECK FOR THIS CARD
    # =====================================================

    name_key = str(patient_name).strip().lower()
    is_duplicate_name = name_key in duplicate_names

    card_class = (
        "patient-card duplicate-name"
        if is_duplicate_name
        else "patient-card"
    )

    if is_duplicate_name:

        patient_id_display = (
            f'<span class="duplicate-id-highlight">{patient_id_safe}</span>'
        )

    else:

        patient_id_display = patient_id_safe


    # =====================================================
    # CONFIDENCE
    # =====================================================

    try:

        confidence_value = float(
            confidence
        )

        confidence_display = (
            f"{confidence_value:.2f}%"
        )

    except (TypeError, ValueError):

        confidence_display = html.escape(
            str(confidence)
        )


    # =====================================================
    # DIAGNOSIS BADGE
    # =====================================================

    diagnosis_lower = str(
        diagnosis
    ).strip().lower()


    if "pneumonia" in diagnosis_lower:

        result_html = (
            f'<span class="pneumonia-badge">🔴 {diagnosis_safe}</span>'
        )

    else:

        result_html = (
            f'<span class="normal-badge">🟢 {diagnosis_safe}</span>'
        )


    # =====================================================
    # PATIENT CARD
    # =====================================================

    card_html = "".join([
        f'<div class="{card_class}">',
        f'<div class="patient-name">👤 {patient_name_safe}</div>',
        '<div class="patient-info">',
        f'<b>Patient ID:</b> {patient_id_display}',
        '&nbsp;&nbsp;|&nbsp;&nbsp;',
        f'<b>Report ID:</b> {report_id_safe}',
        '&nbsp;&nbsp;|&nbsp;&nbsp;',
        f'<b>Report Code:</b> {report_code_safe}',
        '<br>',
        f'<b>Age:</b> {age_safe}',
        '&nbsp;&nbsp;|&nbsp;&nbsp;',
        f'<b>Gender:</b> {gender_safe}',
        '&nbsp;&nbsp;|&nbsp;&nbsp;',
        f'<b>Contact:</b> {phone_safe}',
        '<br>',
        f'<b>Date:</b> {created_at_safe}',
        '<br><br>',
        result_html,
        '&nbsp;&nbsp;',
        f'<b>Confidence:</b> {confidence_display}',
        '</div>',
        '</div>',
    ])

    st.markdown(
        card_html,
        unsafe_allow_html=True
    )


    # =====================================================
    # ACTION BUTTONS
    # =====================================================

    action1, action2 = st.columns(2)


    # =====================================================
    # DOWNLOAD PDF
    # =====================================================

    with action1:

        if st.button(
            " Download PDF",
            key=f"download_button_{report_id}",
            use_container_width=True
        ):

            if not report_code:

                st.error(
                    "❌ Report code is missing."
                )

            else:

                pdf_url = (
                    f"{FASTAPI_BASE_URL}"
                    f"/download/{report_code}"
                )

                try:

                    response = requests.get(
                        pdf_url,
                        timeout=30
                    )


                    if response.status_code == 200:

                        st.download_button(

                            label="⬇ Save PDF",

                            data=response.content,

                            file_name=(
                                f"Report_{report_code}.pdf"
                            ),

                            mime="application/pdf",

                            key=f"save_pdf_{report_id}",

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

                    st.error(
                        "❌ FastAPI request timed out."
                    )


                except Exception as e:

                    st.error(
                        f"❌ PDF error: {e}"
                    )


    # =====================================================
    # VIEW PDF
    # =====================================================

    with action2:

        if report_code:

            pdf_url = (
                f"{FASTAPI_BASE_URL}"
                f"/download/{report_code}"
            )

            st.markdown(
                f'<a href="{pdf_url}" target="_blank" '
                'style="display:block;text-align:center;padding:11px;'
                'background:#0ea5e9;color:white;border-radius:10px;'
                'text-decoration:none;font-weight:700;margin-top:1px;">'
                ' View PDF</a>',
                unsafe_allow_html=True
            )

        else:

            st.warning(
                "PDF unavailable"
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">PneumoScan AI • '
    'AI-Assisted Pneumonia Screening System<br>Doctor Portal</div>',
    unsafe_allow_html=True
)