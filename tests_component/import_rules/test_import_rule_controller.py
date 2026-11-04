import sqlite3

import database_handler
from enums import MiscFields, TransactionFields
from import_rules import import_rule_controller
from import_rules.import_rule import ImportRule

# ==================== insert_import_rule Methods ====================


def test_insert_import_rule_id_variable_fail(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.ID.value, "1", TransactionFields.ACCOUNT.value, "4")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_invalid_variable(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule("Foo", "1", TransactionFields.ACCOUNT.value, "4")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_valid_variable_and_string_values(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert success


def test_insert_import_rule_invalid_date_value(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.DATE.value, "10-2026-11")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_valid_date_value(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.DATE.value, "2026-10-11")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert success


def test_insert_import_rule_invalid_amount_value(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.AMOUNT.value, "a10.11a")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_valid_amount_value(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.AMOUNT.value, "10.11")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert success


def test_insert_import_rule_invalid_excluded_value(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.EXCLUDED.value, "foo")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_valid_excluded_value(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.EXCLUDED.value, "False")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert success


# ==================== get_import_rules Methods ====================


def test_get_import_rules_empty(tmp_path):
    _init_db(tmp_path)

    import_rules = import_rule_controller.get_import_rules()

    assert len(import_rules) == 0


def test_get_import_rules_with_data(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    import_rules = import_rule_controller.get_import_rules()

    assert len(import_rules) == 1


# ==================== delete_import_rule_by_id Methods ====================


def test_delete_import_rule_by_id_empty(tmp_path):
    _init_db(tmp_path)

    deleted = import_rule_controller.delete_import_rule_by_id(1)

    assert not deleted


def test_delete_import_rule_by_id_doesnt_exist(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    deleted = import_rule_controller.delete_import_rule_by_id(2)

    assert not deleted


def test_delete_import_rule_by_valid_id(tmp_path):
    _init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    deleted = import_rule_controller.delete_import_rule_by_id(1)
    import_rules = import_rule_controller.get_import_rules()

    assert deleted
    assert len(import_rules) == 0


# ==================== Helper Methods ====================


def _init_db(tmp_path):
    database_handler.db_path = tmp_path / MiscFields.DATA_BASE.value
    database_handler.init_import_rules_db()

    with sqlite3.connect(database_handler.db_path) as connection:
        connection.execute("DELETE FROM import_rules")
