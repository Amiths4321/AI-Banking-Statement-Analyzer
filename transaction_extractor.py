
import io
import json
import re

import fitz
import pandas as pd
import ollama


OLLAMA_HOST = "http://10.22.39.192:11434"
MODEL = "qwen2.5vl:latest"

client = ollama.Client(host=OLLAMA_HOST)

COLUMNS = [
    "date", "description", "debit", "credit", "balance"
]


def extract_excel_transactions(uploaded_file):
    sheets = pd.read_excel(
        io.BytesIO(uploaded_file.getvalue()),
        sheet_name=None
    )

    transactions = []

    for sheet_name, df in sheets.items():
        # Initial support for common column names
        df.columns = [
            str(col).strip().lower()
            for col in df.columns
        ]

        aliases = {
            "transaction date": "date",
            "txn date": "date",
            "narration": "description",
            "particulars": "description",
            "withdrawal": "debit",
            "withdrawal amt": "debit",
            "deposit": "credit",
            "deposit amt": "credit",
            "closing balance": "balance"
        }

        df = df.rename(columns=aliases)

        if not all(col in df.columns for col in COLUMNS):
            raise ValueError(
                f"Sheet '{sheet_name}' has unsupported columns: "
                f"{list(df.columns)}"
            )

        df = df[COLUMNS].copy()

        for col in ["debit", "credit", "balance"]:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(
                    ",", "", regex=False
                ),
                errors="coerce"
            )

        transactions.extend(
            df.to_dict(orient="records")
        )

    return pd.DataFrame(transactions, columns=COLUMNS)


def extract_pdf_transactions(uploaded_file):
    pdf = fitz.open(
        stream=uploaded_file.getvalue(),
        filetype="pdf"
    )

    text = "\n".join(
        page.get_text(sort=True)
        for page in pdf
    )

    pdf.close()

    if not text.strip():
        raise ValueError(
            "No selectable PDF text found. "
            "Scanned PDF OCR is not yet implemented."
        )

    prompt = f"""
    Extract bank transactions from the following statement.

    Return only valid JSON containing a list of transactions.

    Required structure:
    {{
      "transactions": [
        {{
          "date": "YYYY-MM-DD",
          "description": "Transaction description",
          "debit": 0,
          "credit": 0,
          "balance": 0
        }}
      ]
    }}

    Rules:
    - Extract only actual transaction rows.
    - Do not invent transactions or amounts.
    - Use null for missing values.
    - Keep debit and credit in separate fields.
    - Preserve the original transaction order.
    - Exclude headings and summary totals.
    - Return JSON only.

    Statement:
    {text}
    """

    response = client.chat(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        format="json"
    )

    data = json.loads(response.message.content)

    if not isinstance(data, dict):
        raise ValueError("Unexpected AI response format.")

    transactions = data.get("transactions")

    if not isinstance(transactions, list):
        raise ValueError(
            "AI response does not contain a transaction list."
        )

    df = pd.DataFrame(transactions)

    if df.empty:
        return pd.DataFrame(columns=COLUMNS)

    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    df = df[COLUMNS]

    for col in ["debit", "credit", "balance"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df
