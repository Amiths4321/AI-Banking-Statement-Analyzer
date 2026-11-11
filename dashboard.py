
import streamlit as st
import plotly.express as px


def show_dashboard(analysis, transactions):

    st.title("Financial Analytics Dashboard")

    # KPI cards
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Income",
        f"₹{analysis['total_income']:,.2f}"
    )

    col2.metric(
        "Total Expenses",
        f"₹{analysis['total_expenses']:,.2f}"
    )

    col3.metric(
        "Net Cash Flow",
        f"₹{analysis['net_cash_flow']:,.2f}"
    )

    st.divider()

    # Monthly income and expenses
    st.subheader("Monthly Financial Performance")

    monthly = analysis["monthly_summary"]

    if not monthly.empty:

        monthly_chart = monthly.melt(
            id_vars=["month"],
            value_vars=["income", "expenses"],
            var_name="Type",
            value_name="Amount"
        )

        fig_monthly = px.bar(
            monthly_chart,
            x="month",
            y="Amount",
            color="Type",
            barmode="group",
            title="Monthly Income vs Expenses"
        )

        st.plotly_chart(
            fig_monthly,
            use_container_width=True
        )

    # Expense category chart
    st.subheader("Expense Breakdown by Category")

    expense_data = (
        analysis["expense_summary"]
        .reset_index()
    )

    if not expense_data.empty:

        expense_data.columns = ["Category", "Amount"]

        fig_expense = px.pie(
            expense_data,
            names="Category",
            values="Amount",
            hole=0.45,
            title="Expense Distribution"
        )

        st.plotly_chart(
            fig_expense,
            use_container_width=True
        )

    # Transaction history
    st.subheader("Transaction History")

    st.dataframe(
        transactions,
        use_container_width=True,
        hide_index=True
    )
