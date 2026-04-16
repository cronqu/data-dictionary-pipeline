# Data Dictionary Pipeline — Privacy-Safe Workflow

Generate a professional data dictionary for any health dataset **without
exposing real patient data to any AI tool**.

See **`pipeline_architecture.png`** for a visual overview of all stages.

---

## What this pipeline produces

A formatted Excel workbook (`data_dictionary.xlsx`) describing every column
in your CSV — data types, source tables, clinical descriptions, and Code↔Desc
linkages — structured identically to the reference Pixalere data dictionary.

---

## Prerequisites

| Requirement | Check |
|-------------|-------|
| macOS / Linux terminal (bash) | `bash --version` |
| Python 3.8 or later | `python3 --version` |
| openpyxl Python package | `pip3 install openpyxl` |
| matplotlib Python package | `pip3 install matplotlib` |
| An AI tool meeting the capability requirements in `ai_prompt.md` | See prompt |

---

## File inventory

```
pipeline/
├── README.md                      ← You are here
├── pipeline_architecture.png      ← Visual figure (run generate_figure.py)
│
├── step1_extract_headers.sh       ← STAGE 1 script (bash)
├── step2_make_template.py         ← STAGE 2 helper (Python)
├── step2b_add_resource_doc.py     ← STAGE 2b script (Python) — attach reference doc
├── step3_package_for_ai.py        ← STAGE 3 script (Python)
├── ai_prompt.md                   ← STAGE 4 prompt (paste into AI tool)
├── step5_format_output.py         ← STAGE 5 script (Python)
│
├── context_config.txt             ← Edit ONCE with your study description
│
│   ── Files produced during the pipeline run ──
├── columns.txt                    ← Output of Stage 1
├── synthetic_template.csv         ← Output of Step 2 helper; YOU fill in Stage 2
├── resource_doc.txt               ← Output of Stage 2b (optional but recommended)
├── ai_input.txt                   ← Output of Stage 3
├── ai_output.json                 ← YOU paste AI response here (Stage 4 → 5)
└── data_dictionary.xlsx           ← Final output (Stage 5 → review in Stage 6)
```

---

## Quick-start walkthrough

### Before you begin — one-time setup

1. Open **`context_config.txt`** and update the study name and context
   paragraph to describe your specific dataset. Keep it to 2–5 sentences.
   Do NOT include patient names, IDs, or real data values.

2. Generate the architecture figure (optional but recommended for first-time users):
   ```bash
   python3 generate_figure.py
   ```
   Open `pipeline_architecture.png` to orient yourself before starting.

---

### 🔴 STAGE 1 — Extract column names only (MANUAL)

**Goal:** Pull the header row from your real CSV — and ONLY the header row.
No patient data is read or stored.

```bash
cd /path/to/pipeline
bash step1_extract_headers.sh /path/to/your_data.csv
```

For semicolon-delimited files:
```bash
bash step1_extract_headers.sh /path/to/your_data.csv --sep ";"
```

**Output:** `columns.txt` — a numbered list of column names.

✅ Privacy checkpoint: open `columns.txt` and confirm it contains only
   column names (no dates, IDs, or clinical values).

---

### 🔴 STAGE 2 — Create synthetic example values (MANUAL)

**Goal:** Produce one fake-but-realistic example value for each column.
You supply these using your own domain knowledge — no AI is involved.

**Step 2a:** Generate the template file:
```bash
python3 step2_make_template.py
```
This creates `synthetic_template.csv` with your column headers on Row 1
and empty cells on Row 2.

**Step 2b:** Open `synthetic_template.csv` in Excel, Numbers, or Google
Sheets and fill in Row 2. Guidelines printed by the script; key rules:

| Data type | Good synthetic value | Bad (too real) |
|-----------|---------------------|----------------|
| Numeric ID | `9999` | `1433` (real patient ID) |
| Date YYYY-MM | `1955-03` | `1929-01` (real birth year) |
| Date YYYY-MM-DD | `2020-06-15` | actual assessment date |
| Postal code FSA | `V0A` | `V6S` (real area) |
| Gender code | `F` | ✅ OK (just a category) |
| Clinical text | `To Heal the Wound` | ✅ OK (generic label) |
| Binary Y/N | `N` | ✅ OK |

**Step 2c:** Save `synthetic_template.csv` as CSV (not xlsx).

---

### 🔵 STAGE 2b — Attach a resource document (AUTOMATED + optional but recommended)

**Goal:** Give the AI tool a reference document — such as a data dictionary, codebook,
clinical annotation guide, or any descriptive document — to use when writing variable
descriptions. This is the key step that was done manually in the original pipeline
(pulling definitions from the PARIS categories Word document and Pixalere xlsx).

**This step is optional but strongly recommended** for more accurate, domain-specific
descriptions in the final data dictionary.

**Supported document formats** (any of the following):
- Word document (`.docx`) — including embedded comments
- Excel workbook (`.xlsx`) — all sheets are extracted
- PDF (`.pdf`) — text is extracted page by page
- CSV (`.csv`) — all rows extracted as plain text
- Plain text or Markdown (`.txt`, `.md`)

