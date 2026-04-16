#!/usr/bin/env python3
"""
STEP 3 — Package column names + synthetic examples for the AI tool  (AUTOMATED)
=============================================================================
PURPOSE : Reads columns.txt and synthetic_template.csv, then writes ai_input.txt
          — a structured text block you paste into the AI tool after ai_prompt.md.

INPUTS  : columns.txt            (from step1_extract_headers.sh)
          synthetic_template.csv  (filled in by you during Stage 2)
          context_config.txt      (your study context — edit once)

OUTPUT  : ai_input.txt           (paste this into the AI tool after the prompt)

PRIVACY : This script reads only the column names and YOUR synthetic values.
          It never reads your actual CSV data file.
=============================================================================
"""

import csv
import os
import re
import sys
import datetime

SCRIPT_DIR     = os.path.dirname(os.path.abspath(__file__))
COLUMNS_FILE   = os.path.join(SCRIPT_DIR, "columns.txt")
TEMPLATE_FILE  = os.path.join(SCRIPT_DIR, "synthetic_template.csv")
CONTEXT_FILE   = os.path.join(SCRIPT_DIR, "context_config.txt")
RESOURCE_FILE  = os.path.join(SCRIPT_DIR, "resource_doc.txt")   # optional
OUTPUT_FILE    = os.path.join(SCRIPT_DIR, "ai_input.txt")

# ── Validate inputs ───────────────────────────────────────────────────────────
missing = []
for path, name in [(COLUMNS_FILE, "columns.txt"),
                   (TEMPLATE_FILE, "synthetic_template.csv"),
                   (CONTEXT_FILE,  "context_config.txt")]:
    if not os.path.exists(path):
        missing.append(name)

has_resource = os.path.exists(RESOURCE_FILE)
if missing:
    print("ERROR: Missing required files:")
    for m in missing:
        print(f"  • {m}")
    print()
    print("Please complete the earlier steps before running this script.")
    sys.exit(1)

# ── Read columns ──────────────────────────────────────────────────────────────
with open(COLUMNS_FILE, "r") as f:
    raw_lines = [l.strip() for l in f if l.strip()]

columns = []
for line in raw_lines:
    match = re.match(r"^\s*\d+\.\s*(.+)$", line)
    columns.append(match.group(1) if match else line)

n_cols = len(columns)

# ── Read synthetic template ───────────────────────────────────────────────────
with open(TEMPLATE_FILE, "r", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header_row  = next(reader, [])
    example_row = next(reader, [])

# Validate header matches columns
if len(header_row) != n_cols:
    print(f"WARNING: synthetic_template.csv has {len(header_row)} columns "
          f"but columns.txt has {n_cols}. Proceeding with available data.")

# Build {column_name: example_value} mapping
example_map = {}
for col, val in zip(header_row, example_row):
    example_map[col] = val.strip() if val.strip() else "—"

# Check for unfilled columns
unfilled = [c for c in columns if not example_map.get(c, "").replace("—","")]
if unfilled:
    print(f"WARNING: {len(unfilled)} columns have no synthetic example value:")
    for c in unfilled[:10]:
        print(f"  • {c}")
    if len(unfilled) > 10:
        print(f"  ... and {len(unfilled)-10} more")
    print()
    print("Consider going back to synthetic_template.csv and filling these in.")
    print("Continuing anyway — AI will still generate descriptions.")
    print()

# ── Read context config ───────────────────────────────────────────────────────
with open(CONTEXT_FILE, "r") as f:
    context_raw = f.read()

# Strip comment lines
context_lines = [l for l in context_raw.splitlines()
                 if not l.startswith("#")]
context_text = "\n".join(context_lines).strip()

# ── Build ai_input.txt ────────────────────────────────────────────────────────
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
divider = "=" * 70

lines = [
    divider,
    "AI INPUT PACKAGE — DATA DICTIONARY PIPELINE",
    f"Generated: {now}",
    f"Column count: {n_cols}",
    divider,
    "",
    "── STUDY CONTEXT ──────────────────────────────────────────────────────",
    context_text,
    "",
    "── COLUMNS WITH SYNTHETIC EXAMPLE VALUES ──────────────────────────────",
    f"(Total: {n_cols} columns)",
    "",
]

for i, col in enumerate(columns, 1):
    ex = example_map.get(col, "—")
    lines.append(f"  {i:>4}. {col}  |  Example: {ex}")

lines += [""]

# ── Optional resource document ────────────────────────────────────────────────
if has_resource:
    with open(RESOURCE_FILE, "r", encoding="utf-8") as f:
        resource_text = f.read().strip()
    resource_char_count = len(resource_text)
    lines += [
        "── REFERENCE DOCUMENT FOR VARIABLE DESCRIPTIONS ───────────────────",
        f"(Provided by user to inform data label definitions; {resource_char_count:,} characters)",
        "The AI should use this document when writing the 'description' field.",
        "",
        resource_text,
        "",
    ]
    print(f"   Resource document included: {resource_char_count:,} characters from resource_doc.txt")
else:
    lines += [
        "── REFERENCE DOCUMENT ─────────────────────────────────────────────",
        "(No resource document provided. Run step2b_add_resource_doc.py to add one.)",
        "(The AI will rely on its built-in clinical knowledge for descriptions.)",
        "",
    ]
    print("   No resource_doc.txt found — AI will use built-in knowledge only.")

lines += [
    divider,
    "END OF AI INPUT",
    divider,
]

output_text = "\n".join(lines)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(output_text)

# ── Print summary ─────────────────────────────────────────────────────────────
print(f"✅  Packaged {n_cols} columns → {OUTPUT_FILE}")
print(f"   Unfilled synthetic examples: {len(unfilled)}")
print()
print("──────────────────────────────────────────────────────────────────")
print("NEXT STEP (Stage 4 — Manual):")
print("──────────────────────────────────────────────────────────────────")
print()
print("1. Open ai_prompt.md and read the capability requirements at the top")
print("   to confirm your chosen AI tool meets them.")
print()
print("2. In your AI tool, start a new conversation and paste:")
print("   a) The ENTIRE contents of ai_prompt.md")
print("   b) Immediately followed by the ENTIRE contents of ai_input.txt")
print()
print("3. Wait for the AI to respond with a JSON array.")
print()
print("4. Copy the AI's ENTIRE response and save it as:  ai_output.json")
print("   (The file must contain only the JSON — no extra text.)")
print("   Tip: If the AI wraps the JSON in ```json ... ``` fences,")
print("        include those — the formatter will strip them automatically.")
print()
print("5. Then run:  python3 step5_format_output.py")
print()
