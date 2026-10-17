from pathlib import Path
from datetime import datetime
from uuid import uuid4
from textwrap import dedent
import sys

import pandas as pd
import streamlit as st


# =========================================================
# PROJECT SETUP
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bhumiguard import risk


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ভূমিগার্ড বিডি | BhumiGuard BD",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SAFE HTML RENDERER
# =========================================================

def render_html(content):
    """
    Render raw HTML directly.
    st.html() avoids Markdown interpreting nested HTML
    as a code block.
    """
    cleaned_html = dedent(content).strip()
    st.html(cleaned_html)


# =========================================================
# GLOBAL CSS
# =========================================================

render_html(
    """
    <style>
    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2.5rem;
        max-width: 1380px;
    }

    html, body {
        font-family:
            "Noto Sans Bengali",
            "Hind Siliguri",
            "SolaimanLipi",
            "Kalpurush",
            Arial,
            sans-serif;
    }

    h1, h2, h3 {
        letter-spacing: -0.02em;
    }

    /* HERO */

    .hero-card {
        border: 1px solid rgba(128,128,128,0.22);
        border-radius: 22px;
        padding: 30px 32px;
        margin-bottom: 22px;
        background:
            linear-gradient(
                135deg,
                rgba(34, 197, 94, 0.13),
                rgba(30, 64, 175, 0.07)
            );
    }

    .hero-title {
        font-size: 2.35rem;
        font-weight: 800;
        line-height: 1.3;
        margin-bottom: 7px;
    }

    .hero-subtitle {
        font-size: 1.08rem;
        opacity: 0.88;
        margin-bottom: 8px;
        line-height: 1.6;
    }

    .hero-tagline {
        opacity: 0.72;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    .hero-badge {
        display: inline-block;
        margin-top: 14px;
        padding: 6px 12px;
        border-radius: 999px;
        background: rgba(34,197,94,0.14);
        border: 1px solid rgba(34,197,94,0.32);
        font-size: 0.82rem;
        font-weight: 700;
    }

    /* SECTION CARD */

    .section-card {
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 17px;
        padding: 20px 22px;
        margin-top: 8px;
        margin-bottom: 16px;
        background: rgba(128,128,128,0.025);
    }

    .section-kicker {
        font-size: 0.78rem;
        opacity: 0.60;
        margin-bottom: 4px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .section-title {
        font-size: 1.28rem;
        font-weight: 800;
        margin-bottom: 6px;
        line-height: 1.5;
    }

    .section-description {
        opacity: 0.75;
        font-size: 0.93rem;
        line-height: 1.65;
    }

    /* RISK CARD */

    .risk-card {
        padding: 25px 27px;
        border-radius: 18px;
        margin: 8px 0 18px 0;
        border: 1px solid rgba(128,128,128,0.20);
    }

    .risk-low {
        background: rgba(34,197,94,0.11);
        border-color: rgba(34,197,94,0.35);
    }

    .risk-medium {
        background: rgba(245,158,11,0.11);
        border-color: rgba(245,158,11,0.35);
    }

    .risk-high {
        background: rgba(239,68,68,0.11);
        border-color: rgba(239,68,68,0.35);
    }

    .risk-title {
        font-size: 1.8rem;
        font-weight: 850;
        margin-bottom: 6px;
        line-height: 1.4;
    }

    .risk-description {
        opacity: 0.80;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* RULE CARD */

    .rule-card {
        border-radius: 14px;
        padding: 15px 17px;
        margin-bottom: 10px;
        border: 1px solid rgba(128,128,128,0.18);
    }

    .rule-pass {
        background: rgba(34,197,94,0.075);
        border-left: 5px solid #22c55e;
    }

    .rule-warning {
        background: rgba(245,158,11,0.08);
        border-left: 5px solid #f59e0b;
    }

    .rule-fail {
        background: rgba(239,68,68,0.085);
        border-left: 5px solid #ef4444;
    }

    .rule-name {
        font-weight: 800;
        font-size: 0.98rem;
        margin-bottom: 3px;
    }

    .rule-code {
        font-size: 0.80rem;
        opacity: 0.64;
        margin-bottom: 5px;
    }

    .rule-message {
        font-size: 0.92rem;
        opacity: 0.88;
        line-height: 1.55;
    }

    /* METRICS */

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 14px;
        padding: 12px 14px;
        background: rgba(128,128,128,0.02);
    }

    div[data-testid="stMetricValue"] {
        font-size: 1.72rem;
        font-weight: 800;
    }

    /* BUTTON */

    .stButton > button {
        border-radius: 12px;
        min-height: 47px;
        font-weight: 700;
    }

    .stDownloadButton > button {
        border-radius: 12px;
        min-height: 44px;
        font-weight: 700;
    }

    /* FORM */

    div[data-testid="stForm"] {
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 18px;
        padding: 20px 22px;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.15);
    }

    /* FOOTER */

    .footer-note {
        opacity: 0.60;
        font-size: 0.82rem;
        text-align: center;
        padding-top: 8px;
        line-height: 1.7;
    }

    </style>
    """
)


# =========================================================
# LANGUAGE
# =========================================================

language = st.sidebar.radio(
    "ভাষা / Language",
    ["বাংলা", "English"],
    index=0,
    horizontal=True,
)

LANG = "bn" if language == "বাংলা" else "en"


def bi(bn, en):
    return bn if LANG == "bn" else en


# =========================================================
# BANGLA DIGITS
# =========================================================

BANGLA_DIGITS = str.maketrans(
    "0123456789",
    "০১২৩৪৫৬৭৮৯",
)


def local_number(value):
    if LANG == "en":
        return str(value)

    return str(value).translate(
        BANGLA_DIGITS
    )


# =========================================================
# TRANSLATION MAPS
# =========================================================

VALUE_BN = {
    "PASS": "সফল",
    "WARNING": "সতর্কতা",
    "FAIL": "ব্যর্থ",
    "ACTIVE": "সক্রিয়",
    "INACTIVE": "নিষ্ক্রিয়",
    "VALID": "বৈধ",
    "INVALID": "অবৈধ",
    "PENDING": "অপেক্ষমাণ",
}


RULE_NAME_BN = {
    "deed_id_check":
        "দলিল নম্বর যাচাই",

    "seller_reference_check":
        "বিক্রেতা নিবন্ধন যাচাই",

    "buyer_reference_check":
        "ক্রেতা নিবন্ধন যাচাই",

    "parcel_check":
        "ভূমি খণ্ড যাচাই",

    "seller_ownership_check":
        "বিক্রেতার মালিকানা যাচাই",

    "area_check":
        "জমির পরিমাণ যাচাই",

    "double_sale_check":
        "পুনরায় বিক্রি যাচাই",

    "mutation_check":
        "নামজারি তথ্য যাচাই",
}