> **Not restricted to any specific format.** If your reference document is in
> another format (e.g., `.odt`, `.rtf`, `.pptx`), use your word processor's
> "Save As" to convert it to `.docx` or `.txt` first.

**Examples of suitable resource documents:**
- A data dictionary from your data provider (e.g., a VCH data guide)
- A clinical codebook describing variable labels and value sets
- An annotation guide with comment text (e.g., the PARIS categories document)
- A RAI-HC assessment manual
- Any document containing variable descriptions, code definitions, or clinical context

```bash
# Word document (also extracts embedded comments):
python3 step2b_add_resource_doc.py path/to/PARIS_categories.docx

# Excel workbook:
python3 step2b_add_resource_doc.py path/to/Pix_data_descriptions.xlsx

# PDF:
python3 step2b_add_resource_doc.py path/to/RAI_manual.pdf

# Plain text:
python3 step2b_add_resource_doc.py path/to/codebook.txt

# CSV:
python3 step2b_add_resource_doc.py path/to/variable_labels.csv
```

**Output:** `resource_doc.txt` — open and review it to confirm it contains
definitions (not patient data) before proceeding.

> **Privacy note:** The resource document should contain variable definitions,
> code labels, and clinical descriptions only — **not** patient records.
> The script never reads your actual data CSV.

---

### 🔵 STAGE 3 — Package for AI (AUTOMATED)

```bash
python3 step3_package_for_ai.py
```

Reads `columns.txt` + `synthetic_template.csv` + `context_config.txt`
and writes `ai_input.txt` — a structured text block ready to paste into
your AI tool.

---

### 🔴 STAGE 4 — Run the AI prompt (MANUAL)

**Capability requirements** (check `ai_prompt.md` for full list):
- Knowledge cutoff 2023+
- Outputs valid JSON arrays without truncation
- Healthcare / clinical knowledge (ICD, RAI, nursing terminology)
- Context window ≥ 8,000 tokens (~105 columns); scale up for larger datasets

**Steps:**

1. Open your AI tool and start a **new conversation**.

2. Paste the **entire contents of `ai_prompt.md`** into the message field.

3. Immediately after, paste the **entire contents of `ai_input.txt`**.

4. Send the message and wait for the AI's response.

5. The AI should return a **JSON array** (one object per column).
   If it truncates, ask it to continue: *"Please continue from where you
   left off and complete the remaining columns in the same JSON format."*

6. Copy the **complete JSON response** and save it as **`ai_output.json`**
   in the pipeline folder.
   - Include the ```json fences if present — they are stripped automatically.
   - The file must contain a complete, valid JSON array starting with `[`.

---

### 🔵 STAGE 5 — Format output into xlsx (AUTOMATED)

```bash
python3 step5_format_output.py
```

Reads `ai_output.json` and `synthetic_template.csv`, then writes
`data_dictionary.xlsx` with:
- 7 columns (Field, Example Value, PARIS Source Table, Data Type,
  Source System, Code/Desc Pair, Description & Comments)
- Color-coded rows by source table section
- Frozen header row, wrapped text, calibrated column widths
- Summary sheet with source table legend

---

### 🔴 STAGE 6 — Review and finalize (MANUAL)

1. Open `data_dictionary.xlsx`.
2. Read through all AI-generated descriptions — correct any errors.
3. Check the **Code/Desc Pair** column for any missed linkages.
4. Add custom notes or caveats in the **Description & Comments** column.
5. Save the final file.

Your data dictionary is complete ✅

---

## Troubleshooting

### `columns.txt not found`
Run `step1_extract_headers.sh` first.

### `synthetic_template.csv has X columns but columns.txt has Y`
The template was generated from an older `columns.txt`. Re-run
`step2_make_template.py` after any changes to `columns.txt`.

### JSON parse error in Step 5
- Make sure `ai_output.json` contains only the JSON (starting with `[`)
- If the AI stopped mid-array, ask it to continue and append the rest
- Validate the JSON at https://jsonlint.com (paste without real data)

### AI truncated the output
Ask: *"You stopped before completing all columns. Please continue the
JSON array from column N onwards, maintaining the same format."*
Then manually merge the two JSON arrays before saving to `ai_output.json`.

### Colors/styling wrong in xlsx
Ensure openpyxl ≥ 3.0 is installed: `pip3 install --upgrade openpyxl`

---

## Privacy summary

| Stage | What the AI sees | Real data exposed? |
|-------|-----------------|-------------------|
| 1 | Nothing | ❌ No |
| 2 | Nothing | ❌ No |
| 3 | Nothing | ❌ No |
| 4 | Column names + YOUR synthetic values | ❌ No |
| 5 | AI's own output only | ❌ No |
| 6 | Nothing | ❌ No |

**Your real CSV never leaves your machine and is never read by any AI tool.**

---

## Adapting for a different dataset

1. Update `context_config.txt` with your study details.
2. Run the pipeline from Stage 1.
3. Optionally edit `ai_prompt.md` — update the PARIS table reference card
   or Pixalere field reference if your data source uses different tables.

The pipeline is designed to work for any tabular health dataset, not just
PARIS/Pixalere data. The AI prompt's reference cards can be replaced with
documentation relevant to any EMR or data system.
