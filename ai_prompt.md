<!-- =========================================================================
     DATA DICTIONARY PIPELINE — AI PROMPT  (Version 1.0)
     Compatible with: Claude 3+, GPT-4, Gemini 1.5+, and equivalent models
     ========================================================================= -->

# ┌─────────────────────────────────────────────────────────────────────────┐
# │  CAPABILITY REQUIREMENTS — check before using this prompt               │
# ├─────────────────────────────────────────────────────────────────────────┤
# │  ✅  Knowledge cutoff 2023 or later                                     │
# │  ✅  Outputs valid JSON arrays (≥150 elements without truncation)        │
# │  ✅  Healthcare / clinical knowledge                                     │
# │      (ICD codes, RAI-HC, nursing assessment terminology)                │
# │  ✅  Context window ≥ 8,000 tokens (for ~105 columns)                   │
# │      Scale up to ≥ 32,000 tokens for datasets with 200+ columns         │
# │  ✅  No internet access required — all reference material is below       │
# │                                                                         │
# │  ❌  NOT suitable for: AI tools without structured output / JSON support │
# └─────────────────────────────────────────────────────────────────────────┘

---

## ROLE

You are a **clinical data documentation specialist** with expertise in:
- Community home health electronic medical records (EMRs)
- The PARIS (Patient Assessment and Review Information System) used by
  Vancouver Coastal Health (VCH), British Columbia, Canada
- The Pixalere wound care documentation platform
- RAI-HC (Resident Assessment Instrument — Home Care) assessment scales
- Clinical wound care terminology and nursing practice

Your task is to generate a structured **data dictionary** for the dataset
columns listed at the end of this prompt.

---

## STUDY CONTEXT

This is a **wound infection prediction machine learning study** using VCH
community home health data (approximately 2019–2021). The dataset merges
two source systems:

1. **PARIS** — VCH's community care EMR. Organised into tables coded A01–B20.
2. **Pixalere** — A wound care documentation platform with two structured
   tables: `ax_structured` (per-visit wound assessments) and `wp_structured`
   (wound profile: etiology, goal of care).

The **target variable** (`label`) is a binary outcome (True/False) indicating
whether a patient received antimicrobial wound products (e.g., acticoat or
calcicare) as a proxy for nurse-directed wound infection prophylaxis.

---

## PARIS TABLE REFERENCE CARD

Use these table codes in the `source_table` field of your output JSON.

| Code | Table Name | Key Variables |
|------|-----------|---------------|
| A01  | Demographics | study_id, birth_dt, Deceased, Gender Code/Desc, fsa |
| A02  | Relationships | Association Code/Desc, relationship dates |
| A03  | Alerts | Alert Code/Desc, Is Extended Leave Alert |
| A04  | Allergies | Substance Type Code, Substance Code/Desc, Reaction Type |
| A05  | Funding Source | Funding Type/Detail Code, income assistance flags |
| A06  | Marital Status | Marital Status Code/Desc |
| A07  | (Reserved) | — |
| A08  | Address | Address Type Code/Desc, fsa (postal code), House Type |
| A09  | Language | Language Code/Desc, Interpretor Required, Main Language |
| A10  | Occupation | Occupation/Employment Status Code |
| A11  | (Extended) | Other demographics |
| B01  | Referrals | referral_id, Referred On, Referral Reason/Source/Dept, Discharge |
| B02  | Allocations | staff allocation type, start/end dates |
| B03  | Assessments | asmt_id, Assessment Type Code/Desc, Assessment Started/Completed |
| B04  | (Reserved) | — |
| B05  | CCP (Clinical Care Plan) | Need/Goal/Outcome/Intervention Code, Discipline, Program |
| B06  | Diagnosis | Diagnosis State/Type Code, Diagnosis Code/Desc, Recorded By Team |
| B07  | Immunization Alerts | (excluded from this study) |
| B08  | Immunization History | Antigen Code/Desc, Dose Number, Immunization Date, Status |
| B09  | Weight & Growth | Date Measured, Weight, Height, BMI, Weight Event Code |
| B10  | Vital Signs | Respirations, Temperature, BP, Heart Rate, O2 Saturation |
| B11  | Palliative Perf. Scale | PPS %, Date |
| B12  | Surgeries & Procedures | Procedure Code/Desc, Date of Procedure |
| B13  | Risk Screen | Visit Type Code, Env/Musc/Viol/Occ risk categories |
| B14  | Immunization Suspensions | Suspension reason, dates |
| B16  | Plan | Intervention Type Code, Provider, Start/End dates |
| B17  | HSO (Home Support) | Type Code, Provider Code/Name, Authorized Hours, Status |
| B18  | Waitlist | Status, Team, Dates |
| B19  | Registers | Register Type, Date Registered/Deregistered |
| B20  | Extended Leave | — |
| RAI  | RAI-HC Assessment | IADL Involvement, ADL Long Form, ADL SP Hierarchy, H1/H2 items |

---

## PIXALERE FIELD REFERENCE

### Terminology
- **Alpha**: General term for a single documented site — one wound, incision,
  drain, or ostomy. Each alpha has a unique `alpha_id`.
- **Sub-assessment**: One evaluation of a single alpha (sub_assessment_id).
- **Assessment**: All sub-assessments for one body-part at one visit (assessment_id).
- **Wound profile type**: All alphas of the same type on one body-part
  (wound_profile_type_id) — used for joining structured and free-text data.

### Source tables
| Prefix | Table | Description |
|--------|-------|-------------|
| `_x` suffix (wp) | wp_structured | Wound profile: etiology, goal_of_care, alpha identifiers |
| `_y` suffix (ax) | ax_structured | Per-visit assessment: visited_on, status, clinical fields |

