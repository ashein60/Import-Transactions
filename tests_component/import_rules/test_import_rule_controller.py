from enums import TransactionFields
from import_rules import import_rule_controller
from import_rules.import_rule import ImportRule
from tests_component import common
from transactions import transaction_controller

DATA_PATH = "tests_component/import_rules/data/"
TRANSACTIONS_CSV = "transactions.csv"

# ==================== insert_import_rule Tests ====================


def test_insert_import_rule_id_variable_fail(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.ID.value, "1", TransactionFields.ACCOUNT.value, "4")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_invalid_variable(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule("Foo", "1", TransactionFields.ACCOUNT.value, "4")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_valid_variable_and_string_values(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert success


def test_insert_import_rule_invalid_date_value(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.DATE.value, "10-2026-11")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_valid_date_value(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.DATE.value, "2026-10-11")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert success


def test_insert_import_rule_invalid_amount_value(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.AMOUNT.value, "a10.11a")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_valid_amount_value(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.AMOUNT.value, "10.11")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert success


def test_insert_import_rule_valid_amount_value_dollar_sign(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.AMOUNT.value, "$10.11")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert success


def test_insert_import_rule_invalid_excluded_value(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.EXCLUDED.value, "foo")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert not success


def test_insert_import_rule_valid_excluded_value(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.EXCLUDED.value, "True")  # fmt: skip
    success = import_rule_controller.insert_import_rule(import_rule)

    assert success


def test_insert_import_rule_with_affected_transactions(tmp_path):
    common.init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + TRANSACTIONS_CSV)
    transaction_controller.get_transactions()

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.EXCLUDED.value, "TruE")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    transactions = transaction_controller.get_transactions()

    assert transactions[0].excluded == True


def test_insert_import_rule_with_unaffected_transactions(tmp_path):
    common.init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + TRANSACTIONS_CSV)
    before_transactions = transaction_controller.get_transactions()

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "foo", TransactionFields.EXCLUDED.value, "trUe")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    after_transactions = transaction_controller.get_transactions()

    assert before_transactions == after_transactions


# ==================== get_import_rules Tests ====================


def test_get_import_rules_empty(tmp_path):
    common.init_db(tmp_path)

    import_rules = import_rule_controller.get_import_rules()

    assert len(import_rules) == 0


def test_get_import_rules_with_data(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    import_rules = import_rule_controller.get_import_rules()

    assert len(import_rules) == 1


# ==================== delete_import_rule_by_id Tests ====================


def test_delete_import_rule_by_id_empty(tmp_path):
    common.init_db(tmp_path)

    deleted = import_rule_controller.delete_import_rule_by_id(1)

    assert not deleted


def test_delete_import_rule_by_id_doesnt_exist(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    deleted = import_rule_controller.delete_import_rule_by_id(2)

    assert not deleted


def test_delete_import_rule_by_valid_id(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    deleted = import_rule_controller.delete_import_rule_by_id(1)
    import_rules = import_rule_controller.get_import_rules()

    assert deleted
    assert len(import_rules) == 0


# ==================== apply_rules_to_transaction Tests ====================


def test_apply_rules_to_transactions_empty_import_rules(tmp_path):
    common.init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + TRANSACTIONS_CSV)
    transactions = transaction_controller.get_transactions()

    _apply_rules_to_transactions(transactions)

    # Checking the code runs without errors


def test_apply_rules_to_transactions_description_contains_value(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    transaction_controller.import_transactions(DATA_PATH + TRANSACTIONS_CSV)
    transactions = transaction_controller.get_transactions()

    _apply_rules_to_transactions(transactions)

    assert any(transaction.category == "Groceries" for transaction in transactions)


def test_apply_rules_to_transactions_update_excluded(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "MOBILE PYMT", TransactionFields.EXCLUDED.value, "True")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    transaction_controller.import_transactions(DATA_PATH + TRANSACTIONS_CSV)
    transactions = transaction_controller.get_transactions()

    _apply_rules_to_transactions(transactions)

    assert any(transaction.excluded == "True" for transaction in transactions)


def test_apply_rules_to_transactions_update_same_variable(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.ACCOUNT.value, "2815", TransactionFields.ACCOUNT.value, "CC")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    transaction_controller.import_transactions(DATA_PATH + TRANSACTIONS_CSV)
    transactions = transaction_controller.get_transactions()

    _apply_rules_to_transactions(transactions)

    assert any(transaction.account == "CC" for transaction in transactions)


def test_apply_rules_to_transactions_with_two_rules(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.ACCOUNT.value, "2815", TransactionFields.ACCOUNT.value, "CC")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "MOBILE PYMT", TransactionFields.EXCLUDED.value, "True")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    transaction_controller.import_transactions(DATA_PATH + TRANSACTIONS_CSV)
    transactions = transaction_controller.get_transactions()

    _apply_rules_to_transactions(transactions)

    assert any(transaction.account == "CC" for transaction in transactions)
    assert any(transaction.excluded == "True" for transaction in transactions)


# ==================== Helper Methods ====================


def _apply_rules_to_transactions(transactions):
    for transaction in transactions:
        import_rule_controller.apply_rules_to_transaction(transaction)  # fmt: skip
