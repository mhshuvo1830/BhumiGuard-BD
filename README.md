# 🏡 BhumiGuard BD

### Bangla-First AI-Assisted Pre-Registration Land Transaction Risk Screening

> **শুধু দলিল নয় — লেনদেনের ইতিহাসও যাচাই।**  
> **Verify the transaction, not just the document.**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://bhumiguard-bd.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-BhumiGuard--BD-181717?logo=github)](https://github.com/mhshuvo1830/BhumiGuard-BD)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

---

## 🌐 Quick Links

- **Live App:** https://bhumiguard-bd.streamlit.app
- **Source Code:** https://github.com/mhshuvo1830/BhumiGuard-BD
- **Main App File:** `app/app.py`
- **Backend Package:** `src/bhumiguard/`

---

## 1. Project Overview

**BhumiGuard BD** is a Bangla-first, explainable **pre-registration land transaction risk-screening prototype** designed for the Bangladesh context.

The core idea is simple:

> A land deed may look valid as a document, while the proposed **transaction itself** may still contain serious inconsistencies.

BhumiGuard BD therefore goes beyond document appearance and checks the proposed transaction against structured evidence such as:

- seller and buyer registry references,
- current ownership records,
- parcel identity,
- transfer amount,
- previous transaction history,
- identified land portion,
- mutation-side ownership evidence.

The system returns an explainable screening result:

- **LOW RISK** — no blocking anomaly detected,
- **MEDIUM RISK** — evidence is incomplete or requires review,
- **HIGH RISK** — one or more important checks failed.

> **Important:** BhumiGuard BD is a decision-support prototype. It does **not** establish legal title and does **not** prove fraud.

---

## 2. সমস্যাটি কী? / What Problem Does It Solve?

বাংলাদেশে ভূমি লেনদেনের ক্ষেত্রে শুধু একটি দলিল দেখতে সঠিক বা আসল মনে হচ্ছে কিনা যাচাই করলেই সব ঝুঁকি ধরা যায় না। একটি প্রস্তাবিত লেনদেনে আরও সমস্যা থাকতে পারে, যেমন:

- বিক্রেতা প্রকৃত বর্তমান মালিক নন,
- মালিকানার চেয়ে বেশি জমি বিক্রির চেষ্টা,
- একই নির্দিষ্ট জমির অংশ একাধিকবার বিক্রির ঝুঁকি,
- একই দলিল নম্বর পুনরায় ব্যবহার,
- দলিলের বিক্রেতা ও নামজারি রেকর্ডের মালিকের অমিল,
- অসম্পূর্ণ বা অনির্ভরযোগ্য evidence.

BhumiGuard BD এই transaction-level inconsistency গুলোকে explainable rule-based screening-এর মাধ্যমে শনাক্ত করার চেষ্টা করে।

---

## 3. Who Is This Prototype For?

BhumiGuard BD is designed as a prototype for:

- pre-registration land transaction screening,
- land-service operators and reviewers,
- hackathon / research demonstration,
- explainable risk analysis before deeper manual review,
- future integration with authorized land-record services.

It is **not** intended to replace:

- Sub-Registrar offices,
- official mutation or land-record authorities,
- licensed legal review,
- judicial or administrative title determination.

---

## 4. Why BhumiGuard BD Is Different

Many document-verification systems focus mainly on OCR, visual authenticity, or document classification.

BhumiGuard BD shifts the focus from:

```text
"Is this document visually valid?"
```

toward:

```text
"Is this proposed land transaction consistent with the available evidence?"
```

The prototype combines:

```text
Deed / Document
      ↓
OCR / Structured Extraction
      ↓
Human Verification Gate
      ↓
Normalized Parcel Identity
      ↓
Ownership Ledger
      ↓
Transaction History
      ↓
Mutation Evidence
      ↓
Explainable Risk Rules
      ↓
LOW / MEDIUM / HIGH Screening Result
```

---

## 5. Current Features

### 🧾 Transaction Screening

- Deed ID validation
- Seller registry validation
- Buyer registry validation
- Parcel registry validation
- Seller ownership verification
- Transfer-area sufficiency check
- Previous sale / double-sale screening
- Mutation-side ownership consistency check

### 🧠 Explainable Risk Engine

The system currently evaluates **8 explainable checks** and returns:

- PASS / WARNING / FAIL status,
- machine-readable rule code,
- human-readable explanation,
- overall risk level,
- pass / warning / fail counts.

### 🇧🇩 Bangla-First Interface