### Key Pixalere fields
| Field | Description |
|-------|-------------|
| alpha_location | Body part assessed (e.g., Left Ankle/Foot, Abdomen) |
| alpha_type | W=Wound, I=Incision, D=Drain, O=Ostomy |
| alpha_tag | Label for this alpha on the body diagram (A, B, C…) |
| open_date | Date alpha was first documented |
| closed_date | Date alpha was closed (if applicable) |
| care_region | Regional health authority (VCH-Vancouver, VCH-Richmond, etc.) |
| care_location | Clinic name |
| visited_on | Actual encounter date-time (can be backdated) |
| created_on | When record was charted in database |
| etiology | Wound cause (e.g., Venous Insufficiency, Pressure Injury Stage 2) |
| goal_of_care | e.g., To Heal the Wound, To Maintain the Wound, Permanent Ostomy |
| assessment_type | Full Assessment, Partial Assessment, Phone Visit, etc. |
| status | Open, Closed, Open/Client Self-Care |
| wound_onset_date | Date the wound/incision/ostomy first opened |
| treatment_plan_created | Whether treatment plan was modified (Yes/No) |
| review_done | Whether a product review was completed (Yes/No) |
| progress_note_created | Whether a progress note was recorded (Yes/No) |

---

## RAI-HC ASSESSMENT REFERENCE

### IADL Involvement Scale (`IADL_Involvement`)
Sum score of 7 IADL items. Range 0–21. Higher = more involvement needed.
See RAI outcome scales document page 18.

### ADL Long Form Scale (`ADL_Long_Form`)
Sum of ADL self-performance items. Range 0–28. Higher = more dependence.
See RAI outcome scales document page 5.

### ADL Self-Performance Hierarchy (`ADL_SP_Hierarchy`)
Hierarchical scale 0–6. 0=Independent, 6=Total dependence.
See RAI outcome scales document page 7.

### Individual IADL items (H1a–H1g prefix)
`H1aA_MealpreparationSelf`, `H1bA_OrdinaryHouseworkSelf`,
`H1cA_ManageFinSelf`, `H1dA_ManageMedSelf`, `H1eA_PhoneUseSelf`,
`H1fA_ShoppingSelf`, `H1gA_TransportationSelf`

Scale per item: 0=Independent, 1=Setup help only,
2=Limited assistance, 3=Extensive assistance, 8=Activity did not occur.

### Individual ADL items (H2 prefix)
`H2a_MobilityinBed`, `H2b_Transfer`, `H2c_LocoInHome`,
`H2e_DressingUpperBody`, `H2f_DressingLowerBody`,
`H2g_Eating`, `H2h_ToiletUse`, `H2i_PersonalHygiene`

---

## OUTPUT SPECIFICATION

Produce a **JSON array** where each element is one object representing one
column. Every object must have exactly these 6 keys:

```json
{
  "field": "exact_column_name_as_provided",
  "data_type": "one of the allowed types listed below",
  "source_table": "PARIS table code (e.g. A01) or Pixalere (ax) or Pixalere (wp) or Derived or —",
  "source_system": "PARIS or Pixalere or Derived",
  "code_desc_pair": "name of partner column if this is a Code↔Desc pair, otherwise —",
  "description": "A clear 2–4 sentence clinical description of the variable."
}
```

### Allowed values for `data_type`
Use these exact phrases (pick the best fit):
- `Numeric (ID)` — system-generated integer identifier
- `Numeric (integer)` — count or dose number
- `Numeric (continuous)` — measurement (height, weight, vital sign)
- `Numeric (standardized)` — z-score normalized continuous variable
- `Date (YYYY-MM-DD)` — calendar date
- `Date (YYYY-MM)` — year-month only (partial date, often for privacy)
- `Datetime` — timestamp with time component
- `Categorical (code)` — short coded value (use code column name)
- `Categorical (string)` — free-text category label
- `Binary (Y/N)` — Yes/No flag
- `Binary (True/False)` — boolean outcome
- `Ordinal` — ordered scale (RAI items)
- `String` — free text or mixed format

### Allowed values for `source_system`
- `PARIS`
- `Pixalere`
- `Derived` — computed or target variable

### Guidelines for `description`
- Begin with what the field **represents clinically**.
- State the **source table** name (e.g., "From PARIS B01-Referrals table.").
- Note **allowed values** or scale if applicable.
- Note **privacy or data quality considerations** if relevant.
- For `_x` / `_y` suffix columns: explain the suffix (join disambiguation).
- For Code/Desc column pairs: the code column description should note its
  Desc partner, and vice versa.
- For audit timestamp fields (Created/Amended): use this standard phrase:
  "System-generated audit timestamp recorded when this record was
  created/last amended in [PARIS/Pixalere]."

---

## TASK INSTRUCTIONS

1. Read the study context and column list below carefully.
2. For **every** column in the list, produce one JSON object.
3. Use the PARIS table reference card and Pixalere field reference above
   to assign the correct `source_table` and `source_system`.
4. The `field` value must match the column name **exactly** as given.
5. The `code_desc_pair` should name the linked partner column where a
   Code↔Desc relationship exists (e.g., `"Gender Desc"` for `"Gender Code"`).
   Use `"—"` if no pair exists.
6. Output the **complete JSON array only** — no explanatory text before or
   after. Wrap the array in ```json fences.
7. Do not truncate. Every column must appear in the output.

---

## COLUMN DATA  ← PASTE CONTENTS OF ai_input.txt HERE

```
<<PASTE ai_input.txt CONTENTS HERE>>
```

---
<!-- End of prompt — do not edit below this line -->
