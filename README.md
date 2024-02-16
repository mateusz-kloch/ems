# EMS (EXPENSE MANAGEMENT SYSTEM)

## This program was created with you in mind, so that you can control and manage your budget. You can create your own database, manually add expenses to it or import them from CSV files, edit expenses in the database, and extract the database as an expense report to external CSV file.

:memo: Management is done via text mode in the terminal, and uses click library to divide program into subcommands ("add", "report", "edit", "import-from", "export-to").

This is my extension of the project from module 7 completed during the Praktyczny Python (eng: Practical Python) course.

## The expense consists of:
- ID - assigned by the program when creating an expense
- date - format: "dd/mm/yyyy", by default program uses today's date but it is possibility to add own (see: [Usage](#usage)).
- amount
- description

## In the future will be added:
- Removing existing expenses
- Assigning a given currency to the database and converting values according to current exchange rates
- Support for more external file types

## Programming tools:

### Language:
- Python 3.11.6

  ### Libraries:
    - csv
    - dataclasses
    - datetime
    - pickle
    - sys

  ### Third party libraries:
    - click 8.1.7
    - dateutil 2.8.2
    - pytest 7.4.4

:bulb: All necessary tools are pre-installed in the virtual environment.

:warning: Compatibility with previous versions not tested.

## Repository layout:
:memo: src/run.py - A main script of this project.
```
├── .venv
├── data
│       ├── budget.db
│       └── example_expenses.csv
├── original_solution
├── src
│       └── run.py
├── tests
│       ├── __init__.py
│       └── test_run.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```
:bulb: There is a directory original_solution which contains my first version of this project written during the course, so it is possible to compare the development of this project.

## Usage:
:bulb: You can use all options of each command in any configuration. There are no conflicts between them.

### "add" command:
:memo: Requires entering the amount and description of the expense. Optionally, you can enter a path to a custom database file and a date, otherwise the default path and today's date will be used.
    
    python src/run.py add 149.99 "Telephon installment"
This will add a new entry to the database file (default: "data/budget.db"). If the database does not already exist, a new one will be started.
    
    python src/run.py add 50 "Small shopping" --db-filepath=custom_dir/custom_file.db
This will add a new expense to the user-specified database file. If the database does not already exist, a new one will be started.

    python src/run.py add .99 "Chewing gum" --dt=13-09-1877
This will add a new expense to the database file with the date you specified (default is today's date). You can pass any existing separators, the program will change them to "/".

---

### "report" command:
:memo: Optionally, you can enter the path to a custom database, select a sorting method and change the order, or display expenses as Python code.

    python src/run.py report
This will display the database file as an expense table.

    python src/run.py report --db-filepath=custom_dir/custom_file.db
This will display the database from the file you specified.

    python src/run.py report --sort=date
This will sort expenses by date, by default they are sorted by ID's.

    python src/run.py report --sort=amount
This will sort expenses by amount.

    python src/run.py report --descending
This will change the order of expenses to descending, by default they are in ascending order.

---

### "edit" command:
:memo: Requires the ID of the expense to be edited and at least one of the options ("--dt", "--amount", "--desc"), otherwise an error will be reported.

:warning: ID's cannot be edited.

    python src/run.py edit 13 --db-filepath=dir/file.db --amount=130
This will edit the expense amount in the database file specified by the user.

    python src/run.py edit 24 --dt=12-03-1997
This will edit the expense date.

    python src/run.py edit 5 --amount=1500
This will edit the expense amount.

    python src/run.py edit 190 --desc="Utility fee"
This will edit the description of expense.

    python src/run.py edit 26 --dt=5.12.2000 --amount=500 --desc="Some shopping"
This will edit all expense component values.

---

### "import-from" command:
:memo: Requires a path to an external expense file that will be imported into the database. It only imports amounts and descriptions, a new ID and date will be assigned. Optionally, you can enter a path to a custom database file and a date, otherwise the default path and today's date will be used.
    
    python src/run.py import-from dir/file.csv
This will import the amounts and descriptions of expenses into a database file, generates new ID numbers and date(today's date).

    python src/run.py import-from dir/file.csv --db-filepath=custom_dir/custom_file.db
This will import expenses to database file specified by user.

    python src/run.py import-from dir/file.csv --dt=13-05-2005
This will import expenses and adds the user's date to them. User can pass any separators to date, this program will change them to "/".

---

### "export-to" command:
:memo: Requires the path to the file where the expense file will be exported. Optionally, you can enter a path to a custom database file, otherwise the default path will be used.

    python src/run.py export-to dir/file.csv
This will export expenses to external CSV file.

    python src/run.py export-to dir/dir/file.csv --db-filepath=dir/database.db
This will export expenses from database file specified by user.
