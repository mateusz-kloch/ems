"""
This script allows users to manage their expenses by:
    - creating database
    - adds expenses directly
    - import expenses from csv file (the list of supported files will be expanded in the future)
    - export database to csv file (same as above)
    - view database as table
    - edit exisisting expenses

Database is represented by binary file with .db extension.

Expenses are represented by the "UserExpense" class, which consists of an ID, date, amount and a short description.

Management is done via text mode in the terminal, and uses click library to divide program into subcommands.

Available subcommands:
    - add
    - report
    - edit
    - import-from
    - export-to

Exit codes:
    0 - Success
    1 - TypeError
    2 - ValueError
    3 - FileNotFoundError
    4 - EOFError
    5 - KeyError

For usage examples, see the commands docs.
"""
from src.cli import cli


if __name__ == '__main__':
    cli()
