# EMS (EXPENSE MANAGEMENT SYSTEM)

## This program was created to control and manage budget. You can create your own database, manually add expenses to it or import them from CSV files, edit expenses in the database, and extract the database as an expense report to external CSV file.

:memo: Management is done via text mode in the terminal, and uses click library to divide program into subcommands ("add", "report", "edit", "import-from", "export-to").

This is my extension of the project from module 7 completed during the [Praktyczny Python](https://praktycznypython.pl/) (eng: Practical Python) course.

## The expense consists of:

- ID - assigned by the program when creating an expense
- date - format: "dd/mm/yyyy", by default program uses today's date but it is possibility to add own (see: [Usage](#usage)).
- amount
- description

## Programming tools:

### Language:

- Python 3.12

  ### Third party libraries:

    - click
    - dateutil
    - pytest

## Repository layout:

:memo: run.py - A main script of this project.

```
├── data
│       ├── budget.db
│       └── example_expenses.csv
├── src
│       ├── __init__.py
│       ├── cli.py
│       ├── funcs.py
│       ├── models.py
│       └── settings.py
├── tests
│       ├── __init__.py
│       ├── test_cli.py
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run.py
```

## Usage:

:bulb: You can use all options of each command in any configuration. There are no conflicts between them.

### "add" command:

:memo: Requires entering the amount and description of the expense. Optionally, you can enter a path to a custom database file and a date, otherwise the default path and today's date will be used.
    
    python run.py add 149.99 "Telephon installment"
This will add a new entry to the database file (default: "data/budget.db"). If the database does not already exist, a new one will be started.
    
    python run.py add 50 "Small shopping" --db-filepath=custom_dir/custom_file.db
This will add a new expense to the user-specified database file. If the database does not already exist, a new one will be started.

    python run.py add .99 "Chewing gum" --dt=13-09-1877
This will add a new expense to the database file with the date you specified (default is today's date). You can pass any existing separators, the program will change them to "/".

---

### "report" command:

:memo: Optionally, you can enter the path to a custom database, select a sorting method and change the order, or display expenses as Python code.

    python run.py report
This will display the database file as an expense table.

    python run.py report --db-filepath=custom_dir/custom_file.db
This will display the database from the file you specified.

    python run.py report --sort=date
This will sort expenses by date, by default they are sorted by ID's.

    python run.py report --sort=amount
This will sort expenses by amount.

    python run.py report --descending
This will change the order of expenses to descending, by default they are in ascending order.

---

### "edit" command:

:memo: Requires the ID of the expense to be edited and at least one of the options ("--dt", "--amount", "--desc"), otherwise an error will be reported.

:warning: ID's cannot be edited.

    python run.py edit 13 --db-filepath=dir/file.db --amount=130
This will edit the expense amount in the database file specified by the user.

    python run.py edit 24 --dt=12-03-1997
This will edit the expense date.

    python run.py edit 5 --amount=1500
This will edit the expense amount.

    python run.py edit 190 --desc="Utility fee"
This will edit the description of expense.

    python run.py edit 26 --dt=5.12.2000 --amount=500 --desc="Some shopping"
This will edit all expense component values.

---

### "import-from" command:

:memo: Requires a path to an external expense file that will be imported into the database. It only imports amounts and descriptions, a new ID and date will be assigned. Optionally, you can enter a path to a custom database file and a date, otherwise the default path and today's date will be used.
    
    python run.py import-from dir/file.csv
This will import the amounts and descriptions of expenses into a database file, generates new ID numbers and date(today's date).

    python run.py import-from dir/file.csv --db-filepath=custom_dir/custom_file.db
This will import expenses to database file specified by user.

    python run.py import-from dir/file.csv --dt=13-05-2005
This will import expenses and adds the user's date to them. User can pass any separators to date, this program will change them to "/".

---

### "export-to" command:

:memo: Requires the path to the file where the expense file will be exported. Optionally, you can enter a path to a custom database file, otherwise the default path will be used.

    python run.py export-to dir/file.csv
This will export expenses to external CSV file.

    python run.py export-to dir/dir/file.csv --db-filepath=dir/database.db
This will export expenses from database file specified by user.
