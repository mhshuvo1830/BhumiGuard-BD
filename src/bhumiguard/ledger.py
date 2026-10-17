import pandas as pd


def get_owner_area(
    ledger_df,
    parcel_id,
    owner_id
):
    rows = ledger_df[
        (ledger_df["parcel_id"] == parcel_id) &
        (ledger_df["owner_id"] == owner_id) &
        (ledger_df["status"] == "ACTIVE")
    ]

    if rows.empty:
        return 0.0

    return float(
        rows["owned_area_decimal"].sum()
    )


def next_ownership_id(ledger_df):
    numbers = []

    for value in ledger_df["ownership_id"]:
        value = str(value)

        if value.startswith("OWN"):

            number = value[3:]

            if number.isdigit():
                numbers.append(
                    int(number)
                )

    next_number = (
        max(numbers, default=0) + 1
    )

    return f"OWN{next_number:03d}"


def check_ledger_integrity(
    ledger_df,
    parcels_df,
    tolerance=1e-9
):
    required_ledger_columns = {
        "ownership_id",
        "parcel_id",
        "owner_id",
        "owned_area_decimal",
        "status",
    }

    required_parcel_columns = {
        "parcel_id",
        "total_area_decimal",
    }

    if not required_ledger_columns.issubset(
        ledger_df.columns
    ):
        return False

    if not required_parcel_columns.issubset(
        parcels_df.columns
    ):
        return False

    # No negative ownership
    if (
        ledger_df[
            "owned_area_decimal"
        ] < 0
    ).any():
        return False

    # Every ownership row must reference a real parcel
    if (
        ~ledger_df[
            "parcel_id"
        ].isin(
            parcels_df[
                "parcel_id"
            ]
        )
    ).any():
        return False

    active = ledger_df[
        ledger_df["status"] == "ACTIVE"
    ].copy()

    active_totals = (
        active
        .groupby(
            "parcel_id",
            as_index=False
        )[
            "owned_area_decimal"
        ]
        .sum()
    )

    parcel_totals = parcels_df[
        [
            "parcel_id",
            "total_area_decimal"
        ]
    ].copy()

    comparison = parcel_totals.merge(
        active_totals,
        on="parcel_id",
        how="left"
    )

    comparison[
        "owned_area_decimal"
    ] = comparison[
        "owned_area_decimal"
    ].fillna(0.0)

    difference = (
        comparison[
            "owned_area_decimal"
        ]
        -
        comparison[
            "total_area_decimal"
        ]
    ).abs()

    return bool(
        (difference <= tolerance).all()
    )


def process_transfer(
    ledger_df,
    transaction,
    people_df,
    parcels_df
):
    original_ledger = (
        ledger_df.copy(deep=True)
    )

    updated_ledger = (
        ledger_df.copy(deep=True)
    )

    seller_id = transaction["seller_id"]
    buyer_id = transaction["buyer_id"]
    parcel_id = transaction["parcel_id"]

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
    # Basic validation
    # ---------------------------------

    if seller_id not in person_ids:

        return original_ledger, {
            "valid": False,
            "reason": "SELLER_NOT_FOUND"
        }

    if buyer_id not in person_ids:

        return original_ledger, {
            "valid": False,
            "reason": "BUYER_NOT_FOUND"
        }

    if parcel_id not in parcel_ids:

        return original_ledger, {
            "valid": False,
            "reason": "PARCEL_NOT_FOUND"
        }

    if seller_id == buyer_id:

        return original_ledger, {
            "valid": False,
            "reason": "SELLER_BUYER_SAME"
        }

    if transfer_area <= 0:

        return original_ledger, {
            "valid": False,
            "reason": "INVALID_TRANSFER_AREA"
        }

    # ---------------------------------
    # Seller ownership
    # ---------------------------------

    seller_available = get_owner_area(
        updated_ledger,
        parcel_id,
        seller_id
    )

    if seller_available <= 0:

        return original_ledger, {
            "valid": False,
            "reason": "SELLER_NOT_OWNER",
            "seller_available": 0.0
        }

    if transfer_area > seller_available:

        return original_ledger, {
            "valid": False,
            "reason":
                "INSUFFICIENT_OWNERSHIP",

            "seller_available":
                seller_available,

            "requested_area":
                transfer_area
        }

    # ---------------------------------
    # Deduct seller ownership
    # ---------------------------------

    seller_indices = updated_ledger[
        (updated_ledger["parcel_id"] == parcel_id) &
        (updated_ledger["owner_id"] == seller_id) &
        (updated_ledger["status"] == "ACTIVE")
    ].index.tolist()

    remaining_to_deduct = transfer_area

    for index in seller_indices:

        row_area = float(
            updated_ledger.loc[
                index,
                "owned_area_decimal"
            ]
        )

        deduction = min(
            row_area,
            remaining_to_deduct
        )

        new_area = (
            row_area - deduction
        )

        updated_ledger.loc[
            index,
            "owned_area_decimal"
        ] = new_area

        if abs(new_area) <= 1e-9:

            updated_ledger.loc[
                index,
                "owned_area_decimal"
            ] = 0.0

            updated_ledger.loc[
                index,
                "status"
            ] = "INACTIVE"

        remaining_to_deduct -= (
            deduction
        )

        if remaining_to_deduct <= 1e-9:
            break

    # ---------------------------------
    # Add buyer ownership
    # ---------------------------------

    buyer_indices = updated_ledger[
        (updated_ledger["parcel_id"] == parcel_id) &
        (updated_ledger["owner_id"] == buyer_id) &
        (updated_ledger["status"] == "ACTIVE")
    ].index.tolist()

    if buyer_indices:

        buyer_index = buyer_indices[0]

        updated_ledger.loc[
            buyer_index,
            "owned_area_decimal"
        ] = (
            float(
                updated_ledger.loc[
                    buyer_index,
                    "owned_area_decimal"
                ]
            )
            + transfer_area
        )

    else:

        new_row = {
            "ownership_id":
                next_ownership_id(
                    updated_ledger
                ),

            "parcel_id":
                parcel_id,

            "owner_id":
                buyer_id,

            "owned_area_decimal":
                transfer_area,

            "valid_from":
                transaction[
                    "execution_date"
                ],

            "status":
                "ACTIVE"
        }

        updated_ledger = pd.concat(
            [
                updated_ledger,
                pd.DataFrame(
                    [new_row]
                )
            ],
            ignore_index=True
        )

    # ---------------------------------
    # Final integrity protection
    # ---------------------------------

    if not check_ledger_integrity(
        updated_ledger,
        parcels_df
    ):

        return original_ledger, {
            "valid": False,
            "reason":
                "LEDGER_INTEGRITY_FAILURE"
        }

    return updated_ledger, {
        "valid": True,
        "reason": "VALID_TRANSFER",

        "seller_available_before":
            seller_available,

        "transferred_area":
            transfer_area
    }
