from pathlib import Path
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
# 4. LANGUAGE SELECTOR
# =========================================================

language = st.sidebar.radio(
    "ভাষা / Language",
    [
        "বাংলা",
        "English",
    ],
    index=0,
    horizontal=True,
)

LANG = (
    "bn"
    if language == "বাংলা"
    else "en"
)


# =========================================================
# 5. BANGLA DIGIT CONVERSION
# =========================================================

BANGLA_DIGITS = str.maketrans(
    "0123456789",
    "০১২৩৪৫৬৭৮৯",
)


def to_bangla_digits(value):

    if LANG == "en":
        return str(value)

    return str(value).translate(
        BANGLA_DIGITS
    )


# =========================================================
# 6. TRANSLATION DICTIONARY
# =========================================================

TEXT = {

    "bn": {

        "title":
            "🏡 ভূমিগার্ড বিডি",

        "subtitle":
            "এআই-সহায়িত প্রাক-নিবন্ধন ভূমি লেনদেন ঝুঁকি যাচাই",

        "tagline":
            "শুধু দলিল নয় — লেনদেনের ইতিহাসও যাচাই",

        "demo_controls":
            "ডেমো নিয়ন্ত্রণ",

        "scenario":
            "ডেমো পরিস্থিতি নির্বাচন করুন",

        "synthetic_notice":
            (
                "ডেমোতে ব্যবহৃত সকল ব্যক্তি, দলিল "
                "এবং ভূমি তথ্য কৃত্রিম।"
            ),

        "transaction_overview":
            "১. লেনদেনের সারসংক্ষেপ",

        "deed_id":
            "দলিল আইডি",

        "parcel":
            "ভূমি খণ্ড",

        "transfer_area":
            "হস্তান্তরিত জমি",

        "portion_id":
            "ভূমি অংশ আইডি",

        "verified_fields":
            "যাচাইকৃত লেনদেনের তথ্য দেখুন",

        "field":
            "তথ্য",

        "value":
            "মান",

        "screening":
            "২. প্রাক-নিবন্ধন ঝুঁকি যাচাই",

        "verify":
            "🔍 লেনদেন যাচাই করুন",

        "result":
            "৩. যাচাইয়ের ফলাফল",

        "overall_risk":
            "সামগ্রিক ঝুঁকি",

        "passed":
            "সফল",

        "warnings":
            "সতর্কতা",

        "failed":
            "ব্যর্থ",

        "rule_checks":
            "ব্যাখ্যাসহ নিয়মভিত্তিক যাচাই",

        "rule":
            "যাচাই",

        "status":
            "অবস্থা",

        "code":
            "ফলাফল",

        "explanation":
            "ব্যাখ্যা",

        "decision":
            "ঝুঁকি বিশ্লেষণ",

        "ownership":
            "মালিকানা তথ্য",

        "history":
            "পূর্ববর্তী লেনদেনের তথ্য",

        "mutation":
            "নামজারি তথ্য",

        "no_history":
            "কোনো পূর্ববর্তী বৈধ লেনদেন পাওয়া যায়নি।",

        "demo_mode":
            (
                "ডেমো মোড: এটি শুধুমাত্র ঝুঁকি যাচাই করে। "
                "কোনো মালিকানা খতিয়ান বা সরকারি ভূমি "
                "রেকর্ড পরিবর্তন করা হয় না।"
            ),

        "disclaimer":
            (
                "এই ফলাফল শুধুমাত্র প্রাথমিক ঝুঁকি যাচাইয়ের জন্য। "
                "এটি আইনগত মালিকানা প্রতিষ্ঠা করে না "
                "এবং প্রতারণা প্রমাণ করে না।"
            ),

        "footer":
            (
                "BhumiGuard BD • LandTech 2026 Prototype • "
                "এটি সিদ্ধান্ত-সহায়ক ব্যবস্থা; "
                "আইনগত মালিকানা নির্ধারণের ব্যবস্থা নয়।"
            ),
    },

    "en": {

        "title":
            "🏡 BhumiGuard BD",

        "subtitle":
            (
                "AI-Assisted Pre-Registration "
                "Land Transaction Risk Screening"
            ),

        "tagline":
            "Verify the transaction, not just the document",

        "demo_controls":
            "Demo Controls",

        "scenario":
            "Select Demo Scenario",

        "synthetic_notice":
            (
                "All demo identities, deeds and "
                "land records are synthetic."
            ),

        "transaction_overview":
            "1. Transaction Overview",

        "deed_id":
            "Deed ID",

        "parcel":
            "Parcel",

        "transfer_area":
            "Transfer Area",

        "portion_id":
            "Portion ID",

        "verified_fields":
            "View Verified Transaction Fields",

        "field":
            "Field",

        "value":
            "Value",

        "screening":
            "2. Pre-Registration Screening",

        "verify":
            "🔍 Verify Transaction",

        "result":
            "3. Screening Result",

        "overall_risk":
            "Overall Risk",

        "passed":
            "Passed",

        "warnings":
            "Warnings",

        "failed":
            "Failed",

        "rule_checks":
            "Explainable Rule Checks",

        "rule":
            "Rule",

        "status":
            "Status",

        "code":
            "Code",

        "explanation":
            "Explanation",

        "decision":
            "Decision Explanation",

        "ownership":
            "Ownership Context",

        "history":
            "Transaction History Evidence",

        "mutation":
            "Mutation Evidence",

        "no_history":
            "No previous transaction history found.",

        "demo_mode":
            (
                "Demo mode: screening only. "
                "No ownership ledger or official "
                "land record is modified."
            ),

        "disclaimer":
            (
                "Screening result only. "
                "It does not establish legal title "
                "or prove fraud."
            ),

        "footer":
            (
                "BhumiGuard BD • LandTech 2026 Prototype • "
                "Decision-support system, "
                "not legal title determination."
            ),
    },
}