- Bangla is the default UI language
- English is available as an optional switch
- Bangla numerals are used in Bangla presentation mode
- Internal IDs remain machine-readable

### 🧪 Validated Demo Mode

Six controlled synthetic scenarios are included:

| Scenario | Expected Result |
|---|---|
| Clear baseline | LOW |
| Seller not owner | HIGH |
| Over-transfer | HIGH |
| Double sale | HIGH |
| Duplicate deed | HIGH |
| Mutation mismatch | HIGH |

### 🧩 Custom Transaction Mode

Users can create their own synthetic/test transaction by changing:

- deed ID,
- seller ID,
- buyer ID,
- parcel ID,
- portion ID,
- transfer area,
- seller/buyer/parcel registry presence,
- seller ownership amount,
- duplicate-deed evidence,
- previous same-portion sale evidence,
- mutation availability,
- mutation-side owner.

This allows the same frozen backend engine to be tested on **custom combinations of anomalies**, not only predefined scenarios.

### 📄 Downloadable Screening Report

Each screening run can generate a downloadable text report containing:

- screening ID,
- transaction summary,
- overall risk level,
- pass/warning/fail counts,
- individual rule results,
- explanations,
- disclaimer.

### 🔎 Evidence Summary

The UI exposes supporting evidence for:

- ownership ledger,
- previous transaction history,
- mutation-side record.

### 🆔 Screening / Case ID

Each screening run receives a unique case identifier such as:

```text
BG-20261017-A1B2C3
```

---

## 6. Live Demo — How to Use

### Open the app

Go to:

**https://bhumiguard-bd.streamlit.app**

The application opens in **Bangla by default**.

---

### Mode A — Validated Demo

1. Keep **বাংলা** or switch to **English**.
2. Choose **প্রস্তুত ডেমো / Validated Demo**.
3. Select one of the six scenarios.
4. Click **লেনদেন যাচাই করুন / Verify Transaction**.
5. Review:
   - overall risk,
   - passed checks,
   - warnings,
   - failed checks,
   - explainable rule table,
   - ownership evidence,
   - previous transaction evidence,
   - mutation evidence.
6. Download the screening report if needed.

Recommended demo sequence:

```text
Clear Baseline
→ LOW risk
→ 8 PASS

Double Sale
→ HIGH risk
→ DOUBLE_SALE failure

Mutation Mismatch
→ HIGH risk
→ DEED_MUTATION_MISMATCH failure
```

---

### Mode B — Custom Transaction Screening

1. Select **কাস্টম লেনদেন যাচাই / Custom Transaction**.
2. Enter synthetic/test transaction identifiers.
3. Configure registry evidence.
4. Configure current ownership evidence.
5. Configure previous transaction history.
6. Configure mutation evidence.
7. Click **কাস্টম লেনদেন যাচাই করুন / Screen Custom Transaction**.
8. Review the explainable result.
9. Download the screening report.

Example multi-risk test:

```text
Seller is current owner        → OFF
Duplicate deed                 → ON
Previous same-portion sale     → ON
Mutation owner                 → OTHER-OWNER-CUSTOM
```

Expected result:

```text
HIGH RISK
Multiple failed checks
```

> Do not enter real NIDs, phone numbers, confidential personal information, or sensitive land records into the public demo. Use synthetic/test identifiers only.

---

## 7. Core Risk Checks

The current prototype evaluates the following checks:

### 1. Deed ID Check
Detects whether the same deed identifier already exists in transaction history.

### 2. Seller Reference Check
Verifies whether the seller exists in the supplied registry.

### 3. Buyer Reference Check
Verifies whether the buyer exists and is different from the seller.

### 4. Parcel Check
Verifies whether the target parcel exists in the supplied parcel registry.

### 5. Seller Ownership Check
Checks whether the seller currently owns the target parcel.

### 6. Area Check
Checks whether the requested transfer area is within the seller's recorded ownership.

### 7. Double-Sale Check
Checks whether the **same identified land portion** has a previous valid sale.

> Area alone is not used to prove that two transactions refer to the same physical portion. A reliable `portion_id` is required for strong double-sale checking.

### 8. Mutation Check
Compares the deed-side seller with the active mutation-side owner.

> A mutation mismatch is treated as a screening signal, not legal proof of fraud.

---

## 8. Risk Interpretation

### LOW RISK
No blocking anomaly was detected in the supplied evidence.

### MEDIUM RISK
One or more checks are incomplete or cannot be fully verified.

