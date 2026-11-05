import pytest

from enums import TransactionFields
from import_rules import import_rule_controller
from import_rules.import_rule import ImportRule
from tests_component import common
from transactions import transaction_controller
from transactions.transaction import Transaction

DATA_PATH = "tests_component/transactions/data/"
ACCOUNT_CSV = "account.csv"
CREDIT_CARD_CSV = "credit_card.csv"
EMPTY_CSV = "empty.csv"

# ==================== import_transactions Tests ====================


def test_import_transaction_import_invalid_file_path(tmp_path):
    common.init_db(tmp_path)

    with pytest.raises(FileNotFoundError):
        transaction_controller.import_transactions(ACCOUNT_CSV)


def test_import_transaction_import_invalid_file_data(tmp_path):
    common.init_db(tmp_path)

    with pytest.raises(ValueError):
        transaction_controller.import_transactions(DATA_PATH + EMPTY_CSV)


def test_import_transaction_import_from_account(tmp_path):
    common.init_db(tmp_path)

    count = transaction_controller.import_transactions(DATA_PATH + ACCOUNT_CSV)
    assert count == 2


def test_import_transaction_import_from_credit_card(tmp_path):
    common.init_db(tmp_path)

    count = transaction_controller.import_transactions(DATA_PATH + CREDIT_CARD_CSV)
    assert count == 2


def test_import_transaction_import_with_import_rules_str(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.CATEGORY.value, "Groceries")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    count = transaction_controller.import_transactions(DATA_PATH + CREDIT_CARD_CSV)
    transactions = transaction_controller.get_transactions()

    assert any(transaction.category == "Groceries" for transaction in transactions)

    assert count == 2


def test_import_transaction_import_with_import_rules_decimal(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.AMOUNT.value, "10.14")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    count = transaction_controller.import_transactions(DATA_PATH + CREDIT_CARD_CSV)
    transactions = transaction_controller.get_transactions()

    assert any(str(transaction.amount) == "10.14" for transaction in transactions)

    assert count == 2


def test_import_transaction_import_with_import_rules_bool(tmp_path):
    common.init_db(tmp_path)

    import_rule = ImportRule(TransactionFields.DESCRIPTION.value, "Kroger", TransactionFields.EXCLUDED.value, "False")  # fmt: skip
    import_rule_controller.insert_import_rule(import_rule)

    count = transaction_controller.import_transactions(DATA_PATH + CREDIT_CARD_CSV)
    transactions = transaction_controller.get_transactions()

    assert any(str(transaction.excluded) == "False" for transaction in transactions)

    assert count == 2


# ==================== get_transactions Tests ====================


def test_get_transactions_Empty(tmp_path):
    common.init_db(tmp_path)

    transactions = transaction_controller.get_transactions()
    assert len(transactions) == 0


def test_get_transactions_account_correct_data(tmp_path):
    common.init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + ACCOUNT_CSV)
    transactions = transaction_controller.get_transactions()

    assert transactions[0].id == 1
    assert transactions[1].id == 2

    assert str(transactions[0].date) == "2026-10-11"

    assert str(transactions[0].amount) == "-13.37"
    assert str(transactions[1].amount) == "65"

    assert transactions[0].excluded == False


def test_get_transactions_credit_card_correct_data(tmp_path):
    common.init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + CREDIT_CARD_CSV)
    transactions = transaction_controller.get_transactions()

    assert transactions[0].id == 1
    assert transactions[1].id == 2

    assert str(transactions[0].amount) == "-44.31"
    assert str(transactions[1].amount) == "1073.98"

    assert transactions[0].excluded == False


# ==================== delete_transactions Tests ====================


def test_delete_transactions_Empty(tmp_path):
    common.init_db(tmp_path)

    count = transaction_controller.delete_transactions()
    assert count == 0


def test_delete_transactions_same_as_import(tmp_path):
    common.init_db(tmp_path)

    import_count = transaction_controller.import_transactions(DATA_PATH + ACCOUNT_CSV)
    delete_count = transaction_controller.delete_transactions()

    transactions = transaction_controller.get_transactions()

    assert import_count == delete_count
    assert len(transactions) == 0


# ==================== replace_transaction_by_id Tests ====================


def test_replace_transaction_by_id_with_empty_transactions(tmp_path):
    common.init_db(tmp_path)

    transaction = Transaction(
        -1, "2026-10-01", "1234", "Kroger", "groceries", 10, False
    )
    transaction_controller.replace_transaction_by_id(1, transaction)


def test_replace_transaction_by_invalid_id(tmp_path):
    common.init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + CREDIT_CARD_CSV)
    transactions = transaction_controller.get_transactions()

    transactions[0].description = "Foo"
    success = transaction_controller.replace_transaction_by_id(5, transactions[0])

    assert not success


def test_replace_transaction_by_valid_id(tmp_path):
    common.init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + CREDIT_CARD_CSV)
    transactions = transaction_controller.get_transactions()

    transactions[0].description = "Foo"
    success = transaction_controller.replace_transaction_by_id(1, transactions[0])

    updated_transactions = transaction_controller.get_transactions()

    assert updated_transactions[0].description == "Foo"
    assert success
