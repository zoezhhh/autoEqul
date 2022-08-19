INPUT_FIELD = "input field"
DROPDOWN_LIST = "drop-down list"
CHECKBOX = "checkbox"

Tags = {
    "Coverage": 0,
    "Deposit/Tax Handling": 1,
    "Riders": 2,
}

InputMapping = [
    {
        "Excel colname": "UL Face Amount",
        "Novinsoft Field": {
            "tag": "Coverage",
            "field": "Face Amount",
            "type": INPUT_FIELD,
            "#tab": 6
        }
    },
    {
        "Excel colname": "Gender",
        "Novinsoft Field": {
            "tag": "Coverage",
            "field": "Sex",
            "type": DROPDOWN_LIST,
            "#tab": 8
        }
    },
    {
        "Excel colname": "Age",
        "Novinsoft Field": {
            "tag": "Coverage",
            "field": "Age",
            "type": INPUT_FIELD,
            "#tab": 10
        }
    },
    {
        "Excel colname": "Smoking Status",
        "Novinsoft Field": {
            "tag": "Coverage",
            "field": "Smoking Status",
            "type": DROPDOWN_LIST,
            "#tab": 11
        }
    },
    {
        "Excel colname": "Term Face Amount",
        "Novinsoft Field": {
            "tag": "Riders",
            "field": "20 YRCT",
            "type": CHECKBOX,
            "#tab": 9
        },
        "Folded Fields": [
            {
                "Excel colname": "Term Face Amount",
                "Novinsoft Field": {
                    "tag": "Riders",
                    "field": "Amount",
                    "type": INPUT_FIELD,
                    "#tab": 10
                }
            },
            {
                "Excel colname": "Term To Age",
                "Novinsoft Field": {
                    "tag": "Riders",
                    "field": "To Age",
                    "type": INPUT_FIELD,
                    "#tab": 11
                }
            }
        ]
    },
    {
        "Excel colname": "Deposit To Age",
        "Novinsoft Field": {
            "tag": "Deposit/Tax Handling",
            "field": "Duration",
            "type": INPUT_FIELD,
            "#tab": 6
        }
    },
    {
        "Excel colname": "Monthly Deposit Amount",
        "Novinsoft Field": {
            "tag": "Deposit/Tax Handling",
            "field": "Amount",
            "type": INPUT_FIELD,
            "#tab": 4
        }
    }
]

input_cols = []


def get_cols(mappings):
    for m in mappings:
        input_cols.append(m["Excel colname"])
        if "Folded Fields" in m:
            get_cols(m["Folded Fields"])


get_cols(InputMapping)
input_cols = list(set(input_cols))
