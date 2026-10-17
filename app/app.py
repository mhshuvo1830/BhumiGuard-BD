from pathlib import Path
from datetime import datetime
from uuid import uuid4
import sys

import pandas as pd
import streamlit as st


# =========================================================
# 1. PROJECT SETUP
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from bhumiguard import risk


# =========================================================
# 2. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ভূমিগার্ড বিডি | BhumiGuard BD",
    page_icon="🏡",
    layout="wide",
)


# =========================================================
# 3. UI STYLE
# =========================================================

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family:
            "Noto Sans Bengali",
            "Hind Siliguri",
            "SolaimanLipi",
            "Kalpurush",
            Arial,
            sans-serif;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    div[data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 4. LANGUAGE
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
# 5. BANGLA DIGITS
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
# 6. GENERAL TRANSLATIONS
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


def translate_value(value):

    if LANG == "en":
        return value

    return VALUE_BN.get(
        value,
        value,
    )


# =========================================================
# 7. RULE TRANSLATIONS
# =========================================================

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
        "বিক্রেতা মালিক নন",

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
        "হস্তান্তরের জন্য পর্যাপ্ত জমি আছে",

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
        (
            "দলিল নম্বরটি পূর্ববর্তী রেকর্ডে "
            "পুনরায় পাওয়া যায়নি।"
        ),

    "DUPLICATE_DEED":
        (
            "একই দলিল নম্বর পূর্ববর্তী লেনদেনের "
            "রেকর্ডে ইতোমধ্যে রয়েছে।"
        ),

    "SELLER_FOUND":
        (
            "বিক্রেতার তথ্য নিবন্ধিত ব্যক্তির "
            "তালিকায় পাওয়া গেছে।"
        ),

    "SELLER_NOT_FOUND":
        (
            "বিক্রেতার তথ্য নিবন্ধিত ব্যক্তির "
            "তালিকায় পাওয়া যায়নি।"
        ),

    "SELLER_NOT_OWNER":
        (
            "বিক্রেতা এই ভূমি খণ্ডের বর্তমান "
            "মালিক হিসেবে পাওয়া যায়নি।"
        ),

    "BUYER_FOUND":
        (
            "ক্রেতার তথ্য পাওয়া গেছে এবং তিনি "
            "বিক্রেতার থেকে ভিন্ন ব্যক্তি।"
        ),

    "BUYER_NOT_FOUND":
        (
            "ক্রেতার তথ্য নিবন্ধিত ব্যক্তির "
            "তালিকায় পাওয়া যায়নি।"
        ),

    "PARCEL_FOUND":
        "ভূমি খণ্ডটি রেজিস্ট্রিতে পাওয়া গেছে।",

    "PARCEL_NOT_FOUND":
        "ভূমি খণ্ডটি রেজিস্ট্রিতে পাওয়া যায়নি।",

    "SELLER_IS_OWNER":
        (
            "বিক্রেতা বর্তমানে এই ভূমি খণ্ডের "
            "মালিক হিসেবে নিবন্ধিত।"
        ),

    "AREA_AVAILABLE":
        (
            "হস্তান্তরের পরিমাণ বিক্রেতার বর্তমান "
            "মালিকানার সীমার মধ্যে রয়েছে।"
        ),

    "INSUFFICIENT_OWNERSHIP":
        (
            "বিক্রেতার বর্তমান মালিকানার তুলনায় "
            "বেশি জমি হস্তান্তরের চেষ্টা শনাক্ত হয়েছে।"
        ),

    "AREA_CHECK_NOT_APPLICABLE":
        (
            "বিক্রেতার মালিকানা নিশ্চিত না হওয়ায় "
            "জমির পরিমাণ যাচাই প্রযোজ্য নয়।"
        ),

    "NO_PREVIOUS_SALE":
        (
            "এই নির্দিষ্ট ভূমি অংশের পূর্ববর্তী "
            "বৈধ বিক্রয় পাওয়া যায়নি।"
        ),

    "DOUBLE_SALE":
        (
            "একই নির্দিষ্ট ভূমি অংশের পূর্ববর্তী "
            "বৈধ বিক্রয়ের তথ্য পাওয়া গেছে।"
        ),

    "PORTION_ID_UNAVAILABLE":
        (
            "ভূমির নির্দিষ্ট অংশ শনাক্ত করা না যাওয়ায় "
            "পুনরায় বিক্রির যাচাই সম্পূর্ণ করা যায়নি।"
        ),

    "MUTATION_MATCH":
        (
            "দলিলের বিক্রেতা সক্রিয় নামজারি "
            "রেকর্ডের মালিকের সঙ্গে মিলে গেছে।"
        ),

    "DEED_MUTATION_MISMATCH":
        (
            "দলিলের বিক্রেতা এবং সক্রিয় নামজারি "
            "রেকর্ডের মালিকের মধ্যে অমিল পাওয়া গেছে।"
        ),

    "NO_MUTATION_RECORD":
        (
            "এই ভূমি অংশের জন্য উপযুক্ত "
            "নামজারি রেকর্ড পাওয়া যায়নি।"
        ),

    "INVALID_BUYER":
        "ক্রেতার তথ্য বৈধ নয়।",

    "INVALID_SELLER":
        "বিক্রেতার তথ্য বৈধ নয়।",
}


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


