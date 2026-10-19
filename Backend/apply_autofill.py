"""
Run this ONCE from inside your Backend folder:
    cd Backend
    python apply_autofill.py

It will:
  1. back up main.py  ->  main.py.bak
  2. add the auto-fill code to main.py
  3. create assets/autofill.js
  4. create the stored_patients table in MySQL
"""
import os
import sys
import shutil

MAIN = "main.py"

# ------------------------------------------------------------------
# Code that gets added to main.py
# ------------------------------------------------------------------
BACKEND_CODE = '''# =========================
# AUTO-FILL: remember patient data by X-ray fingerprint
# =========================
AUTOFILL_FIELDS = ["patient_name", "age", "gender", "wbc", "rbc", "platelet",
                   "hb", "temperature", "spo2", "pulse_rate", "crp"]
_AUTOFILL_COLS = ", ".join(AUTOFILL_FIELDS)


def image_hash(file_bytes):
    """Unique fingerprint of the uploaded X-ray file."""
    return hashlib.sha256(file_bytes).hexdigest()


def save_autofill_record(file_bytes, data):
    """Store (or update) one patient's values, keyed by X-ray fingerprint."""
    placeholders = ", ".join(["%s"] * (len(AUTOFILL_FIELDS) + 1))
    updates = ", ".join(f"{f}=VALUES({f})" for f in AUTOFILL_FIELDS)
    values = [image_hash(file_bytes)] + [str(data.get(f, "") or "") for f in AUTOFILL_FIELDS]

    conn = get_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"INSERT INTO stored_patients (image_hash, {_AUTOFILL_COLS}) VALUES ({placeholders}) "
                f"ON DUPLICATE KEY UPDATE {updates}",
                values,
            )
            conn.commit()
        finally:
            cursor.close()
    finally:
        conn.close()


@app.post("/lookup")
async def lookup(file: UploadFile = File(...)):
    """Called by the browser as soon as an X-ray is dropped on the form."""
    contents = await file.read()
    try:
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(
                    f"SELECT {_AUTOFILL_COLS} FROM stored_patients WHERE image_hash = %s",
                    (image_hash(contents),),
                )
                row = cursor.fetchone()
            finally:
                cursor.close()
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"found": row is not None, "data": row}


'''

MOUNT_CODE = '''app.mount("/static", StaticFiles(directory="static"), name="static")

# folder for autofill.js (kept outside "static" because static/ is auto-cleaned)
os.makedirs("assets", exist_ok=True)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")'''

CHECKBOX_HTML = '''<label style="display:flex;gap:8px;align-items:center;font-weight:600;margin-bottom:18px;">
          <input type="checkbox" name="save_for_autofill" value="1" style="width:auto;">
          Remember this patient (auto-fill when this X-ray is uploaded again)
        </label>

        <button class="btn" type="submit"> Analyze &amp; Generate Report</button>'''

SAVE_CALL = '''        contents = await file.read()

        # AUTO-FILL: remember this patient if the checkbox was ticked
        if save_for_autofill:
            try:
                save_autofill_record(contents, {
                    "patient_name": patient_name, "age": age, "gender": gender,
                    "wbc": wbc, "rbc": rbc, "platelet": platelet, "hb": hb,
                    "temperature": temperature, "spo2": spo2,
                    "pulse_rate": pulse_rate, "crp": crp,
                })
            except Exception as autofill_err:
                print("Autofill save error:", autofill_err)
'''

JS_CODE = '''(function () {
  const form = document.querySelector("form");
  const fileInput = form.querySelector('input[type=file]');
  const box = document.querySelector(".upload-box");

  // names of the boxes to fill (same as name="..." in the form)
  const FIELDS = ["patient_name", "age", "gender", "wbc", "rbc", "platelet",
                  "hb", "temperature", "spo2", "pulse_rate", "crp"];

  // message line inside the upload box
  const status = document.createElement("div");
  status.className = "upload-hint";
  status.style.fontWeight = "600";
  box.appendChild(status);

  // send the X-ray to Python, then fill the form with the answer
  async function autofill(file) {
    status.style.color = "#64748b";
    status.textContent = "Looking up stored patient data...";

    const fd = new FormData();
    fd.append("file", file);

    try {
      const res = await fetch("/lookup", { method: "POST", body: fd });
      const json = await res.json();

      if (!json.found) {
        status.style.color = "#b45309";
        status.textContent = "No stored record for this X-ray. Enter values once and tick 'Remember this patient'.";
        return;
      }

      FIELDS.forEach(name => {
        const el = form.elements[name];
        if (el && json.data[name] != null) el.value = json.data[name];
      });

      status.style.color = "#15803d";
      status.textContent = "\\u2714 Patient details, labs, vitals and CRP auto-filled from stored record.";
    } catch (e) {
      status.style.color = "#b91c1c";
      status.textContent = "Lookup failed. Please enter values manually.";
    }
  }

  // "Choose File" button, or dropping onto the file input itself
  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) autofill(fileInput.files[0]);
  });

  // dropping anywhere on the dashed box
  box.addEventListener("dragover", e => e.preventDefault());
  box.addEventListener("drop", e => {
    e.preventDefault();
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      fileInput.dispatchEvent(new Event("change"));
    }
  });
})();
'''

