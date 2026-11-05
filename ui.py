import os
import subprocess
import sys

from import_rules import import_rule_controller
from import_rules.import_rule import ImportRule
from transactions import transaction_controller

# ==================== Public Methods ====================


def main_loop():
    _clear_screen()
    print("\nWelcome to Rule Forge")
    print("(1) Manage your transactions")
    print("(2) Manage your import rules")
    print("(3) Exit")

    choice = input("\nSelect an option: ")

    match choice[:1]:
        case "1":
            _clear_screen()
            _manage_transactions()
        case "2":
            _clear_screen()
            _manage_import_rules()
        case "3":
            sys.exit()
        case _:
            _invalid_choice(choice)

    _press_enter_to_continue()
    main_loop()


# ==================== Transaction Methods ====================


def _manage_transactions():
    print("What would you like to do?")
    print("(1) Import transactions")
    print("(2) Get all transactions")
    print("(3) Delete all transactions")
    print("(4) Return home")

    choice = input("\nSelect an option: ")

    match choice[:1]:
        case "1":
            _clear_screen()
            _import_transactions()
        case "2":
            _clear_screen()
            _get_transactions()
        case "3":
            _clear_screen()
            _delete_transactions()
        case "4":
            main_loop()
        case _:
            _invalid_choice(choice)


def _import_transactions():
    try:
        file_path = input("What file would you like to import? ")
        count = transaction_controller.import_transactions(file_path.strip().strip('"'))

        print(f"{count} transactions imported")
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)


def _get_transactions():
    transactions = transaction_controller.get_transactions()
    _print_entries_as_csv(transactions, "transactions")


def _delete_transactions():
    count = transaction_controller.delete_transactions()

    if count == 0:
        print("No transactions to delete")
        return

    print("(1) Delete all transactions")
    print("(2) Cancel")

    choice = input("\nSelect an option: ")

    if choice[:1] != "1":
        return

    _clear_screen()

    print(f"{count} transactions deleted")


# ==================== Import Rules Methods ====================


def _manage_import_rules():
    print("Import rules automatically customize transactions upon being imported\n")
    print("What would you like to do?")
    print("(1) Insert an import rule")
    print("(2) Get all import rules")
    print("(3) Delete an import rule")
    print("(4) Return home")

    choice = input("\nSelect an option: ")

    match choice[:1]:
        case "1":
            _clear_screen()
            _insert_import_rule()
        case "2":
            _clear_screen()
            _get_import_rules()
        case "3":
            _clear_screen()
            _delete_import_rule_by_id()
        case "4":
            main_loop()
        case _:
            _invalid_choice(choice)


def _insert_import_rule():
    print("Table columns:\nDate (YYYY-MM-DD), Account, Description, Category, Amount, and Excluded (true or false)\n")  # fmt: skip
    print("Example:\nIf 'Description' contains 'Walmart' then set 'Category' to 'Groceries'\n")  # fmt: skip

    input_variable = input("What table column should trigger this rule? ")
    input_value = input("What does the table column contain? ")

    output_variable = input("What table column should change? ")
    output_value = input("What should the table column contain? ")

    import_rule = ImportRule(input_variable, input_value, output_variable, output_value)
    success = import_rule_controller.insert_import_rule(import_rule)

    _clear_screen()

    # Remove Id since it currently displays as -1
    import_rule_str = str(import_rule).removeprefix("Id: -1 | ")

    if success:
        print(f"Import rule inserted:\n{import_rule_str}")
    else:
        print(f"Invalid import rule:\n{import_rule_str}")


def _get_import_rules() -> int:
    import_rules = import_rule_controller.get_import_rules()

    if len(import_rules) == 0:
        print("No import rules exist")
        return 0

    result = "\n".join(str(import_rule) for import_rule in import_rules)
    print(result)
    return len(import_rules)


def _delete_import_rule_by_id():
    count = _get_import_rules()

    if count == 0:
        return

    import_rule_id = input("\nEnter the id of the import rule you want to delete: ")
    deleted = import_rule_controller.delete_import_rule_by_id(import_rule_id)

    if deleted:
        print(f"\nImport rule '{import_rule_id}' deleted successfully")
    else:
        print(f"\nImport rule '{import_rule_id}' does not exist")


# ==================== Helper Methods ====================


def _clear_screen():
    command = "cls" if os.name == "nt" else "clear"
    subprocess.run(command, check=False, shell=True)


def _invalid_choice(choice: str):
    print(f"{choice} is an invalid choice")


def _print_entries_as_csv(entries: list, entry_name: str):
    if len(entries) == 0:
        print(f"No {entry_name} exist")
        return

    headers = list(vars(entries[0]).keys())
    headers.remove("id")

    headers_string = ", ".join(headers)
    print(headers_string.title())

    values = "\n".join(str(entry) for entry in entries)
    print(values)


def _press_enter_to_continue():
    input("\nPress [Enter] to Continue...")