RULE_CODE_BN = {
    "DEED_ID_AVAILABLE":
        "দলিল নম্বর পুনরাবৃত্ত নয়",

    "DUPLICATE_DEED":
        "একই দলিল নম্বর পুনরায় ব্যবহৃত",

    "SELLER_FOUND":
        "বিক্রেতা পাওয়া গেছে",

    "SELLER_NOT_FOUND":
        "বিক্রেতা পাওয়া যায়নি",

    "SELLER_NOT_OWNER":
        "বিক্রেতা বর্তমান মালিক নন",

    "BUYER_FOUND":
        "ক্রেতা পাওয়া গেছে",

    "BUYER_NOT_FOUND":
        "ক্রেতা পাওয়া যায়নি",

    "PARCEL_FOUND":
        "ভূমি খণ্ড পাওয়া গেছে",

    "PARCEL_NOT_FOUND":
        "ভূমি খণ্ড পাওয়া যায়নি",

    "SELLER_IS_OWNER":
        "বিক্রেতাই বর্তমান মালিক",

    "AREA_AVAILABLE":
        "পর্যাপ্ত মালিকানা রয়েছে",

    "INSUFFICIENT_OWNERSHIP":
        "মালিকানার তুলনায় বেশি জমি হস্তান্তর",

    "AREA_CHECK_NOT_APPLICABLE":
        "জমির পরিমাণ যাচাই প্রযোজ্য নয়",

    "NO_PREVIOUS_SALE":
        "পূর্ববর্তী বৈধ বিক্রি নেই",

    "DOUBLE_SALE":
        "একই জমি পুনরায় বিক্রির ঝুঁকি",

    "PORTION_ID_UNAVAILABLE":
        "ভূমি অংশ শনাক্তকরণ অনুপস্থিত",

    "MUTATION_MATCH":
        "নামজারি তথ্য মিলেছে",

    "DEED_MUTATION_MISMATCH":
        "দলিল ও নামজারি তথ্যে অমিল",

    "NO_MUTATION_RECORD":
        "নামজারি রেকর্ড পাওয়া যায়নি",

    "INVALID_BUYER":
        "ক্রেতার তথ্য অবৈধ",

    "INVALID_SELLER":
        "বিক্রেতার তথ্য অবৈধ",
}


RULE_BN = {
    "DEED_ID_AVAILABLE":
        "দলিল নম্বরটি পূর্ববর্তী রেকর্ডে পুনরায় পাওয়া যায়নি।",

    "DUPLICATE_DEED":
        "একই দলিল নম্বর পূর্ববর্তী লেনদেনের রেকর্ডে ইতোমধ্যে রয়েছে।",

    "SELLER_FOUND":
        "বিক্রেতার তথ্য নিবন্ধিত ব্যক্তির তালিকায় পাওয়া গেছে।",

    "SELLER_NOT_FOUND":
        "বিক্রেতার তথ্য নিবন্ধিত ব্যক্তির তালিকায় পাওয়া যায়নি।",

    "SELLER_NOT_OWNER":
        "বিক্রেতা এই ভূমি খণ্ডের বর্তমান মালিক হিসেবে পাওয়া যায়নি।",

    "BUYER_FOUND":
        "ক্রেতার তথ্য পাওয়া গেছে এবং তিনি বিক্রেতার থেকে ভিন্ন ব্যক্তি।",

    "BUYER_NOT_FOUND":
        "ক্রেতার তথ্য নিবন্ধিত ব্যক্তির তালিকায় পাওয়া যায়নি।",

    "PARCEL_FOUND":
        "ভূমি খণ্ডটি রেজিস্ট্রিতে পাওয়া গেছে।",

    "PARCEL_NOT_FOUND":
        "ভূমি খণ্ডটি রেজিস্ট্রিতে পাওয়া যায়নি।",

    "SELLER_IS_OWNER":
        "বিক্রেতা বর্তমানে এই ভূমি খণ্ডের সক্রিয় মালিক।",

    "AREA_AVAILABLE":
        "হস্তান্তরের পরিমাণ বিক্রেতার বর্তমান মালিকানার সীমার মধ্যে রয়েছে।",

    "INSUFFICIENT_OWNERSHIP":
        "বিক্রেতার মালিকানার তুলনায় বেশি জমি হস্তান্তরের চেষ্টা শনাক্ত হয়েছে।",

    "AREA_CHECK_NOT_APPLICABLE":
        "বিক্রেতার মালিকানা নিশ্চিত না হওয়ায় জমির পরিমাণ যাচাই প্রযোজ্য নয়।",

    "NO_PREVIOUS_SALE":
        "এই নির্দিষ্ট ভূমি অংশের পূর্ববর্তী বৈধ বিক্রয় পাওয়া যায়নি।",

    "DOUBLE_SALE":
        "একই নির্দিষ্ট ভূমি অংশের পূর্ববর্তী বৈধ বিক্রয়ের তথ্য পাওয়া গেছে।",

    "PORTION_ID_UNAVAILABLE":
        "ভূমি অংশ শনাক্ত করা না যাওয়ায় পুনরায় বিক্রির যাচাই সম্পূর্ণ নয়।",

    "MUTATION_MATCH":
        "দলিলের বিক্রেতা সক্রিয় নামজারি রেকর্ডের মালিকের সঙ্গে মিলে গেছে।",

    "DEED_MUTATION_MISMATCH":
        "দলিলের বিক্রেতা এবং সক্রিয় নামজারি মালিকের মধ্যে অমিল পাওয়া গেছে।",

    "NO_MUTATION_RECORD":
        "এই ভূমি অংশের জন্য উপযুক্ত নামজারি রেকর্ড পাওয়া যায়নি।",

    "INVALID_BUYER":
        "ক্রেতার তথ্য বৈধ নয়।",

    "INVALID_SELLER":
        "বিক্রেতার তথ্য বৈধ নয়।",
}


TRANSACTION_LABEL_BN = {
    "buyer_id":
        "ক্রেতা আইডি",

    "deed_id":
        "দলিল আইডি",

    "execution_date":
        "দলিল সম্পাদনের তারিখ",

    "parcel_id":
        "ভূমি খণ্ড আইডি",

    "portion_id":
        "ভূমি অংশ আইডি",

    "seller_id":
        "বিক্রেতা আইডি",

    "transaction_status":
        "লেনদেনের অবস্থা",

    "transferred_area_decimal":
        "হস্তান্তরিত জমি (শতক)",
}


# =========================================================
# TRANSLATION HELPERS
# =========================================================

def translate_value(value):
    if LANG == "en":
        return value

    return VALUE_BN.get(
        value,
        value,
    )


def translated_rule_name(rule_name):
    if LANG == "en":
        return rule_name

    return RULE_NAME_BN.get(
        rule_name,
        rule_name,
    )


def translated_rule_code(result):
    if LANG == "en":
        return result["code"]

    return RULE_CODE_BN.get(
        result["code"],
        result["code"],
    )


def translated_rule_message(result):
    if LANG == "en":
        return result["message"]

    return RULE_BN.get(
        result["code"],
        result["message"],
    )


def display_risk_level(level):
    if LANG == "en":
        return level

    mapping = {
        "LOW": "কম ঝুঁকি",
        "MEDIUM": "মাঝারি ঝুঁকি",
        "HIGH": "উচ্চ ঝুঁকি",
    }

    return mapping.get(
        level,
        level,
    )


# =========================================================
# DATAFRAME SCHEMAS
# =========================================================

