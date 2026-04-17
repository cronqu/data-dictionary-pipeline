# Data Dictionary Pipeline — Privacy-Safe Workflow

Generate a professional data dictionary for any tabular dataset **without
exposing real data records to any AI tool**.

See **`pipeline_architecture.png`** for a visual overview of all stages.

---

## What this pipeline produces

A formatted Excel workbook (`data_dictionary.xlsx`) describing every column
in your dataset — data types, source tables, descriptions, and Code↔Description
column linkages — structured as a 7-column data dictionary table.

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
├── pipeline_architecture.png      ← Visual figure (run generate_figure.py to rebuild)
│
├── step1_extract_headers.sh       ← STAGE 1  script (bash)
├── step2_make_template.py         ← STAGE 2  helper (Python)
├── step2b_add_resource_doc.py     ← STAGE 2b script (Python) — attach reference document
├── step3_package_for_ai.py        ← STAGE 3  script (Python)
├── ai_prompt.md                   ← STAGE 4  prompt (paste into AI tool)
├── step5_format_output.py         ← STAGE 5  script (Python)
│
├── context_config.txt             ← Edit once with your study/dataset description
│
│   ── Files produced during the pipeline run (not committed to git) ──
├── columns.txt                    ← Output of Stage 1
├── synthetic_template.csv         ← Output of Stage 2 helper; you fill in Stage 2
├── resource_doc.txt               ← Output of Stage 2b (optional but recommended)
├── ai_input.txt                   ← Output of Stage 3
├── ai_output.json                 ← You paste AI response here (Stage 4 → 5)
└── data_dictionary.xlsx           ← Final output (Stage 5 → review in Stage 6)
```

---

## Quick-start walkthrough

### Before you begin — one-time setup

1. Open **`context_config.txt`** and fill in your study name, a brief
   description of the dataset, and the name(s) of the source system(s)
   your data comes from. Keep it to 2–5 sentences. Do NOT include any
   real data values, patient names, or record-level information.

2. Generate the architecture figure (optional but recommended for first-time users):
   ```bash
   python3 generate_figure.py
   ```
   Open `pipeline_architecture.png` to orient yourself before starting.

---

### 🔴 STAGE 1 — Extract column names only (MANUAL)

**Goal:** Pull only the header row from your data file.
No data records are read or stored anywhere.

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
   column names — no dates, IDs, or data values.

---

### 🔴 STAGE 2 — Create synthetic example values (MANUAL)

**Goal:** Produce one realistic but entirely fictitious example value for
each column. You supply these using your own knowledge of the data —
no AI tool is involved at this stage.

**Step 2a:** Generate the template:
```bash
python3 step2_make_template.py
```
Creates `synthetic_template.csv` with column headers on Row 1 and empty
cells on Row 2.

**Step 2b:** Open `synthetic_template.csv` in Excel, Numbers, or Google
Sheets and fill in Row 2. Key rules:

| Data type | Good synthetic value | Avoid |
|-----------|---------------------|-------|
| Numeric ID | `9999` | any real record ID |
| Date (YYYY-MM) | `1985-06` | real birth or event date |
| Date (YYYY-MM-DD) | `2021-03-15` | real clinical date |
| Postal / zip code | `A0A` | real geographic code |
| Categorical code | any valid code value | — |
| Free text | a generic label | real names or notes |
| Binary Y/N | `N` | — |
| Missing / null | leave blank or `NaN` | — |

**Step 2c:** Save `synthetic_template.csv` as CSV (not xlsx).

---

### 🔵 STAGE 2b — Attach a reference document (AUTOMATED, optional but recommended)

**Goal:** Give the AI tool a reference document — such as a data dictionary,
codebook, variable label guide, or annotation document — so it can write
accurate, domain-specific descriptions for each variable. This is the key
step that replaces the need to manually write descriptions from scratch.

**Supported formats — any of the following:**
- Word document (`.docx`) — including embedded review comments
- Excel workbook (`.xlsx`) — all sheets extracted
- PDF (`.pdf`) — text extracted page by page
- CSV (`.csv`) — all rows extracted as plain text
- Plain text or Markdown (`.txt`, `.md`)

> The reference document is not restricted to any specific format.
> If your file is in another format (e.g., `.odt`, `.rtf`, `.pptx`),
> use your application's "Save As" to convert it to `.docx` or `.txt` first.

**What makes a good reference document?**
- A data dictionary or codebook provided by your data source/provider
- A variable label guide describing field names, codes, and allowed values
- An annotation document with reviewer notes on variable meanings
- Any document that contains field definitions, code descriptions, or
  domain context that the AI should draw on when writing descriptions

```bash
# Word document (also extracts embedded review comments):
python3 step2b_add_resource_doc.py path/to/variable_guide.docx

