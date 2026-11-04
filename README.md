# Import-Transactions
Using bank csv files, create rules to customize or exclude bank transactions. This only works with Capital One checking and savings accounts and credit cards. I use Google sheets to manage a Summary table, but it's time consuming to manually handle each transaction.

> [!IMPORTANT]
> This project is in progress. Not all features work yet.

# How To Use
- Import Transactions throughout the month
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
- if account is 1234 then account is credit card
- if description contains Kroger then category is groceries
- if description contains transfer then excluded is True

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