Examples:

- no reliable `portion_id`,
- no matching mutation record.

### HIGH RISK
One or more important checks failed.

Examples:

- seller not owner,
- insufficient ownership,
- duplicate deed,
- double sale,
- deed–mutation mismatch.

---

## 9. Document & OCR Pipeline

BhumiGuard BD also includes research/prototype work for Bengali deed ingestion and structured extraction.

The current document workflow is:

```text
Raw Deed / Image
      ↓
Quality & Content Review
      ↓
Orientation Analysis
      ↓
Targeted Preprocessing (when needed)
      ↓
Bengali OCR Candidate Extraction
      ↓
Structured Field Extraction
      ↓
Human Verification
      ↓
Risk Engine
```

### Important Safety Rule

Handwritten OCR output is treated as a **candidate**, not automatically trusted evidence.

Unverified OCR values are blocked from entering the risk engine.

---

## 10. Structured Deed Fields

The prototype research pipeline defines 19 core fields:

```text
deed_id
deed_type
registration_office
execution_date
seller_id
seller_name
buyer_id
buyer_name
district
upazila
mouza
survey_type
khatian_no
dag_no
total_property_area
transferred_area
seller_ownership_share
previous_deed_reference
power_of_attorney_reference
```

Derived identifiers include:

- `parcel_key`
- `portion_id` when reliable schedule / boundary / share evidence exists

---

## 11. Demo Data Policy

All public-facing demo identities and land records are **synthetic**.

The repository intentionally does not publish local raw research documents such as:

- handwritten deed images,
- downloaded deed PDFs,
- supporting raw documents,
- private/sensitive records.

These are excluded through `.gitignore`.

---

## 12. Validation Status

### Final Regression Contract

The backend was frozen only after all six final scenarios passed:

```text
CLEAR_BASELINE       → LOW   ✅
SELLER_NOT_OWNER     → HIGH  ✅
OVER_TRANSFER        → HIGH  ✅
DOUBLE_SALE          → HIGH  ✅
DUPLICATE_DEED       → HIGH  ✅
MUTATION_MISMATCH    → HIGH  ✅
```

Final regression summary:

```text
Contracts passed: 6/6
Baseline LOW: True
Baseline zero failures: True
All anomaly scenarios HIGH: True
All required fail codes detected: True
```

### Controlled Benchmark

Earlier backend development also used a controlled synthetic benchmark with:

- 600 records,
- 6 risk classes,
- 100 examples per class.

The benchmark was designed to validate rule purity and ledger behavior before UI integration.

---

## 13. Project Structure

```text
BhumiGuard-BD/
│
├── app/
│   └── app.py
│
├── src/
│   └── bhumiguard/
│       ├── __init__.py
│       ├── normalization.py
│       ├── ledger.py
│       ├── validation.py
│       └── risk.py
│
├── notebooks/
│   ├── 01_data_setup.ipynb
│   ├── 02_dataset_audit.ipynb
│   ├── 03_saf_kabala_schema.ipynb
│   ├── 04_synthetic_registry.ipynb
│   ├── 05_document_ingestion.ipynb
│   ├── 06_handwritten_preprocessing.ipynb
│   ├── 07_structured_field_extraction.ipynb
│   └── 08_end_to_end_integration.ipynb
│
├── data/
│   ├── raw/
│   ├── synthetic/
│   └── processed/
│
├── scripts/
├── tests/
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 14. Technology Stack

### Core

- Python
- Pandas
- Streamlit

### Document Processing

- Tesseract OCR
- pytesseract
- pypdf
- pypdfium2
- Pillow

### Analysis / Visualization

- NumPy
- Matplotlib

---

## 15. Local Installation

### Clone the repository

```bash
git clone https://github.com/mhshuvo1830/BhumiGuard-BD.git
cd BhumiGuard-BD
```

### Create a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
streamlit run app/app.py
```

Windows users may also run:

```powershell
streamlit run app\app.py
```

The app normally opens locally at:

```text
http://localhost:8501
```

---

## 16. Deployment

The current prototype is deployed using **Streamlit Community Cloud**.

Deployment configuration:

```text
Repository: mhshuvo1830/BhumiGuard-BD
Branch: main
Entry point: app/app.py
```

Live application:

**https://bhumiguard-bd.streamlit.app**

---

## 17. Current Prototype Status

