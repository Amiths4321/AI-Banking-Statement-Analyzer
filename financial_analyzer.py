
import pandas as pd


def analyze_transactions(df):

    df = df.copy()

    # Convert transaction amounts to numeric
    for column in ["debit", "credit"]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        ).fillna(0)

    # Total income and expenses
    total_income = df["credit"].sum()
    total_expenses = df["debit"].sum()

    # Net cash flow
    net_cash_flow = total_income - total_expenses

    # Category-wise expenses
    expense_summary = (
        df.groupby("category")["debit"]
        .sum()
        .sort_values(ascending=False)
    )

    # Category-wise income
    income_summary = (
        df.groupby("category")["credit"]
        .sum()
        .sort_values(ascending=False)
    )

    # Monthly summary
    df["date"] = pd.to_datetime(
        df["date"], errors="coerce"
    )

    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly_summary = (
        df.groupby("month")
        .agg(
            income=("credit", "sum"),
            expenses=("debit", "sum")
        )
        .reset_index()
    )

    monthly_summary["net_cash_flow"] = (
        monthly_summary["income"]
        - monthly_summary["expenses"]
    )

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_cash_flow": net_cash_flow,
        "expense_summary": expense_summary,
        "income_summary": income_summary,
        "monthly_summary": monthly_summary
    }
