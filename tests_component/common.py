import sqlite3

import database_handler
from enums import MiscFields


def init_db(tmp_path):
    database_handler.db_path = tmp_path / MiscFields.DATA_BASE.value
    database_handler.init_all_dbs()

    with sqlite3.connect(database_handler.db_path) as connection:
        connection.execute("DELETE FROM import_rules")
        connection.execute("DELETE FROM transactions")
