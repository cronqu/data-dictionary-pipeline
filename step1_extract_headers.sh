#!/usr/bin/env bash
# =============================================================================
# STEP 1 — Extract column names only (MANUAL step, run on your local machine)
# =============================================================================
# PURPOSE : Pull ONLY the header row from your CSV — zero patient data is read.
# OUTPUT  : columns.txt  (numbered list of column names)
# NEXT    : Run step2_make_template.py to create your synthetic data template.
#
# USAGE:
#   bash step1_extract_headers.sh path/to/your_data.csv
#   bash step1_extract_headers.sh path/to/your_data.csv --sep ";"   # for semicolon-delimited
#
# PRIVACY NOTE:
#   This script reads ONLY line 1 (the header row) of your CSV.
#   No patient data, no row values, nothing sensitive is captured.
#   The output file columns.txt contains column names only.
# =============================================================================

set -euo pipefail

# ── Parse arguments ───────────────────────────────────────────────────────────
CSV_FILE="${1:-}"
SEP="${3:-,}"    # default comma; override with --sep argument

if [[ -z "$CSV_FILE" ]]; then
    echo "ERROR: Please provide the path to your CSV file."
    echo ""
    echo "Usage:"
    echo "  bash step1_extract_headers.sh path/to/your_data.csv"
    echo "  bash step1_extract_headers.sh path/to/your_data.csv --sep \";\""
    exit 1
fi

if [[ ! -f "$CSV_FILE" ]]; then
    echo "ERROR: File not found: $CSV_FILE"
    exit 1
fi

# Handle --sep flag
if [[ "${2:-}" == "--sep" ]]; then
    SEP="${3:-,}"
fi

# ── Determine output location (same dir as this script) ───────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT="$SCRIPT_DIR/columns.txt"

# ── Extract header only (head -1 reads ONE line) ──────────────────────────────
echo "Reading header from: $CSV_FILE"
echo "Separator: '$SEP'"
echo ""

# Read line 1, split on separator, number each column
head -1 "$CSV_FILE" | tr "$SEP" '\n' | \
    awk '{printf "%4d. %s\n", NR, $0}' > "$OUTPUT"

COL_COUNT=$(wc -l < "$OUTPUT" | tr -d ' ')

echo "✅  Extracted $COL_COUNT column names → $OUTPUT"
echo ""
echo "Column names extracted (first 10 shown):"
head -10 "$OUTPUT"
if [[ "$COL_COUNT" -gt 10 ]]; then
    echo "    ... ($((COL_COUNT - 10)) more)"
fi
echo ""
echo "──────────────────────────────────────────────────────────────────"
echo "PRIVACY CHECK:"
echo "  ✅  Only column names were read (line 1 of the CSV)"
echo "  ✅  No patient data was captured"
echo "  ✅  Saved to: $OUTPUT"
echo "──────────────────────────────────────────────────────────────────"
echo ""
echo "NEXT STEP:"
echo "  Run:  python3 step2_make_template.py"
echo "  This will create synthetic_template.csv for you to fill in."
echo ""