HISTORY_COLUMNS = [
    "deed_id",
    "parcel_id",
    "portion_id",
    "transaction_status",
    "buyer_id",
]


MUTATION_COLUMNS = [
    "parcel_id",
    "portion_id",
    "mutation_owner_id",
    "status",
]


LEDGER_COLUMNS = [
    "ownership_id",
    "parcel_id",
    "owner_id",
    "owned_area_decimal",
    "status",
]


def empty_history():
    return pd.DataFrame(
        columns=HISTORY_COLUMNS
    )


# =========================================================
# CASE ID
# =========================================================

def create_case_id():

    date_part = (
        datetime.now()
        .strftime("%Y%m%d")
    )

    suffix = (
        uuid4()
        .hex[:6]
        .upper()
    )

    return (
        f"BG-{date_part}-{suffix}"
    )


# =========================================================
# DEMO DATA
# =========================================================

def demo_people():

    return pd.DataFrame(
        [
            {"person_id": "SELLER-SYN-001"},
            {"person_id": "SELLER-SYN-002"},
            {"person_id": "BUYER-SYN-001"},
            {"person_id": "PREVIOUS-BUYER-SYN-001"},
            {"person_id": "OTHER-OWNER-SYN-001"},
        ]
    )


def demo_parcels():

    return pd.DataFrame(
        [
            {
                "parcel_id":
                    "PARCEL-SYN-001"
            }
        ]
    )


def demo_ledger():

    return pd.DataFrame(
        [
            {
                "ownership_id":
                    "OWN-SYN-001",

                "parcel_id":
                    "PARCEL-SYN-001",

                "owner_id":
                    "SELLER-SYN-001",

                "owned_area_decimal":
                    10.5,

                "status":
                    "ACTIVE",
            }
        ]
    )


def demo_mutation(
    owner_id="SELLER-SYN-001"
):

    return pd.DataFrame(
        [
            {
                "parcel_id":
                    "PARCEL-SYN-001",

                "portion_id":
                    "PORTION-SYN-001",

                "mutation_owner_id":
                    owner_id,

                "status":
                    "ACTIVE",
            }
        ]
    )


def demo_transaction():

    return {
        "buyer_id":
            "BUYER-SYN-001",

        "deed_id":
            "DEED-SYN-001",

        "execution_date":
            "2026-10-16",

        "parcel_id":
            "PARCEL-SYN-001",

        "portion_id":
            "PORTION-SYN-001",

        "seller_id":
            "SELLER-SYN-001",

        "transaction_status":
            "PENDING",

        "transferred_area_decimal":
            5.5,
    }


# =========================================================
# DEMO DESCRIPTIONS
# =========================================================

DEMO_DESCRIPTION = {

    "CLEAR_BASELINE": {
        "bn":
            (
                "সব গুরুত্বপূর্ণ মালিকানা, ভূমি খণ্ড, "
                "লেনদেন ইতিহাস এবং নামজারি তথ্য "
                "পরস্পরের সঙ্গে সামঞ্জস্যপূর্ণ।"
            ),

        "en":
            (
                "Ownership, parcel, transaction history "
                "and mutation evidence are consistent."
            ),
    },


    "SELLER_NOT_OWNER": {
        "bn":
            (
                "বিক্রেতা রেজিস্ট্রিতে আছেন, কিন্তু "
                "এই ভূমি খণ্ডের বর্তমান মালিক নন।"
            ),

        "en":
            (
                "The seller exists in the registry "
                "but is not the current parcel owner."
            ),
    },


    "OVER_TRANSFER": {
        "bn":
            (
                "বিক্রেতা ৩.০ শতক মালিকানার বিপরীতে "
                "৫.৫ শতক হস্তান্তর করতে চান।"
            ),

        "en":
            (
                "The seller owns 3.0 decimal "
                "but attempts to transfer 5.5."
            ),
    },


    "DOUBLE_SALE": {
        "bn":
            (
                "একই শনাক্তকৃত ভূমি অংশের একটি "
                "পূর্ববর্তী বৈধ বিক্রয় রয়েছে।"
            ),

        "en":
            (
                "The same identified portion "
                "has a previous valid sale."
            ),
    },


    "DUPLICATE_DEED": {
        "bn":
            (
                "একই দলিল আইডি পূর্ববর্তী "
                "লেনদেন ইতিহাসে ইতোমধ্যে রয়েছে।"
            ),

        "en":
            (
                "The same deed identifier already "
                "exists in transaction history."
            ),
    },


    "MUTATION_MISMATCH": {
        "bn":
            (
                "দলিলের বিক্রেতা এবং সক্রিয় "
                "নামজারি মালিকের মধ্যে অমিল রয়েছে।"
            ),

        "en":
            (
                "The deed seller differs from "
                "the active mutation-side owner."
            ),
    },
}


# =========================================================
# BUILD DEMO SCENARIO
# =========================================================

def build_demo_scenario(name):

    transaction = demo_transaction()
    ledger_df = demo_ledger()
    history_df = empty_history()
    mutation_df = demo_mutation()


    if name == "SELLER_NOT_OWNER":

        transaction[
            "seller_id"
        ] = "SELLER-SYN-002"

        mutation_df = (
            demo_mutation(
                "SELLER-SYN-002"
            )
        )


    elif name == "OVER_TRANSFER":

        ledger_df.loc[
            0,
            "owned_area_decimal"
        ] = 3.0


    elif name == "DOUBLE_SALE":

        transaction[
            "deed_id"
        ] = "DEED-SYN-DOUBLE-001"

        history_df = pd.DataFrame(
            [
                {
                    "deed_id":
                        "DEED-PREV-001",

                    "parcel_id":
                        "PARCEL-SYN-001",

                    "portion_id":
                        "PORTION-SYN-001",

                    "transaction_status":
                        "VALID",

                    "buyer_id":
                        "PREVIOUS-BUYER-SYN-001",
                }
            ],
            columns=HISTORY_COLUMNS,
        )


    elif name == "DUPLICATE_DEED":

        history_df = pd.DataFrame(
            [
                {
                    "deed_id":
                        "DEED-SYN-001",

                    "parcel_id":
                        "PARCEL-SYN-001",

                    "portion_id":
                        "PORTION-OTHER-001",

                    "transaction_status":
                        "VALID",

                    "buyer_id":
                        "PREVIOUS-BUYER-SYN-001",
                }
            ],
            columns=HISTORY_COLUMNS,
        )


    elif name == "MUTATION_MISMATCH":

        mutation_df = (
            demo_mutation(
                "OTHER-OWNER-SYN-001"
            )
        )


    return {
        "description":
            DEMO_DESCRIPTION[name][LANG],

        "transaction":
            transaction,

        "ledger_df":
            ledger_df,

        "history_df":
            history_df,

        "mutation_df":
            mutation_df,

        "people_df":
            demo_people(),

        "parcels_df":
            demo_parcels(),
    }


# =========================================================
# CUSTOM CONTEXT BUILDER
# =========================================================

