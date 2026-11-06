from dataclasses import dataclass
from datetime import date as datetime
from decimal import Decimal

from enums import CapitalOneAccountFields, CapitalOneCreditCardFields, TransactionFields


@dataclass
class Transaction:
    id: int
    date: datetime
    account: str
    description: str
    category: str
    amount: Decimal
    excluded: bool = False

    @classmethod
    def from_sql_row(cls, row):
        excluded = row[TransactionFields.EXCLUDED.value] != 0

        return cls(
            id=row[TransactionFields.ID.value],
            date=row[TransactionFields.DATE.value],
            account=row[TransactionFields.ACCOUNT.value],
            description=row[TransactionFields.DESCRIPTION.value],
            category=row[TransactionFields.CATEGORY.value],
            amount=Decimal(row[TransactionFields.AMOUNT.value]),
            excluded=excluded,
        )

    @classmethod
    def from_capital_one_account(cls, row):
        date_unformatted = row[CapitalOneAccountFields.TRANSACTION_DATE.value]
        date_formatted = datetime.strptime(date_unformatted, "%m/%d/%y").strftime("%Y-%m-%d")  # fmt: skip

        transaction_type = row[CapitalOneAccountFields.TRANSACTION_TYPE.value]
        transaction_amount = Decimal(row[CapitalOneAccountFields.TRANSACTION_AMOUNT.value])  # fmt: skip
        amount_multiplier = -1 if transaction_type == "Debit" else 1

        return cls(
            id=None,
            date=date_formatted,
            account=row[CapitalOneAccountFields.ACCOUNT_NUMBER.value],
            description=row[CapitalOneAccountFields.TRANSACTION_DESCRIPTION.value],
            category="None",  # Will be defined by import rules
            amount=transaction_amount * amount_multiplier,
        )

    @classmethod
    def from_capital_one_credit_card(cls, row):
        debit = row[CapitalOneCreditCardFields.DEBIT.value] or 0
        credit = row[CapitalOneCreditCardFields.CREDIT.value] or 0

        amount = -Decimal(debit) if debit != 0 else Decimal(credit)

        return cls(
            id=None,
            date=row[CapitalOneCreditCardFields.POSTED_DATE.value],
            account=row[CapitalOneCreditCardFields.CARD_NUMBER.value],
            description=row[CapitalOneCreditCardFields.DESCRIPTION.value],
            category=row[CapitalOneCreditCardFields.CATEGORY.value],
            amount=amount,
        )

    @property
    def params(self):
        """Does not include id"""
        return (
            self.date,
            self.account,
            self.description,
            self.category,
            str(self.amount),
            self.excluded,
        )

    def __eq__(self, other):
        """Does not include id"""
        if not isinstance(other, Transaction):
            return NotImplemented

        return (
            self.date == other.date
            and self.account == other.account
            and self.description == other.description
            and self.category == other.category
            and str(self.amount) == str(other.amount)
            and str(self.excluded) == str(other.excluded)
        )

    def __str__(self):
        return f"{self.date}, {self.account}, {self.description}, {self.category}, {self.amount}, {self.excluded}"