def t(key):
    return TEXT[LANG][key]


# =========================================================
# 7. RULE NAME TRANSLATION
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


# =========================================================
# 8. RULE CODE TRANSLATION
# =========================================================

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


# =========================================================
# 9. RULE EXPLANATION TRANSLATION
# =========================================================

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
        (
            "ভূমি খণ্ডটি ভূমি রেজিস্ট্রিতে "
            "পাওয়া গেছে।"
        ),

    "PARCEL_NOT_FOUND":
        (
            "ভূমি খণ্ডটি ভূমি রেজিস্ট্রিতে "
            "পাওয়া যায়নি।"
        ),

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


# =========================================================
# 10. GENERAL VALUE TRANSLATION
# =========================================================

VALUE_BN = {

    "PASS":
        "সফল",

    "WARNING":
        "সতর্কতা",

    "FAIL":
        "ব্যর্থ",

    "ACTIVE":
        "সক্রিয়",

    "INACTIVE":
        "নিষ্ক্রিয়",

    "VALID":
        "বৈধ",

    "INVALID":
        "অবৈধ",

    "PENDING":
        "অপেক্ষমাণ",
}


# =========================================================
# 11. TRANSACTION FIELD TRANSLATION
# =========================================================

TRANSACTION_FIELD_BN = {

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
# 12. TRANSLATION HELPERS
# =========================================================

def translate_value(value):

    if LANG == "en":
        return value

    return VALUE_BN.get(
        value,
        value,
    )


def translated_rule_message(result):

    if LANG == "en":
        return result["message"]

    return RULE_BN.get(
        result["code"],
        result["message"],
    )


def translated_rule_code(result):

    if LANG == "en":
        return result["code"]

    return RULE_CODE_BN.get(
        result["code"],
        result["code"],
    )


def translated_rule_name(rule_name):

    if LANG == "en":
        return rule_name

    return RULE_NAME_BN.get(
        rule_name,
        rule_name,
    )


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


# =========================================================
# 13. RISK BANNER
# =========================================================

def show_risk_banner(risk_level):

    if LANG == "bn":

        if risk_level == "LOW":

            st.success(
                "কম ঝুঁকি — এই যাচাইয়ে কোনো "
                "গুরুতর অসঙ্গতি পাওয়া যায়নি।"
            )

        elif risk_level == "MEDIUM":

            st.warning(
                "মাঝারি ঝুঁকি — কিছু যাচাই অসম্পূর্ণ "
                "অথবা অতিরিক্ত প্রমাণ প্রয়োজন।"
            )

        else:

            st.error(
                "উচ্চ ঝুঁকি — এক বা একাধিক গুরুত্বপূর্ণ "
                "যাচাই ব্যর্থ হয়েছে।"
            )

    else:

        if risk_level == "LOW":

            st.success(
                "LOW RISK — No blocking anomaly "
                "was detected in this screening."
            )

        elif risk_level == "MEDIUM":

            st.warning(
                "MEDIUM RISK — Some checks are incomplete "
                "or require further evidence."
            )

        else:

            st.error(
                "HIGH RISK — One or more important "
                "risk checks failed."
            )


# =========================================================
# 14. DEMO PEOPLE
# =========================================================

def get_people_df():

    return pd.DataFrame(
        [
            {
                "person_id":
                    "SELLER-SYN-001"
            },

            {
                "person_id":
                    "SELLER-SYN-002"
            },

            {
                "person_id":
                    "BUYER-SYN-001"
            },

            {
                "person_id":
                    "PREVIOUS-BUYER-SYN-001"
            },

            {
                "person_id":
                    "OTHER-OWNER-SYN-001"
            },
        ]
    )


# =========================================================
# 15. DEMO PARCELS
# =========================================================

def get_parcels_df():

    return pd.DataFrame(
        [
            {
                "parcel_id":
                    "PARCEL-SYN-001"
            }
        ]
    )


# =========================================================
# 16. DEMO OWNERSHIP LEDGER
# =========================================================

def get_base_ledger():

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
                    10.50,

                "status":
                    "ACTIVE",
            }
        ]
    )