def build_custom_context(
    deed_id,
    execution_date,
    seller_id,
    buyer_id,
    parcel_id,
    portion_id,
    transferred_area,
    seller_exists,
    buyer_exists,
    parcel_exists,
    seller_is_owner,
    seller_owned_area,
    duplicate_deed,
    previous_same_portion_sale,
    mutation_available,
    mutation_owner_id,
):

    clean_portion = (
        portion_id.strip()
        if portion_id.strip()
        else None
    )


    transaction = {
        "buyer_id":
            buyer_id.strip(),

        "deed_id":
            deed_id.strip(),

        "execution_date":
            execution_date.isoformat(),

        "parcel_id":
            parcel_id.strip(),

        "portion_id":
            clean_portion,

        "seller_id":
            seller_id.strip(),

        "transaction_status":
            "PENDING",

        "transferred_area_decimal":
            float(transferred_area),
    }


    # -----------------------------------------------------
    # PEOPLE
    # -----------------------------------------------------

    people_rows = []

    if seller_exists:
        people_rows.append(
            {
                "person_id":
                    seller_id.strip()
            }
        )

    if buyer_exists:

        if (
            buyer_id.strip()
            not in
            [
                row["person_id"]
                for row in people_rows
            ]
        ):

            people_rows.append(
                {
                    "person_id":
                        buyer_id.strip()
                }
            )


    people_rows.append(
        {
            "person_id":
                "PREVIOUS-BUYER-CUSTOM"
        }
    )


    people_df = pd.DataFrame(
        people_rows,
        columns=["person_id"],
    )


    # -----------------------------------------------------
    # PARCEL
    # -----------------------------------------------------

    if parcel_exists:

        parcel_rows = [
            {
                "parcel_id":
                    parcel_id.strip()
            }
        ]

    else:

        parcel_rows = []


    parcels_df = pd.DataFrame(
        parcel_rows,
        columns=["parcel_id"],
    )


    # -----------------------------------------------------
    # LEDGER
    # -----------------------------------------------------

    if seller_is_owner:

        ledger_rows = [
            {
                "ownership_id":
                    "OWN-CUSTOM-SELLER",

                "parcel_id":
                    parcel_id.strip(),

                "owner_id":
                    seller_id.strip(),

                "owned_area_decimal":
                    float(seller_owned_area),

                "status":
                    "ACTIVE",
            }
        ]

    else:

        ledger_rows = [
            {
                "ownership_id":
                    "OWN-CUSTOM-OTHER",

                "parcel_id":
                    parcel_id.strip(),

                "owner_id":
                    "OTHER-OWNER-CUSTOM",

                "owned_area_decimal":
                    max(
                        float(seller_owned_area),
                        float(transferred_area),
                        1.0,
                    ),

                "status":
                    "ACTIVE",
            }
        ]


    ledger_df = pd.DataFrame(
        ledger_rows,
        columns=LEDGER_COLUMNS,
    )


    # -----------------------------------------------------
    # HISTORY
    # -----------------------------------------------------

    history_rows = []


    if duplicate_deed:

        history_rows.append(
            {
                "deed_id":
                    deed_id.strip(),

                "parcel_id":
                    parcel_id.strip(),

                "portion_id":
                    "OTHER-PORTION-CUSTOM",

                "transaction_status":
                    "VALID",

                "buyer_id":
                    "PREVIOUS-BUYER-CUSTOM",
            }
        )


    if previous_same_portion_sale:

        history_rows.append(
            {
                "deed_id":
                    "PREVIOUS-DEED-CUSTOM",

                "parcel_id":
                    parcel_id.strip(),

                "portion_id":
                    clean_portion,

                "transaction_status":
                    "VALID",

                "buyer_id":
                    "PREVIOUS-BUYER-CUSTOM",
            }
        )


    history_df = pd.DataFrame(
        history_rows,
        columns=HISTORY_COLUMNS,
    )


    # -----------------------------------------------------
    # MUTATION
    # -----------------------------------------------------

    mutation_rows = []


    if mutation_available:

        mutation_rows.append(
            {
                "parcel_id":
                    parcel_id.strip(),

                "portion_id":
                    clean_portion,

                "mutation_owner_id":
                    mutation_owner_id.strip(),

                "status":
                    "ACTIVE",
            }
        )


    mutation_df = pd.DataFrame(
        mutation_rows,
        columns=MUTATION_COLUMNS,
    )


    return {
        "transaction":
            transaction,

        "ledger_df":
            ledger_df,

        "history_df":
            history_df,

        "mutation_df":
            mutation_df,

        "people_df":
            people_df,

        "parcels_df":
            parcels_df,
    }


# =========================================================
# DISPLAY HELPERS
# =========================================================

def transaction_display_df(transaction):

    rows = []

    for key, value in (
        transaction.items()
    ):

        if LANG == "bn":
            label = (
                TRANSACTION_LABEL_BN.get(
                    key,
                    key,
                )
            )
        else:
            label = key


        if value is None:

            display_value = bi(
                "উপলব্ধ নয়",
                "Not available",
            )

        elif (
            LANG == "bn"
            and
            key in {
                "execution_date",
                "transferred_area_decimal",
            }
        ):

            display_value = (
                local_number(value)
            )

        else:

            display_value = (
                translate_value(value)
            )


        rows.append(
            {
                bi(
                    "তথ্য",
                    "Field"
                ):
                    label,

                bi(
                    "মান",
                    "Value"
                ):
                    display_value,
            }
        )


    return pd.DataFrame(rows)


def display_ledger_df(df):

    result = df.copy()

    if LANG == "bn":

        result = result.rename(
            columns={
                "ownership_id":
                    "মালিকানা আইডি",

                "parcel_id":
                    "ভূমি খণ্ড",

                "owner_id":
                    "মালিক",

                "owned_area_decimal":
                    "মালিকানাধীন জমি (শতক)",

                "status":
                    "অবস্থা",
            }
        )


        area_col = (
            "মালিকানাধীন জমি (শতক)"
        )


        if area_col in result.columns:

            result[
                area_col
            ] = (
                result[
                    area_col
                ]
                .map(local_number)
            )


        if "অবস্থা" in result.columns:

            result[
                "অবস্থা"
            ] = (
                result[
                    "অবস্থা"
                ]
                .map(translate_value)
            )


    return result


def display_history_df(df):

    result = df.copy()

    if LANG == "bn":

        result = result.rename(
            columns={
                "deed_id":
                    "দলিল আইডি",

                "parcel_id":
                    "ভূমি খণ্ড",

                "portion_id":
                    "ভূমি অংশ",

                "transaction_status":
                    "অবস্থা",

                "buyer_id":
                    "ক্রেতা",
            }
        )


        if "অবস্থা" in result.columns:

            result[
                "অবস্থা"
            ] = (
                result[
                    "অবস্থা"
                ]
                .map(translate_value)
            )


    return result


def display_mutation_df(df):

    result = df.copy()

    if LANG == "bn":

        result = result.rename(
            columns={
                "parcel_id":
                    "ভূমি খণ্ড",

                "portion_id":
                    "ভূমি অংশ",

                "mutation_owner_id":
                    "নামজারি মালিক",

                "status":
                    "অবস্থা",
            }
        )


        if "অবস্থা" in result.columns:

            result[
                "অবস্থা"
            ] = (
                result[
                    "অবস্থা"
                ]
                .map(translate_value)
            )


    return result


