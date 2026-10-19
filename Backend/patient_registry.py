"""
Patient registry: save a patient's X-ray + blood + oxygen + CRP values ONCE,
so they can be auto-filled later by dragging the X-ray on the home page.

Pages added:
    GET  /register   -> form to save a patient
    POST /register   -> saves the X-ray image + all values
    GET  /records    -> table of all saved patients
    POST /records/delete -> delete one saved patient
"""
import os
import html
import hashlib

import cv2
import numpy as np
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import HTMLResponse, RedirectResponse

IMAGE_DIR = "patient_images"
ALLOWED_EXT = {".jpg", ".jpeg", ".png"}

FIELDS = ["patient_name", "age", "gender", "wbc", "rbc", "platelet",
          "hb", "temperature", "spo2", "pulse_rate", "crp"]

REGISTER_FORM = """
<form action="/register" method="post" enctype="multipart/form-data">

  <div class="field-group">
    <p class="section-label">Patient Information</p>
    <div class="grid grid-3">
      <div><label>Patient Name</label>
        <input type="text" name="patient_name" placeholder="e.g. John Carter" required></div>
      <div><label>Age</label>
        <input type="number" name="age" placeholder="e.g. 34" required></div>
      <div><label>Gender</label>
        <input type="text" name="gender" placeholder="Male / Female / Other" required></div>
    </div>
  </div>

  <div class="field-group">
    <p class="section-label">Chest X-Ray Image</p>
    <div class="upload-box">
      <div class="upload-icon">📤</div>
      <input type="file" name="file" accept="image/*" required>
      <div class="upload-hint">JPG or PNG &middot; this X-ray becomes the key that auto-fills the values below</div>
    </div>
  </div>

  <div class="field-group">
    <p class="section-label">Lab Values</p>
    <div class="grid grid-4">
      <div><label>WBC (cells/µL)</label><input type="text" name="wbc" placeholder="e.g. 8200"></div>
      <div><label>RBC (mill/µL)</label><input type="text" name="rbc" placeholder="e.g. 4.8"></div>
      <div><label>Platelets (×10³/µL)</label><input type="text" name="platelet" placeholder="e.g. 250"></div>
      <div><label>Hemoglobin (g/dL)</label><input type="text" name="hb" placeholder="e.g. 13.5"></div>
    </div>
  </div>

  <div class="field-group">
    <p class="section-label">Vitals</p>
    <div class="grid grid-3">
      <div><label>Temperature (°F)</label><input type="text" name="temperature" placeholder="e.g. 98.6"></div>
      <div><label>SpO2 (%)</label><input type="text" name="spo2" placeholder="e.g. 97"></div>
      <div><label>Pulse Rate (bpm)</label><input type="text" name="pulse_rate" placeholder="e.g. 78"></div>
    </div>
  </div>

  <div class="field-group">
    <p class="section-label">CRP</p>
    <div class="grid grid-3">
      <div><label>CRP (mg/L)</label><input type="text" name="crp" placeholder="e.g. 24.5"></div>
    </div>
  </div>

  <button class="btn" type="submit">Save Patient Data</button>
  <div class="upload-hint" style="text-align:center;margin-top:10px;">
    After saving, go to the home page and drag this same X-ray. All values fill automatically.
  </div>
</form>
"""


def create_router(base_css, get_connection):
    router = APIRouter()
    os.makedirs(IMAGE_DIR, exist_ok=True)

    nav = """
    <div class="actions" style="margin-bottom:24px;flex-wrap:wrap;">
      <a href="/" class="btn btn-outline">Home / New Scan</a>
      <a href="/register" class="btn btn-outline">Register Patient</a>
      <a href="/records" class="btn btn-outline">Stored Patient Data</a>
    </div>"""

    def page(title, subtitle, body):
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &middot; Pneumonia Detection System</title>
<style>{base_css}</style>
</head>
<body>
<div class="shell">
  <div class="brand">
    <div class="logo">🫁</div>
    <h1>Pneumonia Detection System<span>{subtitle}</span></h1>
  </div>
  <div class="card">
    <div class="card-pad">
      {nav}
      {body}
    </div>
  </div>