# =========================================================
# 8. RISK HELPERS
# =========================================================

def display_risk_level(risk_level):

    if LANG == "en":
        return risk_level

    mapping = {
        "LOW": "কম ঝুঁকি",
        "MEDIUM": "মাঝারি ঝুঁকি",
        "HIGH": "উচ্চ ঝুঁকি",
    }

    return mapping.get(
        risk_level,
        risk_level,
    )


def show_risk_banner(risk_level):

    if LANG == "bn":

        if risk_level == "LOW":

            st.success(
                "✅ কম ঝুঁকি — এই যাচাইয়ে কোনো "
                "গুরুতর অসঙ্গতি পাওয়া যায়নি।"
            )

        elif risk_level == "MEDIUM":

            st.warning(
                "⚠️ মাঝারি ঝুঁকি — কিছু যাচাই অসম্পূর্ণ "
                "অথবা অতিরিক্ত প্রমাণ প্রয়োজন।"
            )

        else:

            st.error(
                "🚨 উচ্চ ঝুঁকি — এক বা একাধিক গুরুত্বপূর্ণ "
                "যাচাই ব্যর্থ হয়েছে।"
            )

    else:

        if risk_level == "LOW":

            st.success(
                "✅ LOW RISK — No blocking anomaly "
                "was detected."
            )

        elif risk_level == "MEDIUM":

            st.warning(
                "⚠️ MEDIUM RISK — Some checks are "
                "incomplete or require more evidence."
            )

        else:

            st.error(
                "🚨 HIGH RISK — One or more important "
                "risk checks failed."
            )


def create_case_id():

    date_part = datetime.now().strftime(
        "%Y%m%d"
    )

    random_part = (
        uuid4()
        .hex[:6]
        .upper()
    )

    return (
        f"BG-{date_part}-{random_part}"
    )


# =========================================================
# 9. DATAFRAME SCHEMAS
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


def empty_mutation():

    return pd.DataFrame(
        columns=MUTATION_COLUMNS
    )


# =========================================================
# 10. DEMO DATA
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


DEMO_DESCRIPTION = {
    "CLEAR_BASELINE": {
        "bn":
            (
                "বিক্রেতার মালিকানা, ভূমি খণ্ড, জমির পরিমাণ "
                "এবং নামজারি তথ্য পরস্পরের সঙ্গে সামঞ্জস্যপূর্ণ।"
            ),

        "en":
            (
                "Ownership, parcel, transfer area and mutation "
                "evidence are consistent."
            ),
    },

    "SELLER_NOT_OWNER": {
        "bn":
            (
                "ঘোষিত বিক্রেতা নিবন্ধিত ব্যক্তি হলেও "
                "এই ভূমি খণ্ডের বর্তমান মালিক নন।"
            ),

        "en":
            (
                "The seller exists in the registry but does "
                "not currently own this parcel."
            ),
    },

    "OVER_TRANSFER": {
        "bn":
            (
                "বিক্রেতার মালিকানা ৩.০ শতক, কিন্তু "
                "৫.৫ শতক জমি হস্তান্তরের চেষ্টা করা হচ্ছে।"
            ),

        "en":
            (
                "The seller owns 3.0 decimal but attempts "
                "to transfer 5.5 decimal."
            ),
    },

    "DOUBLE_SALE": {
        "bn":
            (
                "একই নির্দিষ্ট ভূমি অংশের পূর্ববর্তী "
                "বৈধ বিক্রয় রেকর্ড রয়েছে।"
            ),

        "en":
            (
                "The same identified land portion has a "
                "previous valid sale."
            ),
    },

    "DUPLICATE_DEED": {
        "bn":
            (
                "জমা দেওয়া দলিল নম্বরটি পূর্ববর্তী "
                "লেনদেনের রেকর্ডে ইতোমধ্যে রয়েছে।"
            ),

        "en":
            (
                "The submitted deed identifier already "
                "exists in transaction history."
            ),
    },

    "MUTATION_MISMATCH": {
        "bn":
            (
                "দলিলের বিক্রেতা এবং সক্রিয় নামজারি "
                "রেকর্ডের মালিকের মধ্যে অমিল রয়েছে।"
            ),

        "en":
            (
                "The deed seller differs from the active "
                "mutation-side owner."
            ),
    },
}