# =========================================================
# DOWNLOAD REPORT
# =========================================================

def build_download_report(
    case_id,
    report,
    transaction,
):

    lines = [
        "BHUMIGUARD BD",
        "=" * 60,

        (
            f"{bi('স্ক্রিনিং আইডি', 'Screening ID')}: "
            f"{case_id}"
        ),

        "",

        (
            f"{bi('দলিল আইডি', 'Deed ID')}: "
            f"{transaction['deed_id']}"
        ),

        (
            f"{bi('ভূমি খণ্ড', 'Parcel')}: "
            f"{transaction['parcel_id']}"
        ),

        (
            f"{bi('ভূমি অংশ', 'Portion')}: "
            f"{transaction['portion_id']}"
        ),

        (
            f"{bi('বিক্রেতা', 'Seller')}: "
            f"{transaction['seller_id']}"
        ),

        (
            f"{bi('ক্রেতা', 'Buyer')}: "
            f"{transaction['buyer_id']}"
        ),

        (
            f"{bi('হস্তান্তরিত জমি', 'Transfer Area')}: "
            f"{local_number(transaction['transferred_area_decimal'])} "
            f"{bi('শতক', 'decimal')}"
        ),

        "",

        (
            f"{bi('সামগ্রিক ঝুঁকি', 'Overall Risk')}: "
            f"{display_risk_level(report['risk_level'])}"
        ),

        "",

        bi(
            "নিয়মভিত্তিক যাচাই",
            "Rule Checks",
        ),

        "-" * 60,
    ]


    for rule_name, result in (
        report["rules"].items()
    ):

        lines.append(
            (
                f"{translate_value(result['status'])} | "
                f"{translated_rule_name(rule_name)} | "
                f"{translated_rule_code(result)}"
            )
        )

        lines.append(
            f"  {translated_rule_message(result)}"
        )


    lines.extend(
        [
            "",
            "-" * 60,

            bi(
                (
                    "এই ফলাফল শুধুমাত্র প্রাথমিক ঝুঁকি যাচাইয়ের "
                    "জন্য। এটি আইনগত মালিকানা প্রতিষ্ঠা করে না "
                    "এবং প্রতারণা প্রমাণ করে না।"
                ),
                (
                    "Screening result only. It does not "
                    "establish legal title or prove fraud."
                ),
            ),
        ]
    )


    return "\n".join(lines)


# =========================================================
# RULE CARD
# =========================================================

def render_rule_card(
    rule_name,
    result,
):

    status = result[
        "status"
    ]


    if status == "PASS":

        css_class = (
            "rule-pass"
        )

        icon = "✓"


    elif status == "WARNING":

        css_class = (
            "rule-warning"
        )

        icon = "⚠"


    else:

        css_class = (
            "rule-fail"
        )

        icon = "✕"


    render_html(
        f"""
        <div class="rule-card {css_class}">
            <div class="rule-name">
                {icon} {translated_rule_name(rule_name)}
            </div>

            <div class="rule-code">
                {translated_rule_code(result)}
            </div>

            <div class="rule-message">
                {translated_rule_message(result)}
            </div>
        </div>
        """
    )


# =========================================================
# SCREENING RESULT RENDERER
# =========================================================

def render_screening_result(bundle):

    case_id = bundle[
        "case_id"
    ]

    report = bundle[
        "report"
    ]

    context = bundle[
        "context"
    ]

    transaction = context[
        "transaction"
    ]

    level = report[
        "risk_level"
    ]


    # -----------------------------------------------------
    # RESULT HEADER
    # -----------------------------------------------------

    render_html(
        f"""
        <div class="section-card">
            <div class="section-kicker">
                {bi("ধাপ ৩", "STEP 3")}
            </div>

            <div class="section-title">
                {bi(
                    "ঝুঁকি যাচাইয়ের ফলাফল",
                    "Screening Result"
                )}
            </div>

            <div class="section-description">
                {bi("স্ক্রিনিং আইডি", "Screening ID")}:
                <b>{case_id}</b>
            </div>
        </div>
        """
    )


    # -----------------------------------------------------
    # RISK CARD
    # -----------------------------------------------------

    if level == "LOW":

        risk_class = (
            "risk-low"
        )

        risk_icon = "🟢"

        risk_description = bi(
            (
                "এই লেনদেনে কোনো গুরুত্বপূর্ণ "
                "blocking anomaly শনাক্ত হয়নি।"
            ),
            (
                "No blocking anomaly was detected "
                "in this screening."
            ),
        )


    elif level == "MEDIUM":

        risk_class = (
            "risk-medium"
        )

        risk_icon = "🟡"

        risk_description = bi(
            (
                "কিছু প্রমাণ অসম্পূর্ণ অথবা "
                "আরও যাচাই প্রয়োজন।"
            ),
            (
                "Some evidence is incomplete "
                "or requires further review."
            ),
        )


    else:

        risk_class = (
            "risk-high"
        )

        risk_icon = "🔴"

        risk_description = bi(
            (
                "এক বা একাধিক গুরুত্বপূর্ণ "
                "অসঙ্গতি শনাক্ত হয়েছে।"
            ),
            (
                "One or more important "
                "inconsistencies were detected."
            ),
        )


    render_html(
        f"""
        <div class="risk-card {risk_class}">
            <div class="risk-title">
                {risk_icon} {display_risk_level(level)}
            </div>

            <div class="risk-description">
                {risk_description}
            </div>
        </div>
        """
    )


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    c1, c2, c3, c4 = (
        st.columns(4)
    )


    c1.metric(
        bi(
            "সামগ্রিক ঝুঁকি",
            "Overall Risk"
        ),
        display_risk_level(level),
    )


    c2.metric(
        bi(
            "সফল",
            "Passed"
        ),
        local_number(
            report["pass_count"]
        ),
    )


    c3.metric(
        bi(
            "সতর্কতা",
            "Warnings"
        ),
        local_number(
            report["warning_count"]
        ),
    )


    c4.metric(
        bi(
            "ব্যর্থ",
            "Failed"
        ),
        local_number(
            report["fail_count"]
        ),
    )


    # -----------------------------------------------------
    # SPLIT RULES
    # -----------------------------------------------------

    failed_rules = []
    warning_rules = []
    passed_rules = []


    for rule_name, result in (
        report["rules"].items()
    ):

        if result["status"] == "FAIL":

            failed_rules.append(
                (
                    rule_name,
                    result,
                )
            )

        elif result["status"] == "WARNING":

            warning_rules.append(
                (
                    rule_name,
                    result,
                )
            )

        else:

            passed_rules.append(
                (
                    rule_name,
                    result,
                )
            )


    # -----------------------------------------------------
    # FAIL + WARNING FIRST
    # -----------------------------------------------------

    if (
        failed_rules
        or
        warning_rules
    ):

        st.subheader(
            bi(
                "গুরুত্বপূর্ণ ঝুঁকি ও সতর্কতা",
                "Important Risks & Warnings",
            )
        )


        for rule_name, result in (
            failed_rules
            +
            warning_rules
        ):

            render_rule_card(
                rule_name,
                result,
            )


    # -----------------------------------------------------
    # PASSED CHECKS
    # -----------------------------------------------------

    with st.expander(
        (
            f"✓ "
            f"{bi('সফল যাচাইসমূহ', 'Passed Checks')} "
            f"({local_number(len(passed_rules))})"
        ),
        expanded=(
            level == "LOW"
        ),
    ):

        for rule_name, result in (
            passed_rules
        ):

            render_rule_card(
                rule_name,
                result,
            )


    # -----------------------------------------------------
    # EVIDENCE TABS
    # -----------------------------------------------------

    st.subheader(
        bi(
            "প্রমাণ ও রেকর্ড",
            "Evidence & Records",
        )
    )


    (
        ownership_tab,
        history_tab,
        mutation_tab,
    ) = st.tabs(
        [
            bi(
                "👤 মালিকানা",
                "👤 Ownership",
            ),

            bi(
                "📜 লেনদেন ইতিহাস",
                "📜 History",
            ),

            bi(
                "🏛️ নামজারি",
                "🏛️ Mutation",
            ),
        ]
    )


    with ownership_tab:

        st.dataframe(
            display_ledger_df(
                context["ledger_df"]
            ),
            use_container_width=True,
            hide_index=True,
        )


    with history_tab:

        if context[
            "history_df"
        ].empty:

            st.info(
                bi(
                    (
                        "কোনো পূর্ববর্তী বৈধ "
                        "লেনদেন পাওয়া যায়নি।"
                    ),
                    (
                        "No previous transaction "
                        "history was found."
                    ),
                )
            )

        else:

            st.dataframe(
                display_history_df(
                    context[
                        "history_df"
                    ]
                ),
                use_container_width=True,
                hide_index=True,
            )


    with mutation_tab:

        if context[
            "mutation_df"
        ].empty:

            st.warning(
                bi(
                    (
                        "কোনো সক্রিয় নামজারি "
                        "রেকর্ড দেওয়া হয়নি।"
                    ),
                    (
                        "No active mutation "
                        "record was provided."
                    ),
                )
            )

        else:

            st.dataframe(
                display_mutation_df(
                    context[
                        "mutation_df"
                    ]
                ),
                use_container_width=True,
                hide_index=True,
            )


    # -----------------------------------------------------
    # DOWNLOAD
    # -----------------------------------------------------

    report_text = (
        build_download_report(
            case_id,
            report,
            transaction,
        )
    )


    st.download_button(
        label=bi(
            "⬇ স্ক্রিনিং রিপোর্ট ডাউনলোড করুন",
            "⬇ Download Screening Report",
        ),
        data=report_text,
        file_name=(
            f"{case_id}_"
            "BhumiGuard_Report.txt"
        ),
        mime="text/plain",
        use_container_width=True,
    )


    st.caption(
        bi(
            (
                "এই ফলাফল সিদ্ধান্ত-সহায়ক screening মাত্র; "
                "এটি আইনগত মালিকানা নির্ধারণ বা প্রতারণা "
                "প্রমাণ করে না।"
            ),
            (
                "This is a decision-support screening result; "
                "it does not establish legal title or prove fraud."
            ),
        )
    )


