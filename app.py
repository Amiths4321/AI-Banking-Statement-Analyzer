import streamlit as st
from transaction_extractor import (
    extract_excel_transactions,
    extract_pdf_transactions
)
from anomaly_detector import detect_anomalies
from dashboard import show_dashboard
from transaction_categorizer import categorize_transactions
from financial_analyzer import analyze_transactions

# ---------------------------------
# PAGE CONFIGURATION (Must be first)
# ---------------------------------
st.set_page_config(
    page_title="AI Banking Statement Analyzer",
    page_icon="🏦",
    layout="wide"
)

st.title("AI Banking Statement Analyzer")
st.write("Upload a bank statement to extract transactions.")

# ---------------------------------
# FILE UPLOADER
# ---------------------------------
uploaded_file = st.file_uploader(
    "Upload Bank Statement",
    type=["pdf", "xlsx", "xls"]
)

if uploaded_file is not None:

    st.success("Bank statement uploaded successfully!")
    st.write("File:", uploaded_file.name)

    if st.button("Extract Transactions"):

        try:
            with st.spinner("Extracting transactions..."):

                if uploaded_file.name.lower().endswith(".pdf"):
                    transactions = extract_pdf_transactions(
                        uploaded_file
                    )
                else:
                    transactions = extract_excel_transactions(
                        uploaded_file
                    )

                st.session_state["transactions"] = transactions
                st.session_state["source_file"] = uploaded_file.name

        except Exception as error:
            st.error(f"Extraction failed: {error}")

    # Display transactions and categorization if available in session state
    if (
        "transactions" in st.session_state
        and st.session_state.get("source_file") == uploaded_file.name
    ):

        df = st.session_state["transactions"]

        categorized_df = categorize_transactions(df)
        st.session_state["categorized_transactions"] = categorized_df

        st.subheader("Categorized Transactions")
        st.dataframe(
            categorized_df,
            use_container_width=True
        )

        st.subheader("Extracted Transactions")
        st.dataframe(
            df,
            use_container_width=True
        )

        st.write("Total transactions:", len(df))

        st.info(
            "Verify dates, amounts and balances against "
            "the original statement before proceeding."
        )

        # ---------------------------------
        # FINANCIAL ANALYSIS & CHARTS
        # ---------------------------------
        st.divider()
        st.subheader("Financial Summary")

        analysis = analyze_transactions(categorized_df)
        st.session_state["financial_analysis"] = analysis

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

        st.subheader("Expense by Category")
        st.bar_chart(
            analysis["expense_summary"]
        )

        st.subheader("Monthly Financial Summary")
        st.dataframe(
            analysis["monthly_summary"],
            use_container_width=True
        )

        # ---------------------------------
        # DASHBOARD & ANOMALY DETECTION
        # ---------------------------------
        show_dashboard(
            analysis,
            categorized_df
        )

        st.subheader("Transaction Anomaly Detection")

        anomalies = detect_anomalies(categorized_df)
        st.session_state["anomalies"] = anomalies

        if anomalies.empty:
            st.success("No transactions were flagged for review.")
        else:
            st.warning(
                f"{len(anomalies)} transactions flagged for review."
            )
            st.dataframe(
                anomalies,
                use_container_width=True
            )

            st.divider()

            st.subheader("Download Financial Report")

            if st.button("Generate Excel Report"):

                excel_file = generate_excel_report(
                    categorized_df,
                    analysis,
                    anomalies
                )

                st.download_button(
                    label="Download Excel Report",
                    data=excel_file,
                    file_name="Banking_Financial_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )