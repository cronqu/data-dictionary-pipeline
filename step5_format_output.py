#!/usr/bin/env python3
"""
STEP 5 — Format AI JSON output into a styled xlsx data dictionary  (AUTOMATED)
=============================================================================
PURPOSE : Reads the AI's JSON response (ai_output.json) and writes a
          professional, formatted Excel workbook (data_dictionary.xlsx).

INPUTS  : ai_output.json          (paste the AI's full response into this file)
          synthetic_template.csv  (used to pull the synthetic example values)

OUTPUT  : data_dictionary.xlsx    (open and review in Stage 6)

STYLING : Matches the structure and color-coding of the reference Pixalere
          data dictionary (Pix data_descriptions.xlsx).

PRIVACY : This script NEVER reads your real CSV. It only reads the AI's output
          and your synthetic template.
=============================================================================
"""

import csv
import json
import os
import re
import sys
import datetime

try:
    import openpyxl
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
except ImportError:
    print("ERROR: openpyxl is not installed.")
    print("Install it with:  pip3 install openpyxl")
    sys.exit(1)

SCRIPT_DIR     = os.path.dirname(os.path.abspath(__file__))
AI_OUTPUT_FILE = os.path.join(SCRIPT_DIR, "ai_output.json")
TEMPLATE_FILE  = os.path.join(SCRIPT_DIR, "synthetic_template.csv")
OUTPUT_FILE    = os.path.join(SCRIPT_DIR, "data_dictionary.xlsx")

# ── Validate inputs ───────────────────────────────────────────────────────────
if not os.path.exists(AI_OUTPUT_FILE):
    print("ERROR: ai_output.json not found.")
    print("Please paste the AI's JSON response into ai_output.json and rerun.")
    sys.exit(1)

# ── Parse AI output ───────────────────────────────────────────────────────────
with open(AI_OUTPUT_FILE, "r", encoding="utf-8") as f:
    raw = f.read().strip()

# Strip markdown code fences if present (```json ... ```)
raw = re.sub(r"^```json\s*", "", raw, flags=re.IGNORECASE)
raw = re.sub(r"^```\s*", "", raw)
raw = re.sub(r"\s*```$", "", raw)
raw = raw.strip()

try:
    records = json.loads(raw)
except json.JSONDecodeError as e:
    print(f"ERROR: Could not parse ai_output.json as JSON.")
    print(f"JSON error: {e}")
    print()
    print("Tips:")
    print("  • Make sure you copied the AI's COMPLETE response")
    print("  • The file should contain only the JSON array (starting with '[')")
    print("  • If the AI wrapped it in ```json ... ``` that's fine — we strip those")
    sys.exit(1)

if not isinstance(records, list):
    print("ERROR: ai_output.json should contain a JSON array (starting with '[').")
    sys.exit(1)

n = len(records)
print(f"Parsed {n} records from ai_output.json")

# ── Required fields ───────────────────────────────────────────────────────────
REQUIRED_KEYS = {"field", "data_type", "source_table", "source_system",
                 "code_desc_pair", "description"}

issues = []
for i, rec in enumerate(records):
    missing = REQUIRED_KEYS - set(rec.keys())
    if missing:
        issues.append(f"  Record {i+1} ({rec.get('field','?')}): missing keys {missing}")
if issues:
    print(f"\nWARNING: {len(issues)} records have missing keys:")
    for msg in issues[:10]:
        print(msg)
    if len(issues) > 10:
        print(f"  ... and {len(issues)-10} more")
    print("\nContinuing — missing fields will be shown as '[MISSING]' in the xlsx.\n")

