
import pandas as pd


def detect_anomalies(df):

    df = df.copy()

    # Ensure numeric transaction amounts
    for col in ["debit", "credit", "balance"]:
        df[col] = pd.to_numeric(
            df[col], errors="coerce"
        )

    # Prepare date column
    df["date"] = pd.to_datetime(
        df["date"], errors="coerce"
    )

    df["anomaly_type"] = ""
    df["severity"] = ""

    # 1. Detect duplicate transactions
    duplicate_mask = df.duplicated(
        subset=["date", "description", "debit", "credit"],
        keep=False
    )

    df.loc[duplicate_mask, "anomaly_type"] += (
        "Possible duplicate transaction; "
    )

    df.loc[duplicate_mask, "severity"] = "Review"

    # 2. Detect unusually large debits
    valid_debits = df.loc[
        df["debit"] > 0, "debit"
    ]

    if len(valid_debits) >= 5:

        debit_threshold = valid_debits.quantile(0.95)

        large_debit_mask = (
            df["debit"] > debit_threshold
        )

        df.loc[large_debit_mask, "anomaly_type"] += (
            "Unusually large debit; "
        )

        df.loc[large_debit_mask, "severity"] = "Review"

    # 3. Detect unusually large credits
    valid_credits = df.loc[
        df["credit"] > 0, "credit"
    ]

    if len(valid_credits) >= 5:

        credit_threshold = valid_credits.quantile(0.95)

        large_credit_mask = (
            df["credit"] > credit_threshold
        )

        df.loc[large_credit_mask, "anomaly_type"] += (
            "Unusually large credit; "
        )

        df.loc[large_credit_mask, "severity"] = "Review"

    # 4. Identify flagged transactions
    anomalies = df[
        df["anomaly_type"] != ""
    ].copy()

    return anomalies
