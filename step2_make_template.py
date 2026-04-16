#!/usr/bin/env python3
"""
STEP 2 — Generate the synthetic data template  (AUTOMATED helper for Stage 2)
=============================================================================
PURPOSE : Reads columns.txt (produced by step1) and creates synthetic_template.csv
          — a two-row CSV with column headers on row 1 and EMPTY cells on row 2.

OUTPUT  : synthetic_template.csv   (open in Excel/Numbers/Google Sheets to fill in)

NEXT    : Manually open synthetic_template.csv and type ONE fake example value
          for every column. Values must LOOK like the real data format but must
          NOT be real patient data.  Then run step3_package_for_ai.py.

PRIVACY : This script only reads columns.txt (column names). It never reads your
          actual CSV data file.
=============================================================================
"""

import csv
import os
import sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
COLUMNS_FILE = os.path.join(SCRIPT_DIR, "columns.txt")
OUTPUT_FILE  = os.path.join(SCRIPT_DIR, "synthetic_template.csv")

# ── Read columns.txt ──────────────────────────────────────────────────────────
if not os.path.exists(COLUMNS_FILE):
    print("ERROR: columns.txt not found.")
    print("Please run step1_extract_headers.sh first to generate it.")
    sys.exit(1)

with open(COLUMNS_FILE, "r") as f:
    raw_lines = [l.strip() for l in f if l.strip()]

# Lines are formatted as "   1. column_name" — strip the number prefix
columns = []
for line in raw_lines:
    # Remove leading number and dot: "   1. study_id" → "study_id"
    match = re.match(r"^\s*\d+\.\s*(.+)$", line)
    if match:
        columns.append(match.group(1))
    else:
        columns.append(line)  # fallback: use line as-is

n = len(columns)
print(f"Found {n} columns in columns.txt")

# ── Build the CSV ─────────────────────────────────────────────────────────────
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)          # Row 1: headers
    writer.writerow([""] * n)         # Row 2: blank — user fills these in

print(f"✅  Created: {OUTPUT_FILE}")
print()
print("──────────────────────────────────────────────────────────────────")
print("MANUAL ACTION REQUIRED (Stage 2):")
print("──────────────────────────────────────────────────────────────────")
print()
print("1. Open synthetic_template.csv in Excel, Numbers, or Google Sheets")
print("2. Fill in Row 2 with ONE fake example value per column")
print()
print("GUIDELINES for writing good synthetic values:")
print("  • Match the FORMAT of the real data (e.g., date → '1955-03', not 'May 1955')")
print("  • Match the DATA TYPE (numbers as numbers, codes as codes)")
print("  • Use realistic but entirely fictional values")
print("  • For IDs: use a clearly fake number (e.g., 9999, 0000)")
print("  • For dates: use a plausible but non-specific date (e.g., '1955-03')")
print("  • For codes: use a value that exists in the codebook (e.g., 'F' for gender)")
print("  • For free text: write a generic clinical phrase")
print("  • For binary Y/N: write 'N' or 'Y'")
print("  • For NULL/missing fields: leave blank or write 'NaN'")
print()
print("EXAMPLES by data type:")
print("  Numeric ID        →  9999")
print("  Date (YYYY-MM)    →  1955-03")
print("  Date (YYYY-MM-DD) →  2020-06-15")
print("  Postal code FSA   →  V0A")
print("  Gender code       →  F")
print("  Boolean/Binary    →  N")
print("  Immunization age  →  72 yr 4 m")
print("  Clinical text     →  To Heal the Wound")
print("  Wound location    →  Left Ankle/Foot")
print()
print("3. Save synthetic_template.csv (keep as CSV, not xlsx)")
print()
print("NEXT STEP:")
print("  Run:  python3 step3_package_for_ai.py")
print()
