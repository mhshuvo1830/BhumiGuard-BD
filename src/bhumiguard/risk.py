from .ledger import get_owner_area

from .validation import (
    check_duplicate_deed,
    check_double_sale,
    check_deed_mutation_match,
)


def evaluate_transaction_rules(
    ledger_df,
    history_df,
    mutation_df,
    transaction,
    people_df,
    parcels_df
):
    rules = {}

    seller_id = transaction["seller_id"]
    buyer_id = transaction["buyer_id"]
    parcel_id = transaction["parcel_id"]
    deed_id = transaction["deed_id"]

    transfer_area = float(
        transaction[
            "transferred_area_decimal"
        ]
    )

    person_ids = set(
        people_df["person_id"]
    )

    parcel_ids = set(
        parcels_df["parcel_id"]
    )

    # ---------------------------------
    # Rule 1: Deed ID
    # ---------------------------------

    duplicate_result = (
        check_duplicate_deed(
            history_df,
            deed_id
        )
    )

    if duplicate_result["duplicate"]:

        rules["deed_id_check"] = {
            "status": "FAIL",
            "code": "DUPLICATE_DEED",
            "message": (
                f"Deed ID {deed_id} "
                "already exists in the "
                "accepted transaction history."
            )
        }

    else:

        rules["deed_id_check"] = {
            "status": "PASS",
            "code": "DEED_ID_AVAILABLE",
            "message":
                "Deed ID is not duplicated."
        }

    # ---------------------------------
    # Rule 2: Party references
    # ---------------------------------

    if seller_id not in person_ids:

        rules["seller_reference_check"] = {
            "status": "FAIL",
            "code": "SELLER_NOT_FOUND",
            "message":
                "Seller was not found in the registry."
        }

    else:

        rules["seller_reference_check"] = {
            "status": "PASS",
            "code": "SELLER_FOUND",
            "message":
                "Seller exists in the registry."
        }

    if buyer_id not in person_ids:

        rules["buyer_reference_check"] = {
            "status": "FAIL",
            "code": "BUYER_NOT_FOUND",
            "message":
                "Buyer was not found in the registry."
        }

    elif seller_id == buyer_id:

        rules["buyer_reference_check"] = {
            "status": "FAIL",
            "code": "SELLER_BUYER_SAME",
            "message":
                "Seller and buyer cannot be the same party."
        }

    else:

        rules["buyer_reference_check"] = {
            "status": "PASS",
            "code": "BUYER_FOUND",
            "message":
                "Buyer exists and differs from the seller."
        }

    # ---------------------------------
    # Rule 3: Parcel reference
    # ---------------------------------

    parcel_exists = (
        parcel_id in parcel_ids
    )

    if parcel_exists:

        rules["parcel_check"] = {
            "status": "PASS",
            "code": "PARCEL_FOUND",
            "message":
                "Parcel exists in the registry."
        }

    else:

        rules["parcel_check"] = {
            "status": "FAIL",
            "code": "PARCEL_NOT_FOUND",
            "message":
                "Parcel was not found in the registry."
        }

    # ---------------------------------
    # Rule 4: Seller ownership
    # ---------------------------------

    seller_area = get_owner_area(
        ledger_df,
        parcel_id,
        seller_id
    )

    if seller_area > 0:

        rules["seller_ownership_check"] = {
            "status": "PASS",
            "code": "SELLER_IS_OWNER",
            "message": (
                f"Seller currently owns "
                f"{seller_area} decimal "
                "in the parcel."
            )
        }

    else:

        rules["seller_ownership_check"] = {
            "status": "FAIL",
            "code": "SELLER_NOT_OWNER",
            "message":
                "Seller has no active ownership "
                "in this parcel."
        }

    # ---------------------------------
    # Rule 5: Transfer area
    # ---------------------------------

    if transfer_area <= 0:

        rules["area_check"] = {
            "status": "FAIL",
            "code":
                "INVALID_TRANSFER_AREA",
            "message":
                "Transfer area must be positive."
        }

    elif (
        seller_area > 0
        and transfer_area > seller_area
    ):

        rules["area_check"] = {
            "status": "FAIL",
            "code":
                "INSUFFICIENT_OWNERSHIP",

            "message": (
                f"Requested transfer is "
                f"{transfer_area} decimal, "
                f"but the seller currently "
                f"owns {seller_area} decimal."
            )
        }

    elif seller_area <= 0:

        rules["area_check"] = {
            "status": "WARNING",
            "code":
                "AREA_CHECK_NOT_APPLICABLE",

            "message":
                "Transfer-area sufficiency cannot "
                "be confirmed because seller "
                "ownership is unavailable."
        }

    else:

        rules["area_check"] = {
            "status": "PASS",
            "code": "AREA_AVAILABLE",
            "message": (
                f"Requested transfer of "
                f"{transfer_area} decimal "
                "is within seller ownership."
            )
        }

    # ---------------------------------
    # Rule 6: Double-sale
    # ---------------------------------

    double_sale_result = (
        check_double_sale(
            history_df,
            transaction
        )
    )

    if double_sale_result[
        "double_sale"
    ]:

        rules["double_sale_check"] = {
            "status": "FAIL",
            "code": "DOUBLE_SALE",
            "message":
                "The same identified land portion "
                "appears in a previous valid sale."
        }

    elif (
        double_sale_result["reason"]
        == "NO_PORTION_ID"
    ):

        rules["double_sale_check"] = {
            "status": "WARNING",
            "code":
                "PORTION_ID_UNAVAILABLE",
            "message":
                "Double-sale verification is "
                "incomplete because no portion "
                "identifier is available."
        }

    elif (
        double_sale_result["reason"]
        == "HISTORY_SCHEMA_INCOMPLETE"
    ):

        rules["double_sale_check"] = {
            "status": "WARNING",
            "code":
                "HISTORY_SCHEMA_INCOMPLETE",
            "message":
                "Transaction history does not contain "
                "all fields required for double-sale "
                "verification."
        }

    else:

        rules["double_sale_check"] = {
            "status": "PASS",
            "code": "NO_PREVIOUS_SALE",
            "message":
                "No previous valid sale was found "
                "for this identified portion."
        }

    # ---------------------------------
    # Rule 7: Mutation consistency
    # ---------------------------------

    mutation_result = (
        check_deed_mutation_match(
            mutation_df,
            transaction
        )
    )

    if mutation_result["match"] is True:

        rules["mutation_check"] = {
            "status": "PASS",
            "code": "MUTATION_MATCH",
            "message":
                "Deed seller matches the active "
                "mutation-side owner."
        }

    elif mutation_result["match"] is False:

        mutation_owners = ", ".join(
            mutation_result[
                "mutation_owners"
            ]
        )

        rules["mutation_check"] = {
            "status": "FAIL",
            "code":
                "DEED_MUTATION_MISMATCH",

            "message": (
                f"Deed seller is {seller_id}, "
                f"while the mutation-side record "
                f"lists {mutation_owners}."
            )
        }

    elif (
        mutation_result["reason"]
        == "MUTATION_SCHEMA_INCOMPLETE"
    ):

        rules["mutation_check"] = {
            "status": "WARNING",
            "code":
                "MUTATION_SCHEMA_INCOMPLETE",

            "message":
                "Mutation data does not contain "
                "all fields required for verification."
        }

    else:

        rules["mutation_check"] = {
            "status": "WARNING",
            "code": "NO_MUTATION_RECORD",
            "message":
                "No matching mutation record is "
                "available for this parcel portion."
        }

    return rules


