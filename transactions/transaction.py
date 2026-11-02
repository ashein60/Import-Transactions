from dataclasses import dataclass
from datetime import date as datetime
from decimal import Decimal

from enums import CapitalOneAccountFields, CapitalOneCreditCardFields, TransactionFields


@dataclass
class Transaction:
    id: int = -1
    date: datetime
    account: str
    description: str
    category: str
    amount: Decimal
    excluded: bool = False


@classmethod
def from_sql_row(cls, row):
    return cls(
        id=row[TransactionFields.ID.value],
        date=row[TransactionFields.DATE.value],
        account=row[TransactionFields.ACCOUNT.value],
        description=row[TransactionFields.DESCRIPTION.value],
        category=row[TransactionFields.CATEGORY.value],
        amount=row[TransactionFields.AMOUNT.value],
        excluded=row[TransactionFields.EXCLUDED.value],
    )


@classmethod
def from_capital_one_account(cls, row):
    date_unformatted = [CapitalOneAccountFields.TRANSACTION_DATE.value]
    date_formatted = datetime.strptime(date_unformatted, "%m/%d/%y").strftime("%Y-%m-%d")  # fmt: skip

    transaction_type = row[CapitalOneAccountFields.TRANSACTION_TYPE.value]
    amount_multiplier = 1 if transaction_type == "Debit" else -1

    return cls(
        date=date_formatted,
        account=row[CapitalOneAccountFields.ACCOUNT_NUMBER.value],
        description=row[CapitalOneAccountFields.TRANSACTION_DESCRIPTION.value],
        category="",  # Will be defined by import rules
        amount=Decimal(row[CapitalOneAccountFields.TRANSACTION_AMOUNT.value])
        * amount_multiplier,
    )


@classmethod
def from_capital_one_credit_card(cls, row):
    debit = Decimal(row[CapitalOneCreditCardFields.DEBIT.value]) or 0
    credit = Decimal(row[CapitalOneCreditCardFields.CREDIT.value]) or 0

    amount = -debit if debit != 0 else credit

    return cls(
        date=row[CapitalOneCreditCardFields.POSTED_DATE.value],
        account=row[CapitalOneCreditCardFields.CARD_NUMBER.value],
        description=row[CapitalOneCreditCardFields.DESCRIPTION.value],
        category=row[CapitalOneCreditCardFields.CATEGORY.value],
        amount=amount,
    )
