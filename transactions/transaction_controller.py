import csv
import sqlite3
from pathlib import Path

from database_handler import db_path
from enums import CapitalOneAccountFields
from transactions.transaction import Transaction

# ==================== Public Methods ====================


def import_transactions(file_path):
    if not Path(file_path).is_file():
        pass  # FileNotFoundError

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            pass  # Empty or missing CSV headers

        if CapitalOneAccountFields.ACCOUNT_NUMBER.value in reader.fieldnames:
            transaction_factory = Transaction.from_capital_one_account
        else:
            transaction_factory = Transaction.from_capital_one_credit_card

        for row in reader:
            transaction = transaction_factory(row)
            _insert_transaction(transaction)


def get_transactions():
    pass


def delete_transactions():
    pass


# ==================== Private Methods ====================


def _insert_transaction(transaction):
    with sqlite3.connect(db_path) as connection:
        query = "INSERT INTO transactions(date, account, description, category, amount, excluded) values (?, ?, ?, ?, ?, ?)"
        connection.execute(query, transaction.params)
