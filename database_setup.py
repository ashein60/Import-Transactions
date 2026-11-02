import sqlite3

from enums import MiscFields, TransactionFields


def init_all_dbs(path=MiscFields.DATA_BASE.value):
    init_transactions_db(path)


def init_transactions_db(path=MiscFields.DATA_BASE.value):
    with sqlite3.connect(path) as connection:
        query = f"""
                    CREATE TABLE IF NOT EXISTS {TransactionFields.TRANSACTIONS_DB.value} (
                        id INTEGER PRIMARY KEY,
                        date TEXT NOT NULL,
                        account TEXT NOT NULL,
                        description TEXT NOT NULL,
                        category TEXT NOT NULL,
                        amount TEXT NOT NULL,
                        excluded BOOLEAN NOT NULL DEFAULT FALSE
                    )
                """

        connection.execute(query)
