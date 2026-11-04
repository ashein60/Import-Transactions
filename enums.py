from enum import Enum


class TransactionFields(Enum):
    ID = "id"
    DATE = "date"
    ACCOUNT = "account"
    DESCRIPTION = "description"
    CATEGORY = "category"
    AMOUNT = "amount"
    EXCLUDED = "excluded"


class CapitalOneAccountFields(Enum):
    ACCOUNT_NUMBER = "Account Number"
    TRANSACTION_DESCRIPTION = "Transaction Description"
    TRANSACTION_DATE = "Transaction Date"
    TRANSACTION_TYPE = "Transaction Type"
    TRANSACTION_AMOUNT = "Transaction Amount"


class CapitalOneCreditCardFields(Enum):
    POSTED_DATE = "Posted Date"
    CARD_NUMBER = "Card No."
    DESCRIPTION = "Description"
    CATEGORY = "Category"
    DEBIT = "Debit"
    CREDIT = "Credit"


class ImportRuleFields(Enum):
    ID = "id"
    INPUT_VARIABLE = "input_variable"
    INPUT_VALUE = "input_value"
    OUTPUT_VARIABLE = "output_variable"
    OUTPUT_VALUE = "output_value"


class MiscFields(Enum):
    DATA_BASE = "database.db"
