from enums import TransactionFields
from import_rules import import_rule_controller
from import_rules.import_rule import ImportRule
from transactions.transaction import Transaction


def test_apply_rule_to_transaction_false():
    transaction = Transaction(1, "2026-10-11", "fooAccount", "fooDescription", "fooCategory", 10.12, False)  # fmt: skip
    import_rule = ImportRule("fooInputVariable", "fooInputValue", "fooOutputVariable", "fooOutputValue")  # fmt: skip

    success = import_rule_controller._apply_rule_to_transaction(import_rule, transaction)  # fmt: skip

    assert not success


def test_apply_rule_to_transaction_true():
    transaction = Transaction(1, "2026-10-11", "fooAccount", "fooDescription", "fooCategory", 10.12, False)  # fmt: skip
    import_rule = ImportRule(TransactionFields.ACCOUNT.value, "foo", TransactionFields.CATEGORY.value, "realCategory")  # fmt: skip

    success = import_rule_controller._apply_rule_to_transaction(import_rule, transaction)  # fmt: skip

    assert success