# =========================================================
# 17. EMPTY HISTORY
# =========================================================

def empty_history():

    return pd.DataFrame(
        columns=[
            "deed_id",
            "parcel_id",
            "portion_id",
            "transaction_status",
            "buyer_id",
        ]
    )


# =========================================================
# 18. MUTATION RECORD
# =========================================================

def matching_mutation(
    owner_id="SELLER-SYN-001",
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


# =========================================================
# 19. BASE TRANSACTION
# =========================================================

def base_transaction():

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
            5.50,
    }


# =========================================================
# 20. SCENARIO DESCRIPTIONS
# =========================================================

SCENARIO_DESCRIPTION = {

    "CLEAR_BASELINE": {

        "bn":
            (
                "বিক্রেতার মালিকানা, ভূমি খণ্ড, নির্দিষ্ট অংশ "
                "এবং নামজারি তথ্য পরস্পরের সঙ্গে সামঞ্জস্যপূর্ণ।"
            ),

        "en":
            (
                "Valid synthetic transaction with matching "
                "ownership, parcel, portion and mutation evidence."
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
                "The declared seller exists in the registry "
                "but does not currently own this parcel."
            ),
    },

    "OVER_TRANSFER": {

        "bn":
            (
                "বিক্রেতার মালিকানা ৩.০ শতক, কিন্তু তিনি "
                "৫.৫ শতক জমি হস্তান্তরের চেষ্টা করছেন।"
            ),

        "en":
            (
                "Seller owns only 3.0 decimal but attempts "
                "to transfer 5.5 decimal."
            ),
    },

    "DOUBLE_SALE": {

        "bn":
            (
                "একই নির্দিষ্ট ভূমি অংশের একটি পূর্ববর্তী "
                "বৈধ বিক্রয় রেকর্ড পাওয়া গেছে।"
            ),

        "en":
            (
                "The same identified land portion already "
                "has a previous valid sale."
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
                "দলিলে উল্লিখিত বিক্রেতা এবং সক্রিয় "
                "নামজারি রেকর্ডের মালিকের মধ্যে অমিল রয়েছে।"
            ),

        "en":
            (
                "The deed seller does not match the "
                "active mutation-side owner."
            ),
    },
}


# =========================================================
# 21. BUILD DEMO SCENARIO
# =========================================================

def build_demo_scenario(
    scenario_name,
):

    transaction = (
        base_transaction()
    )

    ledger_df = (
        get_base_ledger()
    )

    history_df = (
        empty_history()
    )

    mutation_df = (
        matching_mutation()
    )


    if scenario_name == "SELLER_NOT_OWNER":

        transaction[
            "seller_id"
        ] = "SELLER-SYN-002"

        mutation_df = (
            matching_mutation(
                owner_id=
                    "SELLER-SYN-002"
            )
        )


    elif scenario_name == "OVER_TRANSFER":

        ledger_df.loc[
            0,
            "owned_area_decimal"
        ] = 3.0


    elif scenario_name == "DOUBLE_SALE":

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
            ]
        )


    elif scenario_name == "DUPLICATE_DEED":

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
            ]
        )


    elif scenario_name == "MUTATION_MISMATCH":

        mutation_df = (
            matching_mutation(
                owner_id=
                    "OTHER-OWNER-SYN-001"
            )
        )


    return {

        "description":
            SCENARIO_DESCRIPTION[
                scenario_name
            ][LANG],

        "transaction":
            transaction,

        "ledger_df":
            ledger_df,

        "history_df":
            history_df,

        "mutation_df":
            mutation_df,

        "people_df":
            get_people_df(),

        "parcels_df":
            get_parcels_df(),
    }


