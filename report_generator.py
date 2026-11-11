
import pandas as pd
from io import BytesIO


def generate_excel_report(
    transactions,
    analysis,
    anomalies
):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        # Sheet 1: All transactions
        transactions.to_excel(
            writer,
            sheet_name="Transactions",
            index=False
        )

        # Sheet 2: Financial summary
        summary = pd.DataFrame({
            "Metric": [
                "Total Income",
                "Total Expenses",
                "Net Cash Flow"
            ],
            "Amount": [
                analysis["total_income"],
                analysis["total_expenses"],
                analysis["net_cash_flow"]
            ]
        })

        summary.to_excel(
            writer,
            sheet_name="Financial Summary",
            index=False
        )

        # Sheet 3: Monthly summary
        analysis["monthly_summary"].to_excel(
            writer,
            sheet_name="Monthly Summary",
            index=False
        )

        # Sheet 4: Expense categories
        expense_summary = (
            analysis["expense_summary"]
            .rename("Amount")
            .reset_index()
        )

        expense_summary.to_excel(
            writer,
            sheet_name="Expense Categories",
            index=False
        )

        # Sheet 5: Anomalies
        anomalies.to_excel(
            writer,
            sheet_name="Anomalies",
            index=False
        )

    output.seek(0)

    return output.getvalue()