# =========================================================
# HERO
# =========================================================

render_html(
    f"""
    <div class="hero-card">

        <div class="hero-title">
            🏡 {bi(
                "ভূমিগার্ড বিডি",
                "BhumiGuard BD"
            )}
        </div>

        <div class="hero-subtitle">
            {bi(
                "এআই-সহায়িত প্রাক-নিবন্ধন ভূমি লেনদেন ঝুঁকি যাচাই",
                "AI-Assisted Pre-Registration Land Transaction Risk Screening"
            )}
        </div>

        <div class="hero-tagline">
            {bi(
                "শুধু দলিল নয় — লেনদেনের ইতিহাসও যাচাই",
                "Verify the transaction, not just the document"
            )}
        </div>

        <div class="hero-badge">
            ● Live Prototype
        </div>

    </div>
    """
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    f"### {bi('যাচাই পদ্ধতি', 'Screening Mode')}"
)


mode = st.sidebar.radio(
    bi(
        "একটি পদ্ধতি নির্বাচন করুন",
        "Choose a screening mode",
    ),
    [
        bi(
            "প্রস্তুত ডেমো",
            "Validated Demo",
        ),

        bi(
            "কাস্টম লেনদেন",
            "Custom Transaction",
        ),
    ],
)


DEMO_MODE = (
    mode
    ==
    bi(
        "প্রস্তুত ডেমো",
        "Validated Demo",
    )
)


st.sidebar.divider()


st.sidebar.caption(
    bi(
        (
            "Public demo-তে প্রকৃত NID, ফোন নম্বর "
            "বা গোপন ভূমি রেকর্ড ব্যবহার করবেন না।"
        ),
        (
            "Do not enter real NIDs, phone numbers "
            "or confidential land records."
        ),
    )
)


# =========================================================
# DEMO MODE
# =========================================================