def calculate_risk_level(rules):
    pass_count = sum(
        result["status"] == "PASS"
        for result in rules.values()
    )

    warning_count = sum(
        result["status"] == "WARNING"
        for result in rules.values()
    )

    fail_count = sum(
        result["status"] == "FAIL"
        for result in rules.values()
    )

    if fail_count > 0:
        risk_level = "HIGH"

    elif warning_count > 0:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    return {
        "risk_level":
            risk_level,

        "pass_count":
            pass_count,

        "warning_count":
            warning_count,

        "fail_count":
            fail_count,
    }


def verify_transaction(
    ledger_df,
    history_df,
    mutation_df,
    transaction,
    people_df,
    parcels_df
):
    rules = evaluate_transaction_rules(
        ledger_df,
        history_df,
        mutation_df,
        transaction,
        people_df,
        parcels_df
    )

    summary = calculate_risk_level(
        rules
    )

    return {
        "deed_id":
            transaction["deed_id"],

        "parcel_id":
            transaction["parcel_id"],

        "seller_id":
            transaction["seller_id"],

        "buyer_id":
            transaction["buyer_id"],

        "risk_level":
            summary["risk_level"],

        "pass_count":
            summary["pass_count"],

        "warning_count":
            summary["warning_count"],

        "fail_count":
            summary["fail_count"],

        "rules":
            rules,

        "disclaimer":
            (
                "Screening result only. "
                "It does not establish legal title "
                "or prove fraud."
            ),
    }


def format_risk_report(report):
    lines = []

    lines.append(
        "BHUMIGUARD BD — PRE-REGISTRATION CHECK"
    )

    lines.append(
        "=" * 50
    )

    lines.append(
        f"Deed: {report['deed_id']}"
    )

    lines.append(
        f"Parcel: {report['parcel_id']}"
    )

    lines.append(
        f"Seller: {report['seller_id']}"
    )

    lines.append(
        f"Buyer: {report['buyer_id']}"
    )

    lines.append("")
    lines.append("RULE CHECKS")
    lines.append("-" * 50)

    for result in report[
        "rules"
    ].values():

        lines.append(
            f"{result['status']:7} | "
            f"{result['code']}"
        )

        lines.append(
            f"          {result['message']}"
        )

    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 50)

    lines.append(
        f"PASS: {report['pass_count']}"
    )

    lines.append(
        f"WARNING: {report['warning_count']}"
    )

    lines.append(
        f"FAIL: {report['fail_count']}"
    )

    lines.append(
        f"OVERALL RISK: "
        f"{report['risk_level']}"
    )

    lines.append("")
    lines.append(
        report["disclaimer"]
    )

    return "\n".join(lines)
