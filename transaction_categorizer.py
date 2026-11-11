
import re


CATEGORY_RULES = {
    "Salary": [
        "salary", "payroll", "monthly pay"
    ],
    "Rent": [
        "rent", "house rent", "lease"
    ],
    "Groceries": [
        "grocery", "supermarket", "vegetables",
        "bigbasket", "zepto", "blinkit"
    ],
    "Utilities": [
        "electricity", "water bill", "gas bill",
        "internet", "broadband", "mobile recharge"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra",
        "shopping", "retail"
    ],
    "Food & Dining": [
        "restaurant", "swiggy", "zomato",
        "cafe", "food"
    ],
    "Transport": [
        "uber", "ola", "petrol", "fuel",
        "metro", "irctc"
    ],
    "Healthcare": [
        "hospital", "pharmacy", "medical",
        "clinic", "medicine"
    ],
    "Transfers": [
        "neft", "imps", "rtgs", "upi transfer"
    ]
}


def categorize_transaction(description):

    if not isinstance(description, str):
        return "Other"

    text = description.lower()

    for category, keywords in CATEGORY_RULES.items():

        for keyword in keywords:

            if keyword in text:
                return category

    return "Other"


def categorize_transactions(df):

    df = df.copy()

    df["category"] = df["description"].apply(
        categorize_transaction
    )

    return df