# Excel codebook:
python3 step2b_add_resource_doc.py path/to/codebook.xlsx

# PDF data dictionary:
python3 step2b_add_resource_doc.py path/to/data_dictionary.pdf

# Plain text label guide:
python3 step2b_add_resource_doc.py path/to/labels.txt

# CSV codebook:
python3 step2b_add_resource_doc.py path/to/codebook.csv
```

**Output:** `resource_doc.txt` — open and review it to confirm it contains
definitions (not data records) before proceeding.

> **Privacy note:** The reference document should contain variable definitions,
> code labels, and field descriptions only — not data records or participant
> information. The script never reads your actual data file.

---

### 🔵 STAGE 3 — Package for AI (AUTOMATED)

```bash
python3 step3_package_for_ai.py
```

Reads `columns.txt`, `synthetic_template.csv`, `context_config.txt`, and
(if present) `resource_doc.txt`, then writes `ai_input.txt` — a single
structured text block ready to paste into your AI tool.

---

### 🔴 STAGE 4 — Run the AI prompt (MANUAL)

**Capability requirements** (check `ai_prompt.md` for full list):
- Knowledge cutoff 2023 or later
- Outputs valid JSON arrays without truncation
- Context window large enough for the prompt + reference document + column list
  (recommended minimum: 32,000 tokens)

**Steps:**

1. Open your AI tool and start a **new conversation**.

2. Paste the **entire contents of `ai_prompt.md`** into the message field.

3. Immediately after, paste the **entire contents of `ai_input.txt`**.

4. Send the message and wait for the AI's response.

5. The AI should return a **JSON array** (one object per column).
   If it truncates, ask it to continue:
   *"Please continue from column N onwards in the same JSON format."*

6. Copy the **complete JSON response** and save it as **`ai_output.json`**
   in the pipeline folder.
   - Include ```` ```json ```` fences if present — they are stripped automatically.
   - The file must contain a complete, valid JSON array starting with `[`.

---

### 🔵 STAGE 5 — Format output into xlsx (AUTOMATED)

```bash
python3 step5_format_output.py
```

Reads `ai_output.json` and `synthetic_template.csv`, then writes
`data_dictionary.xlsx` with:
- 7 columns: Field, Example Value, Source Table, Data Type, Source System,
  Code/Desc Pair, Description & Comments
- Color-coded rows by source system
- Frozen header row, wrapped text, calibrated column widths
- Summary sheet with a source system legend

---

### 🔴 STAGE 6 — Review and finalize (MANUAL)

1. Open `data_dictionary.xlsx`.
2. Read through all AI-generated descriptions — correct any errors or gaps.
3. Check the **Code/Desc Pair** column for any missed linkages.
4. Add custom notes or caveats in the **Description & Comments** column.
5. Save the final file.

Your data dictionary is complete ✅

---

## Troubleshooting

### `columns.txt not found`
Run `step1_extract_headers.sh` first.

### `synthetic_template.csv has X columns but columns.txt has Y`
Re-run `step2_make_template.py` after any change to `columns.txt`.

### JSON parse error in Step 5
- Ensure `ai_output.json` starts with `[` and ends with `]`
- If the AI stopped mid-array, ask it to continue and merge the two arrays
- Validate the JSON at https://jsonlint.com (do not paste real data)

### AI truncated the output
Ask: *"You stopped before completing all columns. Please continue the
JSON array from column N, maintaining the same format."*
Merge the two JSON arrays manually before saving as `ai_output.json`.

### Colors / styling missing in xlsx
Ensure openpyxl ≥ 3.0: `pip3 install --upgrade openpyxl`

---

## Adapting for any dataset

1. Update `context_config.txt` with your dataset and study details.
2. Run Stage 1 on your new CSV.
3. Supply your own reference document in Stage 2b.
4. Run the pipeline from Stage 3 onward.

The pipeline is designed to work for **any tabular dataset** regardless of
domain or source system. The reference document you supply in Stage 2b is
what makes descriptions accurate and domain-specific — no hard-coded
knowledge about any particular database or system is required.

---

## Privacy summary

| Stage | What the AI tool receives | Real data exposed? |
|-------|--------------------------|-------------------|
| 1 | Nothing | ❌ No |
| 2 | Nothing | ❌ No |
| 2b | Nothing (script runs locally) | ❌ No |
| 3 | Nothing (script runs locally) | ❌ No |
| 4 | Column names + your synthetic values + reference document | ❌ No |
| 5 | AI's own output only | ❌ No |
| 6 | Nothing | ❌ No |

**Your real data file never leaves your machine and is never read by any AI tool.**