if DEMO_MODE:

    if LANG == "bn":

        demo_labels = {
            "স্বাভাবিক বৈধ লেনদেন":
                "CLEAR_BASELINE",

            "বিক্রেতা প্রকৃত মালিক নন":
                "SELLER_NOT_OWNER",

            "মালিকানার চেয়ে বেশি জমি বিক্রি":
                "OVER_TRANSFER",

            "একই জমি পুনরায় বিক্রির ঝুঁকি":
                "DOUBLE_SALE",

            "একই দলিল নম্বর পুনরায় ব্যবহার":
                "DUPLICATE_DEED",

            "দলিল ও নামজারি তথ্যে অমিল":
                "MUTATION_MISMATCH",
        }

    else:

        demo_labels = {
            "Clear Baseline":
                "CLEAR_BASELINE",

            "Seller Not Owner":
                "SELLER_NOT_OWNER",

            "Over Transfer":
                "OVER_TRANSFER",

            "Double Sale":
                "DOUBLE_SALE",

            "Duplicate Deed":
                "DUPLICATE_DEED",

            "Mutation Mismatch":
                "MUTATION_MISMATCH",
        }


    selected_label = (
        st.sidebar.selectbox(
            bi(
                "ডেমো পরিস্থিতি",
                "Demo Scenario",
            ),
            list(
                demo_labels.keys()
            ),
        )
    )


    scenario_name = (
        demo_labels[
            selected_label
        ]
    )


    # -----------------------------------------------------
    # CLEAR STALE RESULT
    # -----------------------------------------------------

    if (
        st.session_state.get(
            "last_demo"
        )
        !=
        scenario_name
    ):

        st.session_state[
            "last_demo"
        ] = scenario_name

        st.session_state.pop(
            "demo_result",
            None,
        )


    context = (
        build_demo_scenario(
            scenario_name
        )
    )

    transaction = context[
        "transaction"
    ]


    # =====================================================
    # STEP 1
    # =====================================================

    render_html(
        f"""
        <div class="section-card">

            <div class="section-kicker">
                {bi("ধাপ ১", "STEP 1")}
            </div>

            <div class="section-title">
                {bi(
                    "লেনদেনের সারসংক্ষেপ",
                    "Transaction Overview"
                )}
            </div>

            <div class="section-description">
                {context["description"]}
            </div>

        </div>
        """
    )


    c1, c2, c3, c4 = (
        st.columns(4)
    )


    c1.metric(
        bi(
            "দলিল আইডি",
            "Deed ID"
        ),
        transaction["deed_id"],
    )


    c2.metric(
        bi(
            "ভূমি খণ্ড",
            "Parcel"
        ),
        transaction["parcel_id"],
    )


    c3.metric(
        bi(
            "হস্তান্তরিত জমি",
            "Transfer Area"
        ),
        (
            f"{local_number(transaction['transferred_area_decimal'])} "
            f"{bi('শতক', 'decimal')}"
        ),
    )


    c4.metric(
        bi(
            "ভূমি অংশ",
            "Portion"
        ),
        transaction["portion_id"],
    )


    with st.expander(
        bi(
            "লেনদেনের সব তথ্য দেখুন",
            "View all transaction fields",
        )
    ):

        st.dataframe(
            transaction_display_df(
                transaction
            ),
            use_container_width=True,
            hide_index=True,
        )


    # =====================================================
    # STEP 2
    # =====================================================

    render_html(
        f"""
        <div class="section-card">

            <div class="section-kicker">
                {bi("ধাপ ২", "STEP 2")}
            </div>

            <div class="section-title">
                {bi(
                    "প্রাক-নিবন্ধন ঝুঁকি যাচাই",
                    "Pre-Registration Screening"
                )}
            </div>

            <div class="section-description">
                {bi(
                    "Validated backend risk engine ব্যবহার করে এই লেনদেন যাচাই করা হবে।",
                    "This transaction will be screened using the validated backend risk engine."
                )}
            </div>

        </div>
        """
    )


    if st.button(
        bi(
            "🔍 এখন লেনদেন যাচাই করুন",
            "🔍 Screen This Transaction",
        ),
        type="primary",
        use_container_width=True,
        key="demo_verify",
    ):

        report = (
            risk.verify_transaction(
                context["ledger_df"],
                context["history_df"],
                context["mutation_df"],
                transaction,
                context["people_df"],
                context["parcels_df"],
            )
        )


        st.session_state[
            "demo_result"
        ] = {
            "case_id":
                create_case_id(),

            "report":
                report,

            "context":
                context,
        }


    if (
        "demo_result"
        in
        st.session_state
    ):

        render_screening_result(
            st.session_state[
                "demo_result"
            ]
        )


# =========================================================
# CUSTOM TRANSACTION MODE
# =========================================================

