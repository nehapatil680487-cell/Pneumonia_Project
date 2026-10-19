"""
Excel auto-fill.
Reads patients_data.xlsx (same folder as this file) and returns one patient's
details when you send the patient name + X-ray file name.
"""
import os
import re
from fastapi import APIRouter
from openpyxl import load_workbook

EXCEL_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patients_data .xlsx")

router = APIRouter()

FIELDS = ["patient_name", "age", "gender", "wbc", "rbc", "platelet",
          "hb", "temperature", "spo2", "pulse_rate", "crp"]

# Excel column headings that are understood (spaces, capitals, units don't matter)
ALIASES = {
    "patient_name": ["patientname", "fullname", "name"],
    "age":          ["age"],
    "gender":       ["gender", "sex"],
    "xray":         ["xrayfile", "xrayimage", "xrayname", "chestxray", "xray", "imagefile",
                     "imagename", "image", "filename", "file"],
    "wbc":          ["wbc", "whitebloodcell"],
    "rbc":          ["rbc", "redbloodcell"],
    "platelet":     ["platelets", "platelet", "plt"],
    "hb":           ["hemoglobin", "haemoglobin", "hgb", "hb"],
    "temperature":  ["temperature", "temp"],
    "spo2":         ["spo2", "oxygen", "o2"],
    "pulse_rate":   ["pulserate", "pulse", "heartrate"],
    "crp":          ["crp"],
}


def _key(text):
    return re.sub(r"[^a-z0-9]", "", str(text or "").lower())


def _field_for_header(header):
    k = _key(header)
    if not k:
        return None
    for field, names in ALIASES.items():
        for n in names:
            if k.startswith(n):
                return field
    return None


def _fmt(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def _norm_name(s):
    return " ".join(str(s or "").lower().split())


def _norm_file(s):
    s = os.path.basename(str(s or "").replace("\\", "/")).strip().lower()
    for ext in (".png", ".jpg", ".jpeg"):
        if s.endswith(ext):
            s = s[: -len(ext)]
    return s


def _load_rows():
    wb = load_workbook(EXCEL_FILE, data_only=True)
    try:
        ws = wb.active
        all_rows = list(ws.iter_rows(values_only=True))
    finally:
        wb.close()

    if not all_rows:
        return []
    columns = [_field_for_header(h) for h in all_rows[0]]
    if "xray" not in columns:
        raise ValueError("The Excel file needs a column named 'X-ray File'.")

    rows = []
    for raw in all_rows[1:]:
        row = {}
        for field, value in zip(columns, raw):
            if field and field not in row:
                row[field] = _fmt(value)
        if any(row.values()):
            rows.append(row)
    return rows


@router.get("/excel-lookup")
def excel_lookup(name: str = "", file: str = ""):
    fkey = _norm_file(file)
    if not fkey:
        return {"found": False, "message": "Please choose the X-ray image first."}

    if not os.path.isfile(EXCEL_FILE):
        return {"found": False,
                "message": "patients_data.xlsx was not found in the Backend folder."}

    try:
        rows = _load_rows()
    except Exception as e:
        return {"found": False, "message": f"Could not read patients_data.xlsx: {e}"}

    by_file = [r for r in rows if _norm_file(r.get("xray")) == fkey]
    if not by_file:
        return {"found": False,
                "message": f"'{file}' was not found in the X-ray File column of patients_data.xlsx."}

    nkey = _norm_name(name)
    if nkey:
        matches = [r for r in by_file if _norm_name(r.get("patient_name")) == nkey]
        if not matches:
            excel_name = by_file[0].get("patient_name") or "(no name)"
            return {"found": False,
                    "message": f"This X-ray is saved in the Excel under the name '{excel_name}', "
                               f"but you typed '{name.strip()}'. Please check the name."}
    else:
        matches = by_file

    row = matches[0]
    return {"found": True,
            "message": "Details auto-filled from patients_data.xlsx.",
            "data": {f: row.get(f, "") for f in FIELDS}}
    