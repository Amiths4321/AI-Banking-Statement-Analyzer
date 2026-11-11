
import streamlit as st
import fitz
import pandas as pd

st.set_page_config(
    page_title="AI Banking Statement Analyzer",
    page_icon="🏦",
    layout="wide"
)

st.title("AI Banking Statement Analyzer")

st.write(
    "Upload your bank statement to analyze "
    "income, expenses and financial transactions."
)

uploaded_file = st.file_uploader(
    "Upload Bank Statement",
    type=["pdf", "xlsx", "xls"]
)

if uploaded_file is not None:

    st.success("Bank statement uploaded successfully!")

    file_name = uploaded_file.name
    file_type = uploaded_file.type

    st.write("**File name:**", file_name)
    st.write("**File type:**", file_type)

    if file_name.lower().endswith(".pdf"):

        pdf_document = fitz.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf"
        )

        st.write("**Total pages:**", len(pdf_document))

        for page_number, page in enumerate(pdf_document):

            st.subheader(f"Page {page_number + 1}")

            page_text = page.get_text()

            st.text_area(
                f"Page {page_number + 1} content",
                page_text,
                height=200
            )

    else:

        excel_data = pd.read_excel(
            uploaded_file,
            sheet_name=None
        )

        st.write("**Total sheets:**", len(excel_data))

        for sheet_name, dataframe in excel_data.items():

            st.subheader(f"Sheet: {sheet_name}")

            st.dataframe(dataframe, use_container_width=True)
