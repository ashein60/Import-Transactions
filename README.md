# Import-Transactions
Using bank csv files, create rules to customize or exclude bank transactions. This only works with Capital One checking and savings accounts and credit cards. I use Google sheets to manage a Summary table, but it's time consuming to manually re-assign transaction columns every month.

> [!Note]
> **If you'd like to include your bank csv files:**
> - **transaction.py** - Use from_capital_one_account and from_capital_one_credit_card as an example
> - **transaction_controller.py** - Under the import_transactions, adjust the transaction_factory definitions and if statement

# How To Use
- In a console or Command Prompt, go to the project path, then run: **python -m main**
  - Note: You can press the up arrow to select the most recent commands
- Import Transactions throughout the month
- Assign rules to customize the existing and future transactions
- Copy them over to a program such as google sheets that can manage a Summary
- At the end of the month or budget period, clear the transactions from the database

# Bank Transactions
- **Id** On rare cases, you might have two identical transactions on the same day, for example, ordering coffee twice
- **Date:** 11/01/2026
- **Account:** John Doe's CC - Instead of 1234, an alias can be used
- **Description:** Kroger
- **Category:** Groceries - Description is used to define this
- **Amount:** -$50.00 - No need for Debit and Credit
- **Excluded:** False - Sometimes it's unnecessary to track money when it's moved between accounts

# Import Rules (Examples)
- if account contains '1234' then set account to 'credit card'
- if description contains Kroger then set category to groceries
- if description contains transfer then set excluded to True

# Tech Stack
Python
Sqlite
Git

# Task Commands
- **Build:** python -m main build
- **Format Code:** python -m main spotlessApply
- **Combined:** python -m main build spotlessApply

# Run Tests
- **Run all Tests:** python -m pytest
- **Run all tests in a specific file:** python -m pytest test_path -v -s
- **Run a specific test method:** python -m pytest test_path::test_method -v -s