# =========================================================
# 22. RULE RESULT DATAFRAME
# =========================================================

def rule_dataframe(
    report,
):

    rows = []

    for rule_name, result in (
        report[
            "rules"
        ].items()
    ):

        rows.append(
            {

                t("rule"):
                    translated_rule_name(
                        rule_name
                    ),

                t("status"):
                    translate_value(
                        result[
                            "status"
                        ]
                    ),

                t("code"):
                    translated_rule_code(
                        result
                    ),

                t("explanation"):
                    translated_rule_message(
                        result
                    ),
            }
        )

    return pd.DataFrame(
        rows
    )


# =========================================================
# 23. SIDEBAR
# =========================================================

st.sidebar.header(
    t(
        "demo_controls"
    )
)


if LANG == "bn":

    scenario_labels = {

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

    scenario_labels = {

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
        t(
            "scenario"
        ),
        list(
            scenario_labels.keys()
        ),
    )
)


scenario_name = (
    scenario_labels[
        selected_label
    ]
)


st.sidebar.info(
    t(
        "synthetic_notice"
    )
)


scenario = (
    build_demo_scenario(
        scenario_name
    )
)


# =========================================================
# 24. HEADER
# =========================================================

st.title(
    t(
        "title"
    )
)


st.subheader(
    t(
        "subtitle"
    )
)


st.caption(
    t(
        "tagline"
    )
)


st.divider()


# =========================================================
# 25. TRANSACTION OVERVIEW
# =========================================================

st.header(
    t(
        "transaction_overview"
    )
)


st.write(
    scenario[
        "description"
    ]
)


transaction = (
    scenario[
        "transaction"
    ]
)


area_unit = (
    "শতক"
    if LANG == "bn"
    else "decimal"
)


col1, col2, col3, col4 = (
    st.columns(4)
)


col1.metric(
    t(
        "deed_id"
    ),
    transaction[
        "deed_id"
    ],
)


col2.metric(
    t(
        "parcel"
    ),
    transaction[
        "parcel_id"
    ],
)


col3.metric(
    t(
        "transfer_area"
    ),
    (
        f"{to_bangla_digits(transaction['transferred_area_decimal'])} "
        f"{area_unit}"
    ),
)


col4.metric(
    t(
        "portion_id"
    ),
    transaction[
        "portion_id"
    ],
)


# =========================================================
# 26. VERIFIED TRANSACTION FIELDS
# =========================================================

