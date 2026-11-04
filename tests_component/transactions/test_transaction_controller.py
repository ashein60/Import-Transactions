import pytest

import database_handler
from enums import MiscFields
from transactions import transaction_controller

DATA_PATH = "tests_component/transactions/data/"
ACCOUNT_CSV = "account.csv"
CREDIT_CARD_CSV = "credit_card.csv"
EMPTY_CSV = "empty.csv"

# ==================== import_transactions Methods ====================


def test_import_transaction_import_invalid_file_path(tmp_path):
    _init_db(tmp_path)

    with pytest.raises(FileNotFoundError):
        transaction_controller.import_transactions(ACCOUNT_CSV)


def test_import_transaction_import_invalid_file_data(tmp_path):
    _init_db(tmp_path)

    with pytest.raises(ValueError):
        transaction_controller.import_transactions(DATA_PATH + EMPTY_CSV)


def test_import_transaction_import_from_account(tmp_path):
    _init_db(tmp_path)

    count = transaction_controller.import_transactions(DATA_PATH + ACCOUNT_CSV)
    assert count == 2


def test_import_transaction_import_from_credit_card(tmp_path):
    _init_db(tmp_path)

    count = transaction_controller.import_transactions(DATA_PATH + CREDIT_CARD_CSV)
    assert count == 2


def test_import_transaction_duplicates(tmp_path):
    _init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + ACCOUNT_CSV)
    count = transaction_controller.import_transactions(DATA_PATH + ACCOUNT_CSV)

    assert count == 0


# ==================== get_transactions Methods ====================


def test_get_transactions_Empty(tmp_path):
    _init_db(tmp_path)

    transactions = transaction_controller.get_transactions()
    assert len(transactions) == 0


def test_get_transactions_account_correct_data(tmp_path):
    _init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + ACCOUNT_CSV)
    transactions = transaction_controller.get_transactions()

    assert transactions[0].id == 1
    assert transactions[1].id == 2

    assert str(transactions[0].date) == "2026-10-11"

    assert str(transactions[0].amount) == "-13.37"
    assert str(transactions[1].amount) == "65"

    assert transactions[0].excluded == False


def test_get_transactions_credit_card_correct_data(tmp_path):
    _init_db(tmp_path)

    transaction_controller.import_transactions(DATA_PATH + CREDIT_CARD_CSV)
    transactions = transaction_controller.get_transactions()

    assert transactions[0].id == 1
    assert transactions[1].id == 2

    assert str(transactions[0].amount) == "-44.31"
    assert str(transactions[1].amount) == "1073.98"

    assert transactions[0].excluded == False


# ==================== delete_transactions Methods ====================


def test_delete_transactions_Empty(tmp_path):
    _init_db(tmp_path)

    count = transaction_controller.delete_transactions()
    assert count == 0


def test_delete_transactions_same_as_import(tmp_path):
    _init_db(tmp_path)

    import_count = transaction_controller.import_transactions(DATA_PATH + ACCOUNT_CSV)
    delete_count = transaction_controller.delete_transactions()

    assert import_count == delete_count


# ==================== Helper Methods ====================


def _init_db(tmp_path):
    database_handler.db_path = tmp_path / MiscFields.DATA_BASE.value
    database_handler.init_transactions_db()
    transaction_controller.delete_transactions()
