import sqlite3
from datetime import datetime
from decimal import InvalidOperation

import database_handler
from enums import TRANSACTION_ATTRIBUTE_TYPES, TransactionFields
from import_rules.import_rule import ImportRule

# ==================== Public Methods ====================


def insert_import_rule(import_rule: ImportRule) -> bool:
    if not _has_valid_import_variables(import_rule) or not _has_valid_import_values(import_rule):  # fmt: skip
        return False

    with sqlite3.connect(database_handler.db_path) as connection:
        query = "INSERT INTO IMPORT_RULES (input_variable, input_value, output_variable, output_value) values (?, ?, ?, ?)"
        connection.execute(query, import_rule.params)

    return True


def get_import_rules() -> list[ImportRule]:
    with sqlite3.connect(database_handler.db_path) as connection:
        connection.row_factory = sqlite3.Row  # Allows csv style row format
        rows = connection.execute("SELECT * FROM import_rules").fetchall()

        import_rules = _convert_rows_to_import_rules(rows)

        return import_rules


def delete_import_rule_by_id(rule_id: int) -> bool:
    with sqlite3.connect(database_handler.db_path) as connection:
        query = "DELETE FROM import_rules WHERE id = ?"
        cursor = connection.execute(query, (rule_id,))

        return cursor.rowcount == 1


# ==================== Private Methods ====================


def _has_valid_import_variables(import_rule: ImportRule) -> bool:
    is_input_in_fields = import_rule.input_variable in TransactionFields
    is_output_in_fields = import_rule.output_variable in TransactionFields

    is_input_id = import_rule.input_variable == TransactionFields.ID.value
    is_output_id = import_rule.output_variable == TransactionFields.ID.value

    return (
        is_input_in_fields
        and is_output_in_fields
        and not is_input_id
        and not is_output_id
    )


def _has_valid_import_values(import_rule: ImportRule) -> bool:
    is_valid_input = _is_valid_value_for_transaction_variable(import_rule.input_variable, import_rule.input_value)  # fmt: skip
    is_valid_output = _is_valid_value_for_transaction_variable(import_rule.output_variable, import_rule.output_value)  # fmt: skip

    return is_valid_input and is_valid_output


def _is_valid_value_for_transaction_variable(variable: str, value: str) -> bool:
    """Ex: variable = 'amount' and value = '10.32'"""
    variable_input_type = TRANSACTION_ATTRIBUTE_TYPES[variable]

    try:
        if variable_input_type == datetime:
            datetime.strptime(value, "%Y-%m-%d")
        elif variable_input_type == bool:
            if value != "True" and value != "False":
                return False
        else:
            variable_input_type(value)
    except (ValueError, TypeError, InvalidOperation):
        return False

    return True


def _convert_rows_to_import_rules(rows: list) -> list[ImportRule]:
    import_rules = []

    for row in rows:
        import_rule = ImportRule.from_sql_row(row)
        import_rules.append(import_rule)

    return import_rules
