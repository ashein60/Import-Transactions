import sqlite3

from enums import MiscFields

db_path = MiscFields.DATA_BASE.value


def init_all_dbs():
    init_transactions_db()
    init_import_rules_db()


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


def init_import_rules_db():
    with sqlite3.connect(db_path) as connection:
        query = """
                    CREATE TABLE IF NOT EXISTS import_rules (
                        id INTEGER PRIMARY KEY,
                        input_variable TEXT NOT NULL,
                        input_value TEXT NOT NULL,
                        output_variable TEXT NOT NULL,
                        output_value TEXT NOT NULL
                    )
                """

        connection.execute(query)
