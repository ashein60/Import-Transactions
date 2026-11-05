import csv
import sqlite3
from pathlib import Path

import database_handler
from enums import CapitalOneAccountFields
from import_rules import import_rule_controller
from transactions.transaction import Transaction

# ==================== Public Methods ====================


def import_transactions(file_path) -> int:
    if not Path(file_path).is_file():
        raise FileNotFoundError(f"File {file_path} not found")

    with open(file_path, "r", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Invalid CSV file")

        transactions = get_transactions()

        if CapitalOneAccountFields.ACCOUNT_NUMBER.value in reader.fieldnames:
            transaction_factory = Transaction.from_capital_one_account
        else:
            transaction_factory = Transaction.from_capital_one_credit_card

        count = 0

        for row in reader:
            transaction = transaction_factory(row)

            if transaction not in transactions:
                import_rule_controller.apply_rules_to_transaction(transaction)
                _insert_transaction(transaction)
                count += 1

    return count


def get_transactions() -> list[Transaction]:
    with sqlite3.connect(database_handler.db_path) as connection:
        connection.row_factory = sqlite3.Row  # Allows csv style row format
        rows = connection.execute("SELECT * FROM transactions").fetchall()

        transactions = _convert_rows_to_transactions(rows)

        return transactions


def delete_transactions() -> int:
    with sqlite3.connect(database_handler.db_path) as connection:
        cursor = connection.execute("DELETE FROM transactions")
        return cursor.rowcount


def replace_transaction_by_id(transaction_id: int, transaction: Transaction) -> bool:
    with sqlite3.connect(database_handler.db_path) as connection:
        query = "UPDATE transactions SET date = ?, account = ?, description = ?, category = ?, amount = ?, excluded = ? WHERE id = ?"
        cursor = connection.execute(query, (*transaction.params, transaction_id))

        return cursor.rowcount == 1


# ==================== Private Methods ====================


def _insert_transaction(transaction):
    with sqlite3.connect(database_handler.db_path) as connection:
        query = "INSERT INTO transactions (date, account, description, category, amount, excluded) values (?, ?, ?, ?, ?, ?)"
        connection.execute(query, transaction.params)


def _convert_rows_to_transactions(rows: list) -> list[Transaction]:
    transactions = []

    for row in rows:
        transaction = Transaction.from_sql_row(row)
        transactions.append(transaction)

    return transactions