def build_demo_scenario(name):

    transaction = demo_transaction()
    ledger_df = demo_ledger()
    history_df = empty_history()
    mutation_df = demo_mutation()

    if name == "SELLER_NOT_OWNER":

        transaction[
            "seller_id"
        ] = "SELLER-SYN-002"

        mutation_df = demo_mutation(
            "SELLER-SYN-002"
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

        mutation_df = demo_mutation(
            "OTHER-OWNER-SYN-001"
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
# 11. CUSTOM TRANSACTION BUILDER
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

    # -----------------------------------------------------
    # Transaction
    # -----------------------------------------------------

    clean_portion_id = (
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
            clean_portion_id,

        "seller_id":
            seller_id.strip(),

        "transaction_status":
            "PENDING",

        "transferred_area_decimal":
            float(
                transferred_area
            ),
    }


    # -----------------------------------------------------
    # People Registry
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
            not in [
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

    # Previous buyer for history evidence
    people_rows.append(
        {
            "person_id":
                "PREVIOUS-BUYER-CUSTOM"
        }
    )

    people_df = pd.DataFrame(
        people_rows,
        columns=[
            "person_id"
        ],
    )


    # -----------------------------------------------------
    # Parcel Registry
    # -----------------------------------------------------

    parcel_rows = []

    if parcel_exists:

        parcel_rows.append(
            {
                "parcel_id":
                    parcel_id.strip()
            }
        )

    parcels_df = pd.DataFrame(
        parcel_rows,
        columns=[
            "parcel_id"
        ],
    )


    # -----------------------------------------------------
    # Ownership Ledger
    # -----------------------------------------------------

    ledger_rows = []

    if seller_is_owner:

        ledger_rows.append(
            {
                "ownership_id":
                    "OWN-CUSTOM-SELLER",

                "parcel_id":
                    parcel_id.strip(),

                "owner_id":
                    seller_id.strip(),

                "owned_area_decimal":
                    float(
                        seller_owned_area
                    ),

                "status":
                    "ACTIVE",
            }
        )

    else:

        ledger_rows.append(
            {
                "ownership_id":
                    "OWN-CUSTOM-OTHER",

                "parcel_id":
                    parcel_id.strip(),

                "owner_id":
                    "OTHER-OWNER-CUSTOM",

                "owned_area_decimal":
                    max(
                        float(
                            seller_owned_area
                        ),
                        float(
                            transferred_area
                        ),
                        1.0,
                    ),

                "status":
                    "ACTIVE",
            }
        )

    ledger_df = pd.DataFrame(
        ledger_rows,
        columns=LEDGER_COLUMNS,
    )


    # -----------------------------------------------------
    # History
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
                    "HISTORICAL-OTHER-PORTION",

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
                    clean_portion_id,

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
    # Mutation
    # -----------------------------------------------------

    mutation_rows = []

    if mutation_available:

        mutation_rows.append(
            {
                "parcel_id":
                    parcel_id.strip(),

                "portion_id":
                    clean_portion_id,

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
# 12. RULE RESULT DATAFRAME
# =========================================================

def build_rule_dataframe(report):

    rows = []

    for rule_name, result in (
        report[
            "rules"
        ].items()
    ):

        rows.append(
            {
                bi(
                    "যাচাই",
                    "Rule"
                ):
                    translated_rule_name(
                        rule_name
                    ),

                bi(
                    "অবস্থা",
                    "Status"
                ):
                    translate_value(
                        result[
                            "status"
                        ]
                    ),

                bi(
                    "ফলাফল",
                    "Code"
                ):
                    translated_rule_code(
                        result
                    ),

                bi(
                    "ব্যাখ্যা",
                    "Explanation"
                ):
                    translated_rule_message(
                        result
                    ),
            }
        )

    return pd.DataFrame(
        rows
    )


# =========================================================
# 13. DISPLAY TRANSACTION
# =========================================================

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


def transaction_display_df(
    transaction
):

    rows = []

    for key, value in (
        transaction.items()
    ):

        display_key = (
            TRANSACTION_LABEL_BN.get(
                key,
                key,
            )
            if LANG == "bn"
            else key
        )

        if LANG == "bn":

            if key in {
                "execution_date",
                "transferred_area_decimal",
            }:

                display_value = (
                    local_number(
                        value
                    )
                )

            elif value is None:

                display_value = (
                    "উপলব্ধ নয়"
                )

            else:

                display_value = (
                    translate_value(
                        value
                    )
                )

        else:

            display_value = (
                "Not available"
                if value is None
                else value
            )

        rows.append(
            {
                bi(
                    "তথ্য",
                    "Field"
                ):
                    display_key,

                bi(
                    "মান",
                    "Value"
                ):
                    display_value,
            }
        )

    return pd.DataFrame(
        rows
    )


# =========================================================
# 14. EVIDENCE DISPLAY HELPERS
# =========================================================

def display_ledger_df(df):

    result = df.copy()

    if LANG == "bn":

        result = result.rename(
            columns={
                "ownership_id":
                    "মালিকানা আইডি",

                "parcel_id":
                    "ভূমি খণ্ড আইডি",

                "owner_id":
                    "মালিক আইডি",

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
                .map(
                    local_number
                )
            )

        if "অবস্থা" in result.columns:

            result[
                "অবস্থা"
            ] = (
                result[
                    "অবস্থা"
                ]
                .map(
                    translate_value
                )
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
                    "ভূমি খণ্ড আইডি",

                "portion_id":
                    "ভূমি অংশ আইডি",

                "transaction_status":
                    "লেনদেনের অবস্থা",

                "buyer_id":
                    "ক্রেতা আইডি",
            }
        )

        status_col = (
            "লেনদেনের অবস্থা"
        )

        if status_col in result.columns:

            result[
                status_col
            ] = (
                result[
                    status_col
                ]
                .map(
                    translate_value
                )
            )

    return result


def display_mutation_df(df):

    result = df.copy()

    if LANG == "bn":

        result = result.rename(
            columns={
                "parcel_id":
                    "ভূমি খণ্ড আইডি",

                "portion_id":
                    "ভূমি অংশ আইডি",

                "mutation_owner_id":
                    "নামজারি মালিক আইডি",

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
                .map(
                    translate_value
                )
            )

    return result


# =========================================================
# 15. DOWNLOADABLE REPORT
# =========================================================

def build_download_report(
    case_id,
    report,
    transaction,
):

    lines = []

    if LANG == "bn":

        lines.extend(
            [
                "ভূমিগার্ড বিডি — প্রাক-নিবন্ধন ঝুঁকি যাচাই",
                "=" * 60,
                f"স্ক্রিনিং আইডি: {case_id}",
                "",
                "লেনদেন",
                "-" * 60,
                f"দলিল আইডি: {transaction['deed_id']}",
                f"ভূমি খণ্ড: {transaction['parcel_id']}",
                f"ভূমি অংশ: {transaction['portion_id']}",
                f"বিক্রেতা: {transaction['seller_id']}",
                f"ক্রেতা: {transaction['buyer_id']}",
                (
                    "হস্তান্তরিত জমি: "
                    f"{local_number(transaction['transferred_area_decimal'])} শতক"
                ),
                "",
                "ফলাফল",
                "-" * 60,
                (
                    "সামগ্রিক ঝুঁকি: "
                    f"{display_risk_level(report['risk_level'])}"
                ),
                (
                    "সফল: "
                    f"{local_number(report['pass_count'])}"
                ),
                (
                    "সতর্কতা: "
                    f"{local_number(report['warning_count'])}"
                ),
                (
                    "ব্যর্থ: "
                    f"{local_number(report['fail_count'])}"
                ),
                "",
                "নিয়মভিত্তিক যাচাই",
                "-" * 60,
            ]
        )

    else:

        lines.extend(
            [
                "BHUMIGUARD BD — PRE-REGISTRATION SCREENING",
                "=" * 60,
                f"Screening ID: {case_id}",
                "",
                "TRANSACTION",
                "-" * 60,
                f"Deed ID: {transaction['deed_id']}",
                f"Parcel: {transaction['parcel_id']}",
                f"Portion: {transaction['portion_id']}",
                f"Seller: {transaction['seller_id']}",
                f"Buyer: {transaction['buyer_id']}",
                (
                    "Transfer area: "
                    f"{transaction['transferred_area_decimal']} decimal"
                ),
                "",
                "RESULT",
                "-" * 60,
                (
                    "Overall risk: "
                    f"{report['risk_level']}"
                ),
                (
                    "PASS: "
                    f"{report['pass_count']}"
                ),
                (
                    "WARNING: "
                    f"{report['warning_count']}"
                ),
                (
                    "FAIL: "
                    f"{report['fail_count']}"
                ),
                "",
                "RULE CHECKS",
                "-" * 60,
            ]
        )

    for rule_name, result in (
        report[
            "rules"
        ].items()
    ):

        if LANG == "bn":

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

        else:

            lines.append(
                (
                    f"{result['status']} | "
                    f"{rule_name} | "
                    f"{result['code']}"
                )
            )

            lines.append(
                f"  {result['message']}"
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
                    "Screening result only. It does not establish "
                    "legal title or prove fraud."
                ),
            ),
        ]
    )

    return "\n".join(
        lines
    )


# =========================================================
# 16. COMMON RESULT RENDERER
# =========================================================

def render_screening_result(
    bundle
):

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


    st.divider()

    st.header(
        bi(
            "৩. যাচাইয়ের ফলাফল",
            "3. Screening Result",
        )
    )


    # -----------------------------------------------------
    # Case ID
    # -----------------------------------------------------

    st.caption(
        (
            f"{bi('স্ক্রিনিং আইডি', 'Screening ID')}: "
            f"{case_id}"
        )
    )


    # -----------------------------------------------------
    # Risk Banner
    # -----------------------------------------------------

    show_risk_banner(
        report[
            "risk_level"
        ]
    )


    # -----------------------------------------------------
    # Metrics
    # -----------------------------------------------------

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        bi(
            "সামগ্রিক ঝুঁকি",
            "Overall Risk"
        ),
        display_risk_level(
            report[
                "risk_level"
            ]
        ),
    )

    col2.metric(
        bi(
            "সফল",
            "Passed"
        ),
        local_number(
            report[
                "pass_count"
            ]
        ),
    )

    col3.metric(
        bi(
            "সতর্কতা",
            "Warnings"
        ),
        local_number(
            report[
                "warning_count"
            ]
        ),
    )

    col4.metric(
        bi(
            "ব্যর্থ",
            "Failed"
        ),
        local_number(
            report[
                "fail_count"
            ]
        ),
    )


    # -----------------------------------------------------
    # Rule Table
    # -----------------------------------------------------

    st.subheader(
        bi(
            "ব্যাখ্যাসহ নিয়মভিত্তিক যাচাই",
            "Explainable Rule Checks",
        )
    )

    rules_df = (
        build_rule_dataframe(
            report
        )
    )

    st.dataframe(
        rules_df,
        use_container_width=True,
        hide_index=True,
    )


    # -----------------------------------------------------
    # Decision Explanation
    # -----------------------------------------------------

    st.subheader(
        bi(
            "ঝুঁকি বিশ্লেষণ",
            "Decision Explanation",
        )
    )

    for _, result in (
        report[
            "rules"
        ].items()
    ):

        display_text = (
            f"{translated_rule_code(result)} — "
            f"{translated_rule_message(result)}"
        )

        if result[
            "status"
        ] == "PASS":

            st.success(
                display_text
            )

        elif result[
            "status"
        ] == "WARNING":

            st.warning(
                display_text
            )

        else:

            st.error(
                display_text
            )


    # -----------------------------------------------------
    # Evidence
    # -----------------------------------------------------

    st.subheader(
        bi(
            "প্রমাণের সারসংক্ষেপ",
            "Evidence Summary",
        )
    )

    evidence_col1, evidence_col2, evidence_col3 = (
        st.columns(3)
    )

    evidence_col1.metric(
        bi(
            "মালিকানা রেকর্ড",
            "Ownership Records",
        ),
        local_number(
            len(
                context[
                    "ledger_df"
                ]
            )
        ),
    )

    evidence_col2.metric(
        bi(
            "পূর্ববর্তী লেনদেন",
            "Previous Transactions",
        ),
        local_number(
            len(
                context[
                    "history_df"
                ]
            )
        ),
    )

    evidence_col3.metric(
        bi(
            "নামজারি রেকর্ড",
            "Mutation Records",
        ),
        local_number(
            len(
                context[
                    "mutation_df"
                ]
            )
        ),
    )


    # -----------------------------------------------------
    # Ownership
    # -----------------------------------------------------

    with st.expander(
        bi(
            "মালিকানা তথ্য দেখুন",
            "View Ownership Evidence",
        )
    ):

        st.dataframe(
            display_ledger_df(
                context[
                    "ledger_df"
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )


    # -----------------------------------------------------
    # History
    # -----------------------------------------------------

    with st.expander(
        bi(
            "পূর্ববর্তী লেনদেনের তথ্য দেখুন",
            "View Transaction History",
        )
    ):

        if context[
            "history_df"
        ].empty:

            st.info(
                bi(
                    "কোনো পূর্ববর্তী বৈধ লেনদেন পাওয়া যায়নি।",
                    "No previous transaction history found.",
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


    # -----------------------------------------------------
    # Mutation
    # -----------------------------------------------------

    with st.expander(
        bi(
            "নামজারি তথ্য দেখুন",
            "View Mutation Evidence",
        )
    ):

        if context[
            "mutation_df"
        ].empty:

            st.info(
                bi(
                    "কোনো নামজারি রেকর্ড সরবরাহ করা হয়নি।",
                    "No mutation record was provided.",
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
    # Report Download
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
            "⬇️ স্ক্রিনিং রিপোর্ট ডাউনলোড করুন",
            "⬇️ Download Screening Report",
        ),
        data=report_text,
        file_name=(
            f"{case_id}_"
            "bhumiguard_report.txt"
        ),
        mime="text/plain",
        use_container_width=True,
    )


    # -----------------------------------------------------
    # Disclaimer
    # -----------------------------------------------------

    st.warning(
        bi(
            (
                "এই ফলাফল শুধুমাত্র প্রাথমিক ঝুঁকি যাচাইয়ের "
                "জন্য। এটি আইনগত মালিকানা প্রতিষ্ঠা করে না "
                "এবং প্রতারণা প্রমাণ করে না।"
            ),
            (
                "This is a screening result only. "
                "It does not establish legal title "
                "or prove fraud."
            ),
        )
    )

    st.info(
        bi(
            (
                "এই prototype screening-এর সময় কোনো "
                "ownership ledger বা সরকারি ভূমি রেকর্ড "
                "পরিবর্তন করে না।"
            ),
            (
                "This prototype does not modify any "
                "ownership ledger or official land record "
                "during screening."
            ),
        )
    )


# =========================================================
# 17. HEADER
# =========================================================

st.title(
    bi(
        "🏡 ভূমিগার্ড বিডি",
        "🏡 BhumiGuard BD",
    )
)

st.subheader(
    bi(
        "এআই-সহায়িত প্রাক-নিবন্ধন ভূমি লেনদেন ঝুঁকি যাচাই",
        (
            "AI-Assisted Pre-Registration "
            "Land Transaction Risk Screening"
        ),
    )
)

st.caption(
    bi(
        "শুধু দলিল নয় — লেনদেনের ইতিহাসও যাচাই",
        "Verify the transaction, not just the document",
    )
)


# =========================================================
# 18. SIDEBAR MODE
# =========================================================

st.sidebar.divider()

st.sidebar.header(
    bi(
        "যাচাই পদ্ধতি",
        "Screening Mode",
    )
)

mode_label = st.sidebar.radio(
    bi(
        "পদ্ধতি নির্বাচন করুন",
        "Choose a mode",
    ),
    [
        bi(
            "প্রস্তুত ডেমো",
            "Validated Demo",
        ),
        bi(
            "কাস্টম লেনদেন যাচাই",
            "Custom Transaction",
        ),
    ],
)


DEMO_MODE = (
    mode_label
    ==
    bi(
        "প্রস্তুত ডেমো",
        "Validated Demo",
    )
)


# =========================================================
# 19. DEMO MODE
# =========================================================

if DEMO_MODE:

    st.sidebar.divider()

    st.sidebar.header(
        bi(
            "ডেমো নিয়ন্ত্রণ",
            "Demo Controls",
        )
    )

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

            "দলিল ও নামজারি তথ্যের অমিল":
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

    selected_demo_label = (
        st.sidebar.selectbox(
            bi(
                "ডেমো পরিস্থিতি নির্বাচন করুন",
                "Select Demo Scenario",
            ),
            list(
                demo_labels.keys()
            ),
        )
    )

    demo_name = (
        demo_labels[
            selected_demo_label
        ]
    )


    # Clear stale result if scenario changes
    if (
        st.session_state.get(
            "current_demo_name"
        )
        !=
        demo_name
    ):

        st.session_state[
            "current_demo_name"
        ] = demo_name

        st.session_state.pop(
            "demo_screening_result",
            None,
        )


    context = (
        build_demo_scenario(
            demo_name
        )
    )

    transaction = (
        context[
            "transaction"
        ]
    )


    # -----------------------------------------------------
    # Overview
    # -----------------------------------------------------

    st.divider()

    st.header(
        bi(
            "১. লেনদেনের সারসংক্ষেপ",
            "1. Transaction Overview",
        )
    )

    st.write(
        context[
            "description"
        ]
    )

    st.info(
        bi(
            (
                "এই ডেমোর সকল ব্যক্তি, দলিল এবং "
                "ভূমি তথ্য কৃত্রিম।"
            ),
            (
                "All identities, deeds and land records "
                "in this demo are synthetic."
            ),
        )
    )


    col1, col2, col3, col4 = (
        st.columns(4)
    )

    col1.metric(
        bi(
            "দলিল আইডি",
            "Deed ID"
        ),
        transaction[
            "deed_id"
        ],
    )

    col2.metric(
        bi(
            "ভূমি খণ্ড",
            "Parcel"
        ),
        transaction[
            "parcel_id"
        ],
    )

    col3.metric(
        bi(
            "হস্তান্তরিত জমি",
            "Transfer Area"
        ),
        (
            f"{local_number(transaction['transferred_area_decimal'])} "
            f"{bi('শতক', 'decimal')}"
        ),
    )

    col4.metric(
        bi(
            "ভূমি অংশ আইডি",
            "Portion ID"
        ),
        transaction[
            "portion_id"
        ],
    )


    with st.expander(
        bi(
            "যাচাইকৃত লেনদেনের তথ্য দেখুন",
            "View Transaction Fields",
        )
    ):

        st.dataframe(
            transaction_display_df(
                transaction
            ),
            use_container_width=True,
            hide_index=True,
        )


    # -----------------------------------------------------
    # Screening
    # -----------------------------------------------------

    st.header(
        bi(
            "২. প্রাক-নিবন্ধন ঝুঁকি যাচাই",
            "2. Pre-Registration Screening",
        )
    )

    if st.button(
        bi(
            "🔍 লেনদেন যাচাই করুন",
            "🔍 Verify Transaction",
        ),
        type="primary",
        use_container_width=True,
        key="demo_verify",
    ):

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
                transaction,
                context[
                    "people_df"
                ],
                context[
                    "parcels_df"
                ],
            )
        )

        st.session_state[
            "demo_screening_result"
        ] = {
            "case_id":
                create_case_id(),

            "report":
                report,

            "context":
                context,
        }


    if (
        "demo_screening_result"
        in
        st.session_state
    ):

        render_screening_result(
            st.session_state[
                "demo_screening_result"
            ]
        )


# =========================================================
# 20. CUSTOM TRANSACTION MODE
# =========================================================

else:

    st.divider()

    st.header(
        bi(
            "১. কাস্টম লেনদেন ও প্রমাণের তথ্য",
            "1. Custom Transaction & Evidence",
        )
    )

    st.info(
        bi(
            (
                "এখানে নিজের test transaction তৈরি করে একই "
                "BhumiGuard risk engine live পরীক্ষা করতে পারবেন।"
            ),
            (
                "Create your own test transaction here and "
                "run it through the same BhumiGuard risk engine."
            ),
        )
    )

    st.warning(
        bi(
            (
                "Public demo-তে প্রকৃত NID, ফোন নম্বর, গোপন ব্যক্তিগত "
                "তথ্য বা confidential ভূমি রেকর্ড ব্যবহার করবেন না। "
                "Synthetic/test ID ব্যবহার করুন।"
            ),
            (
                "Do not enter real NIDs, phone numbers, confidential "
                "personal information, or sensitive land records in "
                "the public demo. Use synthetic/test identifiers."
            ),
        )
    )


    with st.form(
        "custom_transaction_form"
    ):

        # -------------------------------------------------
        # Transaction Details
        # -------------------------------------------------

        st.subheader(
            bi(
                "ক. প্রস্তাবিত লেনদেন",
                "A. Proposed Transaction",
            )
        )

        c1, c2 = st.columns(2)

        deed_id = c1.text_input(
            bi(
                "দলিল আইডি",
                "Deed ID"
            ),
            value="DEED-CUSTOM-001",
        )

        execution_date = c2.date_input(
            bi(
                "দলিল সম্পাদনের তারিখ",
                "Execution Date",
            )
        )


        c1, c2 = st.columns(2)

        seller_id = c1.text_input(
            bi(
                "বিক্রেতা আইডি",
                "Seller ID"
            ),
            value="SELLER-CUSTOM-001",
        )

        buyer_id = c2.text_input(
            bi(
                "ক্রেতা আইডি",
                "Buyer ID"
            ),
            value="BUYER-CUSTOM-001",
        )


        c1, c2 = st.columns(2)

        parcel_id = c1.text_input(
            bi(
                "ভূমি খণ্ড আইডি",
                "Parcel ID"
            ),
            value="PARCEL-CUSTOM-001",
        )

        portion_id = c2.text_input(
            bi(
                "ভূমি অংশ আইডি",
                "Portion ID",
            ),
            value="PORTION-CUSTOM-001",
            help=bi(
                (
                    "Boundary/schedule/share evidence থেকে নির্ধারিত "
                    "portion identifier। খালি রাখলে double-sale "
                    "verification অসম্পূর্ণ হবে।"
                ),
                (
                    "An identifier derived from reliable portion "
                    "evidence. Leave blank to test incomplete "
                    "double-sale verification."
                ),
            ),
        )


        transferred_area = (
            st.number_input(
                bi(
                    "হস্তান্তরিত জমি (শতক)",
                    "Transfer Area (decimal)",
                ),
                min_value=0.01,
                value=5.50,
                step=0.50,
            )
        )


        # -------------------------------------------------
        # Registry Evidence
        # -------------------------------------------------

        st.subheader(
            bi(
                "খ. Registry Evidence",
                "B. Registry Evidence",
            )
        )

        c1, c2, c3 = st.columns(3)

        seller_exists = c1.checkbox(
            bi(
                "বিক্রেতা registry-তে আছেন",
                "Seller exists in registry",
            ),
            value=True,
        )

        buyer_exists = c2.checkbox(
            bi(
                "ক্রেতা registry-তে আছেন",
                "Buyer exists in registry",
            ),
            value=True,
        )

        parcel_exists = c3.checkbox(
            bi(
                "ভূমি খণ্ড registry-তে আছে",
                "Parcel exists in registry",
            ),
            value=True,
        )


        # -------------------------------------------------
        # Ownership Evidence
        # -------------------------------------------------

        st.subheader(
            bi(
                "গ. বর্তমান মালিকানা",
                "C. Current Ownership",
            )
        )

        c1, c2 = st.columns(2)

        seller_is_owner = c1.checkbox(
            bi(
                "বিক্রেতা বর্তমান মালিক",
                "Seller is current owner",
            ),
            value=True,
        )

        seller_owned_area = c2.number_input(
            bi(
                "বিক্রেতার মালিকানাধীন জমি (শতক)",
                "Seller-owned Area (decimal)",
            ),
            min_value=0.0,
            value=10.50,
            step=0.50,
        )


        # -------------------------------------------------
        # History Evidence
        # -------------------------------------------------

        st.subheader(
            bi(
                "ঘ. পূর্ববর্তী লেনদেনের ইতিহাস",
                "D. Previous Transaction History",
            )
        )

        c1, c2 = st.columns(2)

        duplicate_deed = c1.checkbox(
            bi(
                "একই দলিল আইডি আগে ব্যবহৃত হয়েছে",
                "Same deed ID already exists",
            ),
            value=False,
        )

        previous_same_portion_sale = c2.checkbox(
            bi(
                "একই ভূমি অংশ আগে বৈধভাবে বিক্রি হয়েছে",
                "Same portion has a previous valid sale",
            ),
            value=False,
        )


        # -------------------------------------------------
        # Mutation Evidence
        # -------------------------------------------------

        st.subheader(
            bi(
                "ঙ. নামজারি তথ্য",
                "E. Mutation Evidence",
            )
        )

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
                    "নামজারি রেকর্ডের মালিক আইডি",
                    "Mutation-side Owner ID",
                ),
                value="SELLER-CUSTOM-001",
                disabled=(
                    not mutation_available
                ),
            )
        )


        # -------------------------------------------------
        # Submit
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
    # 21. CUSTOM EXECUTION
    # =====================================================

    if custom_submit:

        validation_errors = []

        if not deed_id.strip():

            validation_errors.append(
                bi(
                    "দলিল আইডি আবশ্যক।",
                    "Deed ID is required.",
                )
            )

        if not seller_id.strip():

            validation_errors.append(
                bi(
                    "বিক্রেতা আইডি আবশ্যক।",
                    "Seller ID is required.",
                )
            )

        if not buyer_id.strip():

            validation_errors.append(
                bi(
                    "ক্রেতা আইডি আবশ্যক।",
                    "Buyer ID is required.",
                )
            )

        if not parcel_id.strip():

            validation_errors.append(
                bi(
                    "ভূমি খণ্ড আইডি আবশ্যক।",
                    "Parcel ID is required.",
                )
            )


        if validation_errors:

            for message in validation_errors:

                st.error(
                    message
                )

        else:

            custom_context = (
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

                custom_report = (
                    risk.verify_transaction(
                        custom_context[
                            "ledger_df"
                        ],
                        custom_context[
                            "history_df"
                        ],
                        custom_context[
                            "mutation_df"
                        ],
                        custom_context[
                            "transaction"
                        ],
                        custom_context[
                            "people_df"
                        ],
                        custom_context[
                            "parcels_df"
                        ],
                    )
                )


                st.session_state[
                    "custom_screening_result"
                ] = {
                    "case_id":
                        create_case_id(),

                    "report":
                        custom_report,

                    "context":
                        custom_context,
                }


            except Exception as error:

                st.error(
                    bi(
                        (
                            "ঝুঁকি যাচাই সম্পন্ন করা যায়নি। "
                            "ইনপুট ও evidence configuration যাচাই করুন।"
                        ),
                        (
                            "Screening could not be completed. "
                            "Please review the input and evidence configuration."
                        ),
                    )
                )

                with st.expander(
                    bi(
                        "Technical error",
                        "Technical error",
                    )
                ):

                    st.code(
                        str(
                            error
                        )
                    )


    # =====================================================
    # 22. CUSTOM RESULT
    # =====================================================

    if (
        "custom_screening_result"
        in
        st.session_state
    ):

        st.subheader(
            bi(
                "লেনদেনের সারসংক্ষেপ",
                "Transaction Summary",
            )
        )

        st.dataframe(
            transaction_display_df(
                st.session_state[
                    "custom_screening_result"
                ][
                    "context"
                ][
                    "transaction"
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )


        render_screening_result(
            st.session_state[
                "custom_screening_result"
            ]
        )


# =========================================================
# 23. FOOTER
# =========================================================

st.divider()

st.caption(
    bi(
        (
            "BhumiGuard BD • LandTech 2026 Prototype • "
            "সিদ্ধান্ত-সহায়ক ব্যবস্থা; আইনগত মালিকানা "
            "নির্ধারণের ব্যবস্থা নয়।"
        ),
        (
            "BhumiGuard BD • LandTech 2026 Prototype • "
            "Decision-support system, not legal title determination."
        ),
    )
)