</div>
</body>
</html>"""

    @router.get("/register", response_class=HTMLResponse)
    def register_page():
        return page("Register Patient", "Save a patient once &mdash; auto-fill forever", REGISTER_FORM)

    @router.post("/register")
    async def register_patient(
        patient_name: str = Form(...),
        age: str = Form(...),
        gender: str = Form(...),
        wbc: str = Form(""),
        rbc: str = Form(""),
        platelet: str = Form(""),
        hb: str = Form(""),
        temperature: str = Form(""),
        spo2: str = Form(""),
        pulse_rate: str = Form(""),
        crp: str = Form(""),
        file: UploadFile = File(...),
    ):
        contents = await file.read()

        # make sure the upload really is an image
        decoded = cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR) if contents else None
        if decoded is None:
            msg = ('<div class="info-note"><h4>Invalid image</h4>'
                   '<p>The uploaded file could not be read as an image. Please choose a JPG or PNG X-ray.</p></div>')
            return HTMLResponse(page("Register Patient", "Save a patient once", msg + REGISTER_FORM),
                                status_code=400)

        key = hashlib.sha256(contents).hexdigest()
        ext = os.path.splitext(file.filename or "")[1].lower()
        if ext not in ALLOWED_EXT:
            ext = ".jpg"
        image_name = f"{key[:24]}{ext}"
        with open(os.path.join(IMAGE_DIR, image_name), "wb") as f:
            f.write(contents)

        values = [key, image_name, patient_name.strip(), age.strip(), gender.strip(),
                  wbc.strip(), rbc.strip(), platelet.strip(), hb.strip(),
                  temperature.strip(), spo2.strip(), pulse_rate.strip(), crp.strip()]

        conn = get_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "REPLACE INTO stored_patients "
                    "(image_hash, image_name, patient_name, age, gender, wbc, rbc, platelet, "
                    "hb, temperature, spo2, pulse_rate, crp) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    values,
                )
                conn.commit()
            finally:
                cursor.close()
        finally:
            conn.close()

        return RedirectResponse("/records?saved=1", status_code=303)

    @router.get("/records", response_class=HTMLResponse)
    def records_page(saved: str = ""):
        rows, error = [], None
        try:
            conn = get_connection()
            try:
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.execute(
                        "SELECT image_hash, image_name, patient_name, age, gender, wbc, rbc, "
                        "platelet, hb, temperature, spo2, pulse_rate, crp "
                        "FROM stored_patients ORDER BY created_at DESC"
                    )
                    rows = cursor.fetchall()
                finally:
                    cursor.close()
            finally:
                conn.close()
        except Exception as e:
            error = str(e)

        banner = ""
        if saved:
            banner = ('<div class="info-note" style="background:linear-gradient(135deg,#f0fdf4,#dcfce7);'
                      'border-color:#bbf7d0;"><h4 style="color:#15803d;">✔ Patient saved</h4>'
                      '<p>Go to the home page and drag this patient\'s X-ray. '
                      'All values will fill automatically.</p></div>')

        if error:
            body_rows = (f'<tr><td colspan="14" style="text-align:center;padding:24px;color:#b91c1c;">'
                         f'Could not load records: {html.escape(error)}<br>'
                         f'(Run setup_registry.py once to add the missing column.)</td></tr>')
        elif not rows:
            body_rows = ('<tr><td colspan="14" style="text-align:center;padding:24px;color:#94a3b8;">'
                         'No patients saved yet. Use "Register Patient" to add one.</td></tr>')
        else:
            body_rows = ""
            for r in rows:
                if r.get("image_name"):
                    thumb = (f'<img src="/patient_images/{html.escape(r["image_name"])}" '
                             f'style="width:56px;height:56px;object-fit:cover;border-radius:8px;">')
                else:
                    thumb = "-"

                def cell(k):
                    v = r.get(k)
                    return html.escape(str(v)) if v not in (None, "") else "-"

                body_rows += f"""
                <tr>
                  <td>{thumb}</td>
                  <td><strong>{cell('patient_name')}</strong></td>
                  <td>{cell('age')}</td>
                  <td>{cell('gender')}</td>
                  <td>{cell('wbc')}</td>
                  <td>{cell('rbc')}</td>
                  <td>{cell('platelet')}</td>
                  <td>{cell('hb')}</td>
                  <td>{cell('temperature')}</td>
                  <td>{cell('spo2')}</td>
                  <td>{cell('pulse_rate')}</td>
                  <td>{cell('crp')}</td>
                  <td>
                    <form action="/records/delete" method="post"
                          onsubmit="return confirm('Delete this patient record?');">
                      <input type="hidden" name="image_hash" value="{html.escape(r['image_hash'])}">
                      <button type="submit" class="btn btn-outline"
                              style="width:auto;padding:6px 12px;font-size:12px;color:#b91c1c;border-color:#fecaca;">
                        Delete</button>
                    </form>
                  </td>
                </tr>"""

        table = f"""
        {banner}
        <div class="lab-card" style="overflow-x:auto;">
          <table class="lab-table">
            <thead><tr>
              <th>X-ray</th><th>Name</th><th>Age</th><th>Gender</th>
              <th>WBC</th><th>RBC</th><th>Platelets</th><th>Hb</th>
              <th>Temp (°F)</th><th>SpO2</th><th>Pulse</th><th>CRP</th><th></th>
            </tr></thead>
            <tbody>{body_rows}</tbody>
          </table>
        </div>"""
        return page("Stored Patient Data", "Saved patients available for auto-fill", table)

    @router.post("/records/delete")
    async def delete_record(image_hash: str = Form(...)):
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("SELECT image_name FROM stored_patients WHERE image_hash = %s", (image_hash,))
                row = cursor.fetchone()
                cursor.execute("DELETE FROM stored_patients WHERE image_hash = %s", (image_hash,))
                conn.commit()
            finally:
                cursor.close()
        finally:
            conn.close()

        if row and row.get("image_name"):
            path = os.path.join(IMAGE_DIR, os.path.basename(row["image_name"]))
            try:
                if os.path.isfile(path):
                    os.remove(path)
            except OSError:
                pass
        return RedirectResponse("/records", status_code=303)

    return router