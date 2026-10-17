# 🏡 BhumiGuard BD

**AI-Assisted Pre-Registration Land Transaction Risk Screening**

**বাংলা:** শুধু দলিল নয় — লেনদেনের ইতিহাসও যাচাই  
**English:** Verify the transaction, not just the document

---

## 1. Overview

BhumiGuard BD is a prototype decision-support system designed for pre-registration screening of land transactions in Bangladesh.

Instead of checking only whether a deed appears authentic, the system evaluates the proposed transaction against structured ownership, transaction-history, parcel, and mutation-side evidence.

The prototype can flag risks such as:

- seller not being the current owner,
- attempted transfer beyond recorded ownership,
- possible double sale of the same identified land portion,
- duplicate deed identifiers,
- deed–mutation mismatch,
- incomplete evidence requiring further review.

BhumiGuard BD does **not** establish legal title and does **not** prove fraud.

---

## 2. Core Idea

Traditional document-only verification may fail to detect transaction-level inconsistencies.

BhumiGuard BD therefore follows this workflow:

\\\	ext
Document / Deed
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
\\\

---

## 3. Main Risk Checks

The current prototype evaluates eight explainable checks:

1. Deed ID availability
2. Seller registry reference
3. Buyer registry reference
4. Parcel registry reference
5. Seller ownership
6. Transfer-area availability
7. Previous sale / double-sale risk
8. Mutation-side ownership consistency

---

## 4. Validated Demo Scenarios

Six controlled synthetic scenarios are included:

| Scenario | Expected Result |
|---|---|
| Clear baseline | LOW |
| Seller not owner | HIGH |
| Over-transfer | HIGH |
| Double sale | HIGH |
| Duplicate deed | HIGH |
| Mutation mismatch | HIGH |

The six demo contracts were validated against the backend risk engine.

---

## 5. Bangla-First Interface

The application is designed primarily for Bangla-speaking users.

- Default interface language: **বাংলা**
- Optional language: **English**
- Bangla numerals are used in Bangla presentation mode.
- Internal technical identifiers remain machine-readable.

---

## 6. Project Structure

\\\	ext
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
├── tests/
├── scripts/
├── requirements.txt
├── .gitignore
└── README.md
\\\

---

## 7. Prototype Data

Current local research assets include:

- 653 handwritten deed images
- 17 deed/sample-document files
- 5 supporting-form files

Repository file counts may additionally include \.gitkeep\ placeholders.

All public-facing demo transactions use synthetic identities and synthetic land records.

---

## 8. Handwritten Document Processing

The handwritten document workflow includes:

1. content and quality review,
2. orientation testing,
3. optional targeted preprocessing,
4. Bengali OCR candidate generation,
5. human verification,
6. structured field extraction.

Handwritten OCR output is **not automatically trusted** for transaction-risk execution.

Human verification is required before extracted values can enter the risk engine.

---

## 9. Document Safety Principles

The prototype follows several conservative rules:

- OCR label detection is not treated as extracted evidence.
- Unverified OCR values do not enter the transaction engine.
- Area alone does not establish that two transactions concern the same physical portion.
- Double-sale detection requires a reliable \portion_id\.
- Missing mutation information is treated as incomplete evidence, not automatic fraud.
- Screening does not modify ownership records.
- Synthetic demo records cannot be committed as live transactions.

---

## 10. Installation

### Python

Development environment used:

\\\	ext
Python 3.13.7
\\\

Install dependencies:

\\\ash
pip install -r requirements.txt
\\\

---

## 11. Run the Application

From the project root:

\\\ash
streamlit run app/app.py
\\\

On Windows:

\\\powershell
cd D:\BhumiGuard-BD
streamlit run app\app.py
\\\

The application normally opens at:

\\\	ext
http://localhost:8501
\\\

---

## 12. Demo Flow

Recommended demonstration:

1. Open BhumiGuard BD.
2. Keep default language as Bangla.
3. Run the **Clear Baseline** scenario.
4. Show the LOW-risk result and eight passed checks.
5. Select the **Double Sale** scenario.
6. Show the HIGH-risk result and explainable double-sale flag.
7. Select **Seller Not Owner** or **Mutation Mismatch**.
8. Show how ownership and mutation-side evidence affect the decision.
9. Demonstrate the English-language switch.
10. Emphasize that the system is screening support, not legal adjudication.

---

## 13. Technology

Core prototype stack:

- Python
- Pandas
- Streamlit
- Tesseract OCR
- pypdf
- pypdfium2
- Pillow
- Matplotlib

---

## 14. Current Prototype Status

- Data audit: ✅
- Saf Kabala schema: ✅
- Synthetic registry: ✅
- Ownership ledger: ✅
- Risk engine: ✅
- Controlled benchmark: ✅
- Document ingestion: ✅
- Handwritten preprocessing: ✅
- Structured extraction: ✅
- Human verification gate: ✅
- Parcel identity workflow: ✅
- End-to-end integration: ✅
- Six risk-demo scenarios: ✅
- Bangla-first bilingual UI: ✅

---

## 15. Limitations

The current hackathon prototype has important limitations:

- It is not connected to an official government land-record database.
- Public demo records are synthetic.
- Bengali handwritten OCR is assistive rather than fully autonomous.
- Portion identification requires reliable schedule, boundary, share, or equivalent evidence.
- Mutation mismatch is a screening signal and is not proof of fraudulent ownership.
- Legal title determination remains outside the scope of this system.

---

## 16. Future Development

Potential next-stage work includes:

- secure integration with authorized land-record systems,
- stronger Bangla deed OCR and handwriting recognition,
- automated schedule and boundary extraction,
- geospatial parcel matching,
- provenance-aware evidence tracing,
- case-management workflow for human reviewers,
- audit logging,
- role-based government/user access,
- privacy-preserving document processing.

---

## 17. Disclaimer

**BhumiGuard BD is a decision-support prototype.**

A LOW, MEDIUM, or HIGH screening result does not establish legal title, invalidate a deed, or prove fraud.

Human and legally authorized review remains necessary for official decisions.

---

## LandTech 2026 Prototype

**BhumiGuard BD**  
**শুধু দলিল নয় — লেনদেনের ইতিহাসও যাচাই**
