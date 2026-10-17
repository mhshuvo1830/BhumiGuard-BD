import pandas as pd

from .ledger import process_transfer


def check_duplicate_deed(
    history_df,
    deed_id
):
    matches = history_df[
        history_df["deed_id"] == deed_id
    ]

    if matches.empty:
        return {
            "duplicate": False,
            "reason": "DEED_ID_AVAILABLE"
        }

    return {
        "duplicate": True,
        "reason": "DUPLICATE_DEED",
        "existing_records": len(matches)
    }


def check_double_sale(
    history_df,
    transaction
):
    portion_id = transaction.get(
        "portion_id"
    )

    if portion_id is None:
        return {
            "double_sale": False,
            "reason": "NO_PORTION_ID"
        }

    required_columns = {
        "parcel_id",
        "portion_id",
        "transaction_status",
        "deed_id",
        "buyer_id",
    }

    if not required_columns.issubset(
        history_df.columns
    ):
        return {
            "double_sale": False,
            "reason": "HISTORY_SCHEMA_INCOMPLETE"
        }

    previous_sales = history_df[
        (
            history_df["parcel_id"]
            == transaction["parcel_id"]
        )
        &
        (
            history_df["portion_id"]
            == portion_id
        )
        &
        (
            history_df[
                "transaction_status"
            ]
            == "VALID"
        )
    ]

    if previous_sales.empty:
        return {
            "double_sale": False,
            "reason": "NO_PREVIOUS_SALE"
        }

    return {
        "double_sale": True,
        "reason": "DOUBLE_SALE",

        "previous_deeds":
            previous_sales[
                "deed_id"
            ].tolist(),

        "previous_buyers":
            previous_sales[
                "buyer_id"
            ].tolist(),
    }


def check_deed_mutation_match(
    mutation_df,
    transaction
):
    required_columns = {
        "parcel_id",
        "portion_id",
        "mutation_owner_id",
        "status",
    }

    if not required_columns.issubset(
        mutation_df.columns
    ):
        return {
            "match": None,
            "reason":
                "MUTATION_SCHEMA_INCOMPLETE"
        }

    records = mutation_df[
        (
            mutation_df["parcel_id"]
            == transaction["parcel_id"]
        )
        &
        (
            mutation_df["portion_id"]
            == transaction.get(
                "portion_id"
            )
        )
        &
        (
            mutation_df["status"]
            == "ACTIVE"
        )
    ]

    if records.empty:
        return {
            "match": None,
            "reason": "NO_MUTATION_RECORD"
        }

    mutation_owners = set(
        records[
            "mutation_owner_id"
        ]
    )

    deed_seller = transaction[
        "seller_id"
    ]

    if deed_seller in mutation_owners:
        return {
            "match": True,
            "reason": "MUTATION_MATCH",
            "mutation_owners":
                sorted(
                    mutation_owners
                ),
        }

    return {
        "match": False,
        "reason":
            "DEED_MUTATION_MISMATCH",

        "deed_seller":
            deed_seller,

        "mutation_owners":
            sorted(
                mutation_owners
            ),
    }


def process_transfer_full_checks(
    ledger_df,
    history_df,
    mutation_df,
    transaction,
    people_df,
    parcels_df
):
    original_ledger = (
        ledger_df.copy(deep=True)
    )

    original_history = (
        history_df.copy(deep=True)
    )

    # ---------------------------------
    # 1. Duplicate deed
    # ---------------------------------

    duplicate_result = (
        check_duplicate_deed(
            history_df,
            transaction["deed_id"]
        )
    )

    if duplicate_result["duplicate"]:

        return (
            original_ledger,
            original_history,
            {
                "valid": False,
                "reason": "DUPLICATE_DEED",
                "existing_records":
                    duplicate_result[
                        "existing_records"
                    ],
            }
        )

    # ---------------------------------
    # 2. Double-sale
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

        return (
            original_ledger,
            original_history,
            {
                "valid": False,
                "reason": "DOUBLE_SALE",

                "previous_deeds":
                    double_sale_result[
                        "previous_deeds"
                    ],

                "previous_buyers":
                    double_sale_result[
                        "previous_buyers"
                    ],
            }
        )

    # ---------------------------------
    # 3. Mutation consistency
    # ---------------------------------

    mutation_result = (
        check_deed_mutation_match(
            mutation_df,
            transaction
        )
    )

    if mutation_result["match"] is False:

        return (
            original_ledger,
            original_history,
            {
                "valid": False,
                "reason":
                    "DEED_MUTATION_MISMATCH",

                "deed_seller":
                    mutation_result[
                        "deed_seller"
                    ],

                "mutation_owners":
                    mutation_result[
                        "mutation_owners"
                    ],
            }
        )

    # ---------------------------------
    # 4. Ownership / transfer validation
    # ---------------------------------

    (
        updated_ledger,
        transfer_result
    ) = process_transfer(
        ledger_df,
        transaction,
        people_df,
        parcels_df
    )

    if not transfer_result["valid"]:

        return (
            original_ledger,
            original_history,
            transfer_result
        )

    # ---------------------------------
    # 5. Store accepted transaction
    # ---------------------------------

    accepted_transaction = (
        transaction.copy()
    )

    accepted_transaction[
        "transaction_status"
    ] = "VALID"

    updated_history = pd.concat(
        [
            original_history,
            pd.DataFrame(
                [accepted_transaction]
            )
        ],
        ignore_index=True
    )

    return (
        updated_ledger,
        updated_history,
        {
            "valid": True,
            "reason": "VALID_TRANSFER",

            "mutation_status":
                mutation_result[
                    "reason"
                ],
        }
    )