# ── Read synthetic example values ─────────────────────────────────────────────
example_map = {}
if os.path.exists(TEMPLATE_FILE):
    with open(TEMPLATE_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header_row  = next(reader, [])
        example_row = next(reader, [])
    for col, val in zip(header_row, example_row):
        example_map[col] = val.strip() if val.strip() else "—"
else:
    print("WARNING: synthetic_template.csv not found. Example values will be blank.")

# ── Color palette by source table ─────────────────────────────────────────────
section_fills = {
    "A01": PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid"),  # green
    "A02": PatternFill(start_color="F2DCDB", end_color="F2DCDB", fill_type="solid"),  # pink
    "A03": PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid"),  # light orange
    "A04": PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid"),
    "A05": PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid"),  # yellow
    "A06": PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid"),
    "A08": PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid"),
    "A09": PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid"),
    "B01": PatternFill(start_color="D9E2F3", end_color="D9E2F3", fill_type="solid"),  # light blue
    "B02": PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid"),  # orange
    "B03": PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid"),  # blue
    "B05": PatternFill(start_color="DAEEF3", end_color="DAEEF3", fill_type="solid"),  # teal
    "B06": PatternFill(start_color="D6E4F0", end_color="D6E4F0", fill_type="solid"),
    "B08": PatternFill(start_color="E2D9F3", end_color="E2D9F3", fill_type="solid"),  # purple
    "B09": PatternFill(start_color="E2D9F3", end_color="E2D9F3", fill_type="solid"),
    "B10": PatternFill(start_color="E2D9F3", end_color="E2D9F3", fill_type="solid"),
    "B13": PatternFill(start_color="D9F0DA", end_color="D9F0DA", fill_type="solid"),  # mint
    "B16": PatternFill(start_color="D9F0DA", end_color="D9F0DA", fill_type="solid"),
    "B17": PatternFill(start_color="D9F0DA", end_color="D9F0DA", fill_type="solid"),
    "RAI": PatternFill(start_color="EAD1DC", end_color="EAD1DC", fill_type="solid"),  # rose
    "Pixalere (ax)": PatternFill(start_color="FDE9D9", end_color="FDE9D9", fill_type="solid"),  # peach
    "Pixalere (wp)": PatternFill(start_color="FDE9D9", end_color="FDE9D9", fill_type="solid"),
}

# ── Build workbook ────────────────────────────────────────────────────────────
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Data Descriptions"

# Styling constants
header_font  = Font(bold=True, size=11, color="FFFFFF")
header_fill  = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
data_font    = Font(size=10)
thin_border  = Border(
    left=Side(style="thin"), right=Side(style="thin"),
    top=Side(style="thin"),  bottom=Side(style="thin"),
)

HEADER_LABELS = [
    "Field",
    "Example Value (Synthetic)",
    "PARIS Source Table",
    "Data Type",
    "Source System",
    "Code/Desc Pair",
    "Description & Comments",
]

# Write header row
for col_idx, label in enumerate(HEADER_LABELS, 1):
    cell = ws.cell(row=1, column=col_idx, value=label)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = thin_border

# Write data rows
for row_idx, rec in enumerate(records, 2):
    field       = rec.get("field", "[MISSING]")
    data_type   = rec.get("data_type", "[MISSING]")
    source_tbl  = rec.get("source_table", "—")
    source_sys  = rec.get("source_system", "—")
    pair        = rec.get("code_desc_pair", "—")
    description = rec.get("description", "[MISSING]")
    example_val = example_map.get(field, "—")

    values = [field, example_val, source_tbl, data_type, source_sys, pair, description]

    # Determine row fill from source_table
    row_fill = None
    for key in [source_tbl, source_tbl.split()[0] if source_tbl else ""]:
        if key in section_fills:
            row_fill = section_fills[key]
            break

    for col_idx, val in enumerate(values, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.font = data_font
        cell.alignment = Alignment(vertical="top", wrap_text=True)
        cell.border = thin_border
        # Apply section color to first 2 cols (Field + Example)
        if row_fill and col_idx <= 2:
            cell.fill = row_fill

# Column widths
ws.column_dimensions["A"].width = 32
ws.column_dimensions["B"].width = 38
ws.column_dimensions["C"].width = 18
ws.column_dimensions["D"].width = 22
ws.column_dimensions["E"].width = 14
ws.column_dimensions["F"].width = 26
ws.column_dimensions["G"].width = 85

ws.freeze_panes = "A2"
ws.sheet_view.showGridLines = True

# ── Summary sheet ─────────────────────────────────────────────────────────────
ws2 = wb.create_sheet("Summary")
bold = Font(bold=True)
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

summary_rows = [
    ("File described:", "exported_data.csv"),
    ("Data dictionary generated:", now_str),
    ("Total columns described:", n),
    ("", ""),
    ("PRIVACY NOTE:", "Synthetic example values only — no real patient data included."),
    ("", ""),
    ("Source Table Legend:", ""),
    ("A01", "Demographics (study_id, birth_dt, Deceased, Gender)"),
    ("A02", "Relationships (Association Code, Association Desc)"),
    ("A03", "Alerts (Alert Code/Desc, Extended Leave)"),
    ("A04", "Allergies (Substance Type, Reaction Type)"),
    ("A05", "Funding Source (Funding Type/Detail, income assistance)"),
    ("A06", "Marital Status"),
    ("A08", "Address (Address Type, postal code / FSA)"),
    ("A09", "Language (Language Code, Interpreter Required)"),
    ("B01", "Referrals (reason, source role, department, discharge)"),
    ("B02", "Allocations (staff allocation type, dates)"),
    ("B03", "Assessments (assessment type, staff, start/completed)"),
    ("B05", "CCP — Clinical Care Plan (need, goal, intervention, discipline)"),
    ("B06", "Diagnosis (diagnosis type, recording team)"),
    ("B08", "Immunization History (antigen, dose, tradename, status)"),
    ("B09", "Weight & Growth"),
    ("B10", "Vital Signs (respirations, temperature, BP)"),
    ("B13", "Risk Screen (environmental, musculoskeletal, violence, occupational)"),
    ("B16", "Plan (intervention type, provider, dates)"),
    ("B17", "HSO — Home Support (type, provider, authorized hours)"),
    ("RAI", "RAI-HC Assessment (IADL, ADL scales, H1/H2 items)"),
    ("Pixalere (wp)", "Wound Profile table (alpha_id, etiology, goal_of_care)"),
    ("Pixalere (ax)", "Assessment Structured table (visited_on, status, wound fields)"),
    ("Derived / —", "Computed variable or target label"),
]

for row_idx, (key, val) in enumerate(summary_rows, 1):
    c1 = ws2.cell(row=row_idx, column=1, value=key)
    c2 = ws2.cell(row=row_idx, column=2, value=val)
    if key and not str(val).startswith("(") and row_idx <= 7:
        c1.font = bold
    if key in section_fills:
        c1.fill = section_fills[key]

ws2.column_dimensions["A"].width = 22
ws2.column_dimensions["B"].width = 85

# ── Save ──────────────────────────────────────────────────────────────────────
wb.save(OUTPUT_FILE)
print(f"✅  Saved: {OUTPUT_FILE}")
print(f"   {n} rows | 7 columns | color-coded by source table")
print()
print("──────────────────────────────────────────────────────────────────")
print("NEXT STEP (Stage 6 — Manual):")
print("──────────────────────────────────────────────────────────────────")
print()
print("1. Open data_dictionary.xlsx")
print("2. Review all descriptions — correct any errors or gaps the AI made")
print("3. Check the 'Code/Desc Pair' column for any missed linkages")
print("4. Add any custom notes in the 'Description & Comments' column")
print("5. Save the final file")
print()
print("Your data dictionary is complete! ✅")
print()
