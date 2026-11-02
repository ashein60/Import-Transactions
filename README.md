# Import-Transactions
Using bank csv files, create rules to customize or exclude bank transactions. This should work with any bank csv file, since rules are used to map to table column headers. I use Google sheets to manage a Summary table, but it's time consuming to manually handle each transaction.

> [!IMPORTANT]
> This project is in progress. Not all features work yet.

# Intended Use
Each month, start by clearing transactions, then import them throughout the month. Transactions are stored to eliminate importing data that is already in the database.

# Bank Transactions
- **Id** On rare cases, you might have two identical transactions on the same day, for example, ordering coffee twice in one day
- **Date:** 11/01/2026
- **Account:** John Doe's CC - Instead of 1234, an alias can be used
- **Description:** Kroger
**- Category:** Groceries - Description is used to define this
**- Amount:** -$50.00 - No need for Debit and Credit
- **Excluded:** FALSE - Sometimes it's unnecessary to track money when it's moved between accounts

# Tech Stack
Python
Sqlite
Git

# Task Commands
- Build: python main build
- Format Code: python main spotlessApply

# Run Tests
- **Run all Tests:** python -m pytest
- **Run all tests in a specific file:** python -m pytest test_path -v -s
- **Run a specific test method:** python -m pytest test_path::test_method -v -s
