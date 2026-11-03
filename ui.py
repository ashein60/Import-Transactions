import os
import subprocess

from transactions import transaction_controller

# ==================== Public Methods ====================


def main_loop():
    _clear_screen()

    print("Welcome to Transaction Hub")
    print("(1) Manage your transactions")
    print("(2) Manage your import rules")

    choice = input("\nSelect an option: ")

    match choice[:1]:
        case "1":
            _clear_screen()
            _manage_transactions()
        case _:
            _invalid_choice(choice)


# ==================== Transaction Methods ====================


def _manage_transactions():
    print("What would you like to do?")
    print("(1) Import transactions")
    print("(2) Get transactions")
    print("(3) Delete transactions")

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

    if count > 0:
        print(f"{count} transactions deleted")
    else:
        print("No transactions to delete")


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

    headers = vars(entries[0]).keys()
    headers_string = ",".join(headers)
    print(headers_string)

    values = "\n".join(str(entry) for entry in entries)
    print(values)