| Component | Status |
|---|---|
| Dataset audit | ✅ Complete |
| Saf Kabala field schema | ✅ Complete |
| Synthetic registry | ✅ Complete |
| Ownership ledger | ✅ Complete |
| Explainable risk engine | ✅ Complete |
| Controlled benchmark | ✅ Complete |
| Document ingestion | ✅ Complete |
| Handwritten preprocessing | ✅ Prototype complete |
| Structured extraction | ✅ Prototype complete |
| Human verification gate | ✅ Complete |
| Parcel identity workflow | ✅ Complete |
| End-to-end backend integration | ✅ Complete |
| 6 validated demo scenarios | ✅ Complete |
| Custom interactive screening | ✅ Complete |
| Bangla-first bilingual UI | ✅ Complete |
| Screening report download | ✅ Complete |
| Streamlit deployment | ✅ Live |

---

## 18. Limitations

The current hackathon prototype has important limitations:

1. It is **not connected to official government land-record databases**.
2. Public demo records are synthetic.
3. Bengali handwritten OCR is assistive rather than fully autonomous.
4. OCR-derived values require human verification before entering the risk engine.
5. Reliable double-sale detection depends on a trustworthy land-portion identifier.
6. Area equality alone is not treated as proof of the same physical land portion.
7. Mutation mismatch is a screening signal, not proof of fraudulent ownership.
8. The system does not make legal title decisions.
9. The prototype does not write back to any official land system.

---

## 19. Future Development

Potential next-stage work includes:

### Data & Integration

- authorized integration with official land-record APIs,
- secure registry connectors,
- verified mutation and ownership data sources,
- cadastral / map-based parcel matching.

### AI / Document Intelligence

- stronger Bengali handwritten deed recognition,
- better table and schedule extraction,
- automatic boundary-clause parsing,
- provenance-aware field confidence,
- reviewer-assisted OCR correction.

### Risk Intelligence

- temporal ownership reconstruction,
- richer chain-of-title analysis,
- geospatial overlap detection,
- risk scoring calibrated from real labeled cases,
- anomaly detection across large transaction networks.

### Product / Governance

- role-based access control,
- reviewer case management,
- evidence audit trail,
- digital signatures,
- privacy-preserving processing,
- secure document retention policies,
- official reviewer approval workflow.

---

## 20. Security & Privacy Principles

BhumiGuard BD is designed around conservative handling of land evidence:

- no real personal identifiers are required for the public demo,
- raw research documents are excluded from the public repository,
- unverified OCR is not treated as authoritative evidence,
- screening does not automatically mutate ownership records,
- uncertainty is surfaced as WARNING instead of being silently converted into a fraud claim.

---

## 21. Recommended Judge Demo Flow

### Step 1 — Show the baseline

```text
Validated Demo
→ Clear Baseline
→ Verify Transaction
→ LOW risk
→ 8 passed checks
```

### Step 2 — Show double-sale detection

```text
Validated Demo
→ Double Sale
→ HIGH risk
→ Same identified portion has a previous valid sale
```

### Step 3 — Show ownership mismatch

```text
Validated Demo
→ Seller Not Owner
→ HIGH risk
```

### Step 4 — Show custom interaction

Switch to **Custom Transaction** and create a multi-risk case:

```text
Seller is current owner        → OFF
Duplicate deed                 → ON
Previous same-portion sale     → ON
Mutation owner                 → OTHER-OWNER-CUSTOM
```

Then run screening and show multiple failed checks.

### Step 5 — Download the report

Use the built-in report download button to show that the result can be exported for review.

---

## 22. Key Contribution

The core contribution of BhumiGuard BD is the shift from **document-only verification** to **transaction-integrity screening**.

Instead of asking only:

> “Does this deed look valid?”

BhumiGuard BD asks:

> “Is this proposed transfer consistent with the available ownership, history, portion, area, and mutation evidence?”

---

## 23. Disclaimer

**BhumiGuard BD is a research and hackathon decision-support prototype.**

A LOW, MEDIUM, or HIGH screening result:

- does not establish legal ownership,
- does not invalidate a deed,
- does not prove fraud,
- does not replace official land administration or legal review.

Human and legally authorized review remains necessary for official decisions.

---

## 24. Links

- **Live Demo:** https://bhumiguard-bd.streamlit.app
- **GitHub Repository:** https://github.com/mhshuvo1830/BhumiGuard-BD

---

## LandTech 2026 Prototype

### **BhumiGuard BD**

**শুধু দলিল নয় — লেনদেনের ইতিহাসও যাচাই।**  
**Verify the transaction, not just the document.**
