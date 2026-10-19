"""
Run this from inside your Backend folder:
    cd Backend
    python create_excel.py

Creates patients_data.xlsx with 15 patients that use YOUR real X-ray file
names (normal x ray 1.jpg, pn1.jpg ... pn6.jpg, img1.png ... etc).

Safety: if patients_data.xlsx already exists and has data, it is NOT changed.
"""
import os

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Font, PatternFill, Alignment
except ImportError:
    print("openpyxl is not installed. Run this first:  pip install openpyxl")
    raise SystemExit(1)

FILE_NAME = "patients_data .xlsx"

if os.path.isfile(FILE_NAME) and os.path.getsize(FILE_NAME) > 0:
    try:
        wb_check = load_workbook(FILE_NAME)
        has_rows = wb_check.active.max_row > 1
        wb_check.close()
    except Exception:
        has_rows = False
    if has_rows:
        print(f"'{FILE_NAME}' already exists and has data. Nothing was changed.")
        print("To rebuild it, delete the file first:  del patients_data.xlsx")
        raise SystemExit(0)

wb = Workbook()
ws = wb.active
ws.title = "Patients"

headers = ["Patient Name", "Age", "Gender", "X-ray File",
           "WBC (cells/uL)", "RBC (mill/uL)", "Platelets (x10^3/uL)",
           "Hemoglobin (g/dL)", "Temperature (F)", "SpO2 (%)",
           "Pulse Rate (bpm)", "CRP (mg/L)"]

rows = [
    # --- Normal ---
    ["Meera Iyer", 22, "Female", "normal x ray 1.jpg", 7100, 4.9, 290, 13.6, 98.3, 98, 70, 3],
    ["Rohit Verma", 30, "Male", "normal2.jpeg", 6800, 5.0, 275, 14.1, 98.6, 99, 72, 2.5],
    ["Aarti Shinde", 27, "Female", "Normal3.jpg", 8600, 4.7, 260, 12.7, 98.8, 96, 80, 6],
    ["John Carter", 34, "Male", "patient1.png", 8200, 4.8, 250, 13.5, 98.6, 97, 78, 4.5],
    ["Lakshmi Menon", 29, "Female", "lung.jpg", 7400, 4.8, 265, 13.2, 98.5, 97, 76, 3.8],
    # --- Mild / Non-Severe Pneumonia (NSCAP) ---
    ["Anjali Deshpande", 31, "Female", "pn1.jpg", 9800, 4.6, 245, 12.9, 99.4, 95, 88, 15],
    ["Ganesh Nair", 45, "Male", "pn2.jpg", 10900, 4.5, 210, 13.1, 100.0, 93, 92, 28],
    ["Kavita Joshi", 38, "Female", "pn3.jpg", 10200, 4.6, 230, 12.6, 99.6, 94, 90, 35],
    ["Priya Sharma", 45, "Female", "img1.png", 11800, 4.5, 310, 12.8, 100.4, 92, 96, 60],
    ["Neha Kulkarni", 26, "Female", "img2.jpg", 10500, 4.6, 240, 12.9, 99.8, 94, 88, 32],
    # --- Severe Pneumonia (SCAP) ---
    ["Suresh Kadam", 58, "Male", "pn4.jpg", 14500, 4.1, 175, 11.2, 102.1, 88, 118, 92],
    ["Amit Deshmukh", 61, "Male", "pn5.jpg", 13800, 3.9, 150, 10.8, 103.5, 85, 122, 110],
    ["Farida Khan", 67, "Female", "pn6.jpg", 15200, 3.8, 140, 10.4, 104.0, 84, 128, 130],
    ["Vikram Singh", 47, "Male", "img3.jpg", 14200, 4.0, 155, 10.9, 103.0, 86, 120, 95],
    ["Sunita Rao", 50, "Female", "img4.png", 13500, 3.9, 160, 10.6, 102.8, 87, 119, 100],
]

ws.append(headers)
for r in rows:
    ws.append(r)

for c in ws[1]:
    c.font = Font(bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor="0EA5E9")
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws.row_dimensions[1].height = 32
for col, w in zip("ABCDEFGHIJKL", [20, 7, 10, 22, 16, 16, 20, 18, 17, 10, 17, 12]):
    ws.column_dimensions[col].width = w
ws.freeze_panes = "A2"

GREEN = PatternFill("solid", fgColor="DCFCE7")
YELLOW = PatternFill("solid", fgColor="FEF3C7")
RED = PatternFill("solid", fgColor="FEE2E2")
for row_number, fill in enumerate([GREEN] * 5 + [YELLOW] * 5 + [RED] * 5, start=2):
    for cell in ws[row_number]:
        cell.fill = fill

wb.save(FILE_NAME)
print(f"'{FILE_NAME}' created with {len(rows)} patients (5 Normal, 5 Mild, 5 Severe).")
print("Now restart the server:  uvicorn main:app --reload")