CREATE_SQL = """CREATE TABLE IF NOT EXISTS stored_patients (
    image_hash   CHAR(64) PRIMARY KEY,
    patient_name VARCHAR(255),
    age          VARCHAR(10),
    gender       VARCHAR(50),
    wbc          VARCHAR(20),
    rbc          VARCHAR(20),
    platelet     VARCHAR(20),
    hb           VARCHAR(20),
    temperature  VARCHAR(20),
    spo2         VARCHAR(20),
    pulse_rate   VARCHAR(20),
    crp          VARCHAR(20),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""


def fail(msg):
    print("\nERROR:", msg)
    print("Nothing was changed. Send me this message and I will fix it.")
    sys.exit(1)


def patch(src, old, new, label):
    count = src.count(old)
    if count != 1:
        fail(f"Could not find the place to edit: '{label}' (found {count} times, expected 1).")
    return src.replace(old, new, 1)


def main():
    if not os.path.isfile(MAIN):
        fail("main.py not found. Run this script from inside the Backend folder.")

    with open(MAIN, "r", encoding="utf-8") as f:
        src = f.read()

    if "stored_patients" in src:
        print("Auto-fill is already added to main.py. Skipping the main.py edit.")
    else:
        # --- edits inside /predict first ---
        src = patch(
            src,
            '    crp: str = Form(""),\n    file: UploadFile = File(...)\n):',
            '    crp: str = Form(""),\n    save_for_autofill: str = Form(""),\n    file: UploadFile = File(...)\n):',
            "predict() inputs",
        )
        src = patch(src, "        contents = await file.read()\n", SAVE_CALL, "predict() file read")

        # --- the rest ---
        src = patch(src, "import joblib\n", "import joblib\nimport hashlib\n", "import line")
        src = patch(
            src,
            'app.mount("/static", StaticFiles(directory="static"), name="static")',
            MOUNT_CODE,
            "static mount",
        )
        src = patch(src, 'BASE_CSS = """', BACKEND_CODE + 'BASE_CSS = """', "before BASE_CSS")
        src = patch(
            src,
            '<button class="btn" type="submit"> Analyze &amp; Generate Report</button>',
            CHECKBOX_HTML,
            "Analyze button",
        )
        # the first </body> in the file belongs to the home page
        if "</body>" not in src:
            fail("Could not find </body> in the home page HTML.")
        src = src.replace("</body>", '<script src="/assets/autofill.js"></script>\n</body>', 1)

        shutil.copy(MAIN, "main.py.bak")
        with open(MAIN, "w", encoding="utf-8") as f:
            f.write(src)
        print("main.py updated (backup saved as main.py.bak)")

    # --- assets/autofill.js ---
    os.makedirs("assets", exist_ok=True)
    with open(os.path.join("assets", "autofill.js"), "w", encoding="utf-8") as f:
        f.write(JS_CODE)
    print("assets/autofill.js created")

    # --- MySQL table ---
    try:
        sys.path.insert(0, os.getcwd())
        from database import get_connection
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(CREATE_SQL)
        conn.commit()
        cur.close()
        conn.close()
        print("MySQL table stored_patients is ready")
    except Exception as e:
        print("\nCould not create the MySQL table automatically:", e)
        print("Please run this SQL in MySQL Workbench (with pneumonia_project selected):\n")
        print(CREATE_SQL + ";")

    print("\nDone. Restart your server:  uvicorn main:app --reload")


if __name__ == "__main__":
    main()