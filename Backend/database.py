import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="System",
        database="pneumonia_project"
    )


# =========================
# USER FUNCTIONS
# =========================

def add_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users (username, password)
            VALUES (%s, %s)
            """,
            (username, password)
        )

        connection.commit()
        return True

    except mysql.connector.IntegrityError:
        return False

    finally:
        cursor.close()
        connection.close()


def check_user(username, password):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = %s
            AND password = %s
            """,
            (username, password)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


# =========================
# PATIENT FUNCTIONS
# =========================

def get_patient_by_user_id(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                patient_id,
                user_id,
                full_name,
                age,
                gender,
                phone,
                created_at
            FROM patients
            WHERE user_id = %s
            ORDER BY patient_id DESC
            LIMIT 1
            """,
            (user_id,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        connection.close()


def add_patient(user_id, full_name, age, gender, phone):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO patients
            (user_id, full_name, age, gender, phone)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (user_id, full_name, age, gender, phone)
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        cursor.close()
        connection.close()


def update_patient(patient_id, full_name, age, gender, phone):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            UPDATE patients
            SET full_name = %s,
                age = %s,
                gender = %s,
                phone = %s
            WHERE patient_id = %s
            """,
            (full_name, age, gender, phone, patient_id)
        )

        connection.commit()

    finally:
        cursor.close()
        connection.close()


# =========================
# DIAGNOSIS REPORT
# =========================

def add_diagnosis_report(
    patient_id,
    report_code,
    image_name,
    final_diagnosis,
    confidence,
    pdf_path,
    severity=None
):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO diagnosis_reports
            (
                patient_id,
                report_code,
                image_name,
                final_diagnosis,
                confidence,
                pdf_path,
                severity
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                patient_id,
                report_code,
                image_name,
                final_diagnosis,
                confidence,
                pdf_path,
                severity
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        cursor.close()
        connection.close()


# =========================
# USAGE / HISTORY
# =========================

def get_reports_by_user_id(user_id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT
                dr.report_id,
                dr.report_code,
                dr.image_name,
                dr.final_diagnosis,
                dr.confidence,
                dr.pdf_path,
                dr.severity,
                dr.created_at,
                p.patient_id,
                p.full_name,
                p.age,
                p.gender,
                p.phone
            FROM diagnosis_reports dr
            INNER JOIN patients p
                ON dr.patient_id = p.patient_id
            WHERE p.user_id = %s
            ORDER BY dr.created_at DESC
            """,
            (user_id,)
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        connection.close()