else:

    render_html(
        f"""
        <div class="section-card">

            <div class="section-kicker">
                {bi(
                    "ইন্টারেক্টিভ মোড",
                    "INTERACTIVE MODE"
                )}
            </div>

            <div class="section-title">
                {bi(
                    "নিজের test transaction তৈরি করুন",
                    "Build Your Own Test Transaction"
                )}
            </div>

            <div class="section-description">
                {bi(
                    "Synthetic/test identifiers ব্যবহার করে মালিকানা, ইতিহাস ও নামজারি প্রমাণ পরিবর্তন করে একই risk engine পরীক্ষা করুন।",
                    "Use synthetic/test identifiers and configure ownership, history and mutation evidence to test the same risk engine."
                )}
            </div>

        </div>
        """
    )


    st.warning(
        bi(
            (
                "⚠ Public demo-তে প্রকৃত NID, ফোন নম্বর "
                "বা confidential ভূমি তথ্য দেবেন না।"
            ),
            (
                "⚠ Do not enter real NIDs, phone numbers "
                "or confidential land information."
            ),
        )
    )


    # =====================================================
    # CUSTOM FORM
    # =====================================================

    with st.form(
        "custom_screening_form"
    ):

        (
            transaction_tab,
            ownership_tab,
            history_tab,
            mutation_tab,
        ) = st.tabs(
            [
                bi(
                    "📝 লেনদেন",
                    "📝 Transaction"
                ),

                bi(
                    "👤 মালিকানা",
                    "👤 Ownership"
                ),

                bi(
                    "📜 ইতিহাস",
                    "📜 History"
                ),

                bi(
                    "🏛️ নামজারি",
                    "🏛️ Mutation"
                ),
            ]
        )


        # -------------------------------------------------
        # TRANSACTION
        # -------------------------------------------------

        with transaction_tab:

            c1, c2 = (
                st.columns(2)
            )


            deed_id = (
                c1.text_input(
                    bi(
                        "দলিল আইডি",
                        "Deed ID"
                    ),
                    value=
                        "DEED-CUSTOM-001",
                )
            )


            execution_date = (
                c2.date_input(
                    bi(
                        "দলিল সম্পাদনের তারিখ",
                        "Execution Date",
                    )
                )
            )


            c1, c2 = (
                st.columns(2)
            )


            seller_id = (
                c1.text_input(
                    bi(
                        "বিক্রেতা আইডি",
                        "Seller ID"
                    ),
                    value=
                        "SELLER-CUSTOM-001",
                )
            )


            buyer_id = (
                c2.text_input(
                    bi(
                        "ক্রেতা আইডি",
                        "Buyer ID"
                    ),
                    value=
                        "BUYER-CUSTOM-001",
                )
            )


            c1, c2 = (
                st.columns(2)
            )


            parcel_id = (
                c1.text_input(
                    bi(
                        "ভূমি খণ্ড আইডি",
                        "Parcel ID"
                    ),
                    value=
                        "PARCEL-CUSTOM-001",
                )
            )


            portion_id = (
                c2.text_input(
                    bi(
                        "ভূমি অংশ আইডি",
                        "Portion ID"
                    ),
                    value=
                        "PORTION-CUSTOM-001",
                    help=
                        bi(
                            (
                                "নির্ভরযোগ্য schedule, boundary "
                                "বা share evidence থেকে নির্ধারিত "
                                "হওয়া উচিত।"
                            ),
                            (
                                "Should come from reliable schedule, "
                                "boundary or share evidence."
                            ),
                        ),
                )
            )


            transferred_area = (
                st.number_input(
                    bi(
                        "হস্তান্তরিত জমি (শতক)",
                        "Transfer Area (decimal)",
                    ),
                    min_value=
                        0.01,
                    value=
                        5.5,
                    step=
                        0.5,
                )
            )


            st.markdown(
                "**"
                +
                bi(
                    "রেজিস্ট্রি উপস্থিতি",
                    "Registry Presence"
                )
                +
                "**"
            )


            c1, c2, c3 = (
                st.columns(3)
            )


            seller_exists = (
                c1.checkbox(
                    bi(
                        "বিক্রেতা রেজিস্ট্রিতে আছেন",
                        "Seller exists",
                    ),
                    value=True,
                )
            )


            buyer_exists = (
                c2.checkbox(
                    bi(
                        "ক্রেতা রেজিস্ট্রিতে আছেন",
                        "Buyer exists",
                    ),
                    value=True,
                )
            )


            parcel_exists = (
                c3.checkbox(
                    bi(
                        "ভূমি খণ্ড রেজিস্ট্রিতে আছে",
                        "Parcel exists",
                    ),
                    value=True,
                )
            )


        # -------------------------------------------------
        # OWNERSHIP
        # -------------------------------------------------

        with ownership_tab:

            seller_is_owner = (
                st.checkbox(
                    bi(
                        "বিক্রেতা বর্তমান সক্রিয় মালিক",
                        "Seller is the current active owner",
                    ),
                    value=True,
                )
            )


            seller_owned_area = (
                st.number_input(
                    bi(
                        "বিক্রেতার মালিকানাধীন জমি (শতক)",
                        "Seller-owned Area (decimal)",
                    ),
                    min_value=
                        0.0,
                    value=
                        10.5,
                    step=
                        0.5,
                )
            )


            st.caption(
                bi(
                    (
                        "হস্তান্তরের পরিমাণ বিক্রেতার মালিকানাধীন "
                        "জমির চেয়ে বেশি হলে over-transfer risk "
                        "শনাক্ত হবে।"
                    ),
                    (
                        "If the requested transfer exceeds the "
                        "seller-owned area, an over-transfer risk "
                        "will be triggered."
                    ),
                )
            )


        # -------------------------------------------------
        # HISTORY
        # -------------------------------------------------

        with history_tab:

            duplicate_deed = (
                st.checkbox(
                    bi(
                        "একই দলিল আইডি আগে ব্যবহৃত হয়েছে",
                        "Same deed ID already exists",
                    ),
                    value=False,
                )
            )


            previous_same_portion_sale = (
                st.checkbox(
                    bi(
                        (
                            "একই শনাক্তকৃত ভূমি অংশ আগে "
                            "বৈধভাবে বিক্রি হয়েছে"
                        ),
                        (
                            "Same identified portion has "
                            "a previous valid sale"
                        ),
                    ),
                    value=False,
                )
            )


            st.caption(
                bi(
                    (
                        "Double-sale screening শুধু জমির "
                        "পরিমাণের উপর নয়; নির্দিষ্ট ভূমি অংশের "
                        "evidence-এর উপর নির্ভর করে।"
                    ),
                    (
                        "Double-sale screening depends on "
                        "identified portion evidence, not area alone."
                    ),
                )
            )


        # -------------------------------------------------
        # MUTATION
        # -------------------------------------------------

        with mutation_tab:

            mutation_available = (
                st.checkbox(
                    bi(
                        "সক্রিয় নামজারি রেকর্ড আছে",
                        "Active mutation record available",
                    ),
                    value=True,
                )
            )


            mutation_owner_id = (
                st.text_input(
                    bi(
                        "নামজারি মালিক আইডি",
                        "Mutation-side Owner ID",
                    ),
                    value=
                        "SELLER-CUSTOM-001",
                    disabled=(
                        not mutation_available
                    ),
                )
            )


            st.caption(
                bi(
                    (
                        "নামজারি অমিল একটি risk signal; "
                        "এটি প্রতারণার আইনি প্রমাণ নয়।"
                    ),
                    (
                        "A mutation mismatch is a risk signal, "
                        "not legal proof of fraud."
                    ),
                )
            )


        # -------------------------------------------------
        # SUBMIT
        # -------------------------------------------------

        custom_submit = (
            st.form_submit_button(
                bi(
                    "🔍 কাস্টম লেনদেন যাচাই করুন",
                    "🔍 Screen Custom Transaction",
                ),
                type="primary",
                use_container_width=True,
            )
        )


    # =====================================================
    # CUSTOM SUBMISSION
    # =====================================================

    if custom_submit:

        errors = []


        if not deed_id.strip():

            errors.append(
                bi(
                    "দলিল আইডি আবশ্যক।",
                    "Deed ID is required.",
                )
            )


        if not seller_id.strip():

            errors.append(
                bi(
                    "বিক্রেতা আইডি আবশ্যক।",
                    "Seller ID is required.",
                )
            )


        if not buyer_id.strip():

            errors.append(
                bi(
                    "ক্রেতা আইডি আবশ্যক।",
                    "Buyer ID is required.",
                )
            )


        if not parcel_id.strip():

            errors.append(
                bi(
                    "ভূমি খণ্ড আইডি আবশ্যক।",
                    "Parcel ID is required.",
                )
            )


        if errors:

            for error in errors:
                st.error(error)


        else:

            context = (
                build_custom_context(
                    deed_id=
                        deed_id,

                    execution_date=
                        execution_date,

                    seller_id=
                        seller_id,

                    buyer_id=
                        buyer_id,

                    parcel_id=
                        parcel_id,

                    portion_id=
                        portion_id,

                    transferred_area=
                        transferred_area,

                    seller_exists=
                        seller_exists,

                    buyer_exists=
                        buyer_exists,

                    parcel_exists=
                        parcel_exists,

                    seller_is_owner=
                        seller_is_owner,

                    seller_owned_area=
                        seller_owned_area,

                    duplicate_deed=
                        duplicate_deed,

                    previous_same_portion_sale=
                        previous_same_portion_sale,

                    mutation_available=
                        mutation_available,

                    mutation_owner_id=
                        mutation_owner_id,
                )
            )


            try:

                report = (
                    risk.verify_transaction(
                        context[
                            "ledger_df"
                        ],

                        context[
                            "history_df"
                        ],

                        context[
                            "mutation_df"
                        ],

                        context[
                            "transaction"
                        ],

                        context[
                            "people_df"
                        ],

                        context[
                            "parcels_df"
                        ],
                    )
                )


                st.session_state[
                    "custom_result"
                ] = {
                    "case_id":
                        create_case_id(),

                    "report":
                        report,

                    "context":
                        context,
                }


            except Exception as error:

                st.error(
                    bi(
                        (
                            "Screening সম্পন্ন করা যায়নি। "
                            "Input এবং evidence configuration "
                            "যাচাই করুন।"
                        ),
                        (
                            "Screening could not be completed. "
                            "Please review the input and evidence "
                            "configuration."
                        ),
                    )
                )


                with st.expander(
                    "Technical error"
                ):

                    st.code(
                        str(error)
                    )


    # =====================================================
    # CUSTOM RESULT
    # =====================================================

    if (
        "custom_result"
        in
        st.session_state
    ):

        transaction = (
            st.session_state[
                "custom_result"
            ][
                "context"
            ][
                "transaction"
            ]
        )


        with st.expander(
            bi(
                "সাবমিট করা লেনদেনের তথ্য",
                "Submitted Transaction",
            )
        ):

            st.dataframe(
                transaction_display_df(
                    transaction
                ),
                use_container_width=True,
                hide_index=True,
            )


        render_screening_result(
            st.session_state[
                "custom_result"
            ]
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()


render_html(
    f"""
    <div class="footer-note">
        BhumiGuard BD • LandTech 2026 Prototype
        <br>
        {bi(
            "সিদ্ধান্ত-সহায়ক ব্যবস্থা — আইনগত মালিকানা নির্ধারণের ব্যবস্থা নয়।",
            "Decision-support system — not legal title determination."
        )}
    </div>
    """
)