with st.expander(
    t(
        "verified_fields"
    )
):

    transaction_rows = []

    for key, value in (
        transaction.items()
    ):

        if LANG == "bn":

            display_key = (
                TRANSACTION_FIELD_BN.get(
                    key,
                    key,
                )
            )

            if key == "transferred_area_decimal":

                display_value = (
                    to_bangla_digits(
                        value
                    )
                )

            elif key == "execution_date":

                display_value = (
                    to_bangla_digits(
                        value
                    )
                )

            else:

                display_value = (
                    translate_value(
                        value
                    )
                )

        else:

            display_key = key
            display_value = value


        transaction_rows.append(
            {

                t("field"):
                    display_key,

                t("value"):
                    display_value,
            }
        )


    transaction_df = (
        pd.DataFrame(
            transaction_rows
        )
    )


    st.dataframe(
        transaction_df,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# 27. SCREENING SECTION
# =========================================================

st.header(
    t(
        "screening"
    )
)


verify_clicked = (
    st.button(
        t(
            "verify"
        ),
        type="primary",
        use_container_width=True,
    )
)


# =========================================================
# 28. RUN SCREENING
# =========================================================

if verify_clicked:

    report = (
        risk.verify_transaction(
            scenario[
                "ledger_df"
            ],

            scenario[
                "history_df"
            ],

            scenario[
                "mutation_df"
            ],

            transaction,

            scenario[
                "people_df"
            ],

            scenario[
                "parcels_df"
            ],
        )
    )


    st.divider()


    # =====================================================
    # 29. RESULT HEADER
    # =====================================================

    st.header(
        t(
            "result"
        )
    )


    show_risk_banner(
        report[
            "risk_level"
        ]
    )


    # =====================================================
    # 30. RESULT METRICS
    # =====================================================

    col1, col2, col3, col4 = (
        st.columns(4)
    )


    col1.metric(
        t(
            "overall_risk"
        ),
        display_risk_level(
            report[
                "risk_level"
            ]
        ),
    )


    col2.metric(
        t(
            "passed"
        ),
        to_bangla_digits(
            report[
                "pass_count"
            ]
        ),
    )


    col3.metric(
        t(
            "warnings"
        ),
        to_bangla_digits(
            report[
                "warning_count"
            ]
        ),
    )


    col4.metric(
        t(
            "failed"
        ),
        to_bangla_digits(
            report[
                "fail_count"
            ]
        ),
    )


    # =====================================================
    # 31. RULE TABLE
    # =====================================================

    st.subheader(
        t(
            "rule_checks"
        )
    )


    rules_df = (
        rule_dataframe(
            report
        )
    )


    st.dataframe(
        rules_df,
        use_container_width=True,
        hide_index=True,
    )


    # =====================================================
    # 32. DECISION EXPLANATION
    # =====================================================

    st.subheader(
        t(
            "decision"
        )
    )


    for rule_name, rule_result in (
        report[
            "rules"
        ].items()
    ):

        message = (
            translated_rule_message(
                rule_result
            )
        )


        display_code = (
            translated_rule_code(
                rule_result
            )
        )


        display_text = (
            f"{display_code} — "
            f"{message}"
        )


        if (
            rule_result[
                "status"
            ]
            ==
            "PASS"
        ):

            st.success(
                display_text
            )


        elif (
            rule_result[
                "status"
            ]
            ==
            "WARNING"
        ):

            st.warning(
                display_text
            )


        else:

            st.error(
                display_text
            )


    # =====================================================
    # 33. OWNERSHIP CONTEXT
    # =====================================================

    st.subheader(
        t(
            "ownership"
        )
    )


    ownership_display_df = (
        scenario[
            "ledger_df"
        ].copy()
    )


    if LANG == "bn":

        ownership_display_df = (
            ownership_display_df.rename(
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
        )


        area_column = (
            "মালিকানাধীন জমি (শতক)"
        )

        if (
            area_column
            in
            ownership_display_df.columns
        ):

            ownership_display_df[
                area_column
            ] = (
                ownership_display_df[
                    area_column
                ]
                .map(
                    to_bangla_digits
                )
            )


        if (
            "অবস্থা"
            in
            ownership_display_df.columns
        ):

            ownership_display_df[
                "অবস্থা"
            ] = (
                ownership_display_df[
                    "অবস্থা"
                ]
                .map(
                    lambda value:
                        translate_value(
                            value
                        )
                )
            )


    st.dataframe(
        ownership_display_df,
        use_container_width=True,
        hide_index=True,
    )


    # =====================================================
    # 34. TRANSACTION HISTORY
    # =====================================================

    with st.expander(
        t(
            "history"
        )
    ):

        if (
            scenario[
                "history_df"
            ].empty
        ):

            st.write(
                t(
                    "no_history"
                )
            )


        else:

            history_display_df = (
                scenario[
                    "history_df"
                ].copy()
            )


            if LANG == "bn":

                history_display_df = (
                    history_display_df.rename(
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
                )


                if (
                    "লেনদেনের অবস্থা"
                    in
                    history_display_df.columns
                ):

                    history_display_df[
                        "লেনদেনের অবস্থা"
                    ] = (
                        history_display_df[
                            "লেনদেনের অবস্থা"
                        ]
                        .map(
                            lambda value:
                                translate_value(
                                    value
                                )
                        )
                    )


            st.dataframe(
                history_display_df,
                use_container_width=True,
                hide_index=True,
            )


    # =====================================================
    # 35. MUTATION INFORMATION
    # =====================================================

    with st.expander(
        t(
            "mutation"
        )
    ):

        mutation_display_df = (
            scenario[
                "mutation_df"
            ].copy()
        )


        if LANG == "bn":

            mutation_display_df = (
                mutation_display_df.rename(
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
            )


            if (
                "অবস্থা"
                in
                mutation_display_df.columns
            ):

                mutation_display_df[
                    "অবস্থা"
                ] = (
                    mutation_display_df[
                        "অবস্থা"
                    ]
                    .map(
                        lambda value:
                            translate_value(
                                value
                            )
                    )
                )


        st.dataframe(
            mutation_display_df,
            use_container_width=True,
            hide_index=True,
        )


    # =====================================================
    # 36. DISCLAIMER
    # =====================================================

    st.divider()


    st.caption(
        t(
            "disclaimer"
        )
    )


    st.info(
        t(
            "demo_mode"
        )
    )


# =========================================================
# 37. FOOTER
# =========================================================

st.divider()


st.caption(
    t(
        "footer"
    )
)