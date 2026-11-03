import sqlite3

from enums import MiscFields

db_path = MiscFields.DATA_BASE.value


def init_all_dbs():
    init_transactions_db()


def init_transactions_db():
    with sqlite3.connect(db_path) as connection:
        query = """
                    CREATE TABLE IF NOT EXISTS transactions (
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
