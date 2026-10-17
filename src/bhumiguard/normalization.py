import re
import unicodedata


BANGLA_DIGITS = str.maketrans(
    "০১২৩৪৫৬৭৮৯",
    "0123456789"
)


SURVEY_ALIASES = {
    "CS": "CS",
    "C S": "CS",
    "C.S": "CS",
    "C.S.": "CS",
    "সি এস": "CS",

    "SA": "SA",
    "S A": "SA",
    "S.A": "SA",
    "S.A.": "SA",
    "এস এ": "SA",

    "RS": "RS",
    "R S": "RS",
    "R.S": "RS",
    "R.S.": "RS",
    "আর এস": "RS",

    "BS": "BS",
    "B S": "BS",
    "B.S": "BS",
    "B.S.": "BS",
    "বি এস": "BS",
}


def bangla_to_english_digits(value):
    if value is None:
        return None

    return str(value).translate(
        BANGLA_DIGITS
    )


def normalize_land_number(value):
    if value is None:
        return None

    value = bangla_to_english_digits(
        value
    )

    value = unicodedata.normalize(
        "NFKC",
        value
    )

    value = value.strip()

    labels = [
        "দাগ নং",
        "দাগ নম্বর",
        "দাগ",
        "খতিয়ান নং",
        "খতিয়ান নং",
        "খতিয়ান নম্বর",
        "খতিয়ান নম্বর",
        "খতিয়ান",
        "খতিয়ান",
        "নং",
        "নম্বর",
        "NO.",
        "NO",
    ]

    for label in labels:
        value = value.replace(
            label,
            ""
        )

    value = value.strip()

    digits = re.sub(
        r"[^0-9]",
        "",
        value
    )

    if digits == "":
        return None

    return str(
        int(digits)
    )


def normalize_survey_type(value):
    if value is None:
        return None

    value = unicodedata.normalize(
        "NFKC",
        str(value)
    )

    value = " ".join(
        value.strip()
        .upper()
        .split()
    )

    return SURVEY_ALIASES.get(
        value,
        value
    )


def normalize_location(value):
    if value is None:
        return None

    value = unicodedata.normalize(
        "NFKC",
        str(value)
    )

    value = " ".join(
        value.strip()
        .split()
    )

    return value.upper()


def create_parcel_key(
    district,
    upazila,
    mouza,
    survey_type,
    khatian_no,
    dag_no
):
    district_n = normalize_location(
        district
    )

    upazila_n = normalize_location(
        upazila
    )

    mouza_n = normalize_location(
        mouza
    )

    survey_n = normalize_survey_type(
        survey_type
    )

    khatian_n = normalize_land_number(
        khatian_no
    )

    dag_n = normalize_land_number(
        dag_no
    )

    components = [
        district_n,
        upazila_n,
        mouza_n,
        survey_n,
        khatian_n,
        dag_n,
    ]

    if any(
        value is None
        for value in components
    ):
        return None

    return "|".join(
        components
    )
