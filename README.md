# EMS (EXPENSE MANAGEMENT SYSTEM)

### This program was created to enable users to control and manage their budget. The user can create his own database, manually add expenses to it or import them from CSV files, edit expenses in database and extract the database in the form of expense report to external CSV files.

Management is done via text mode in the terminal, and uses click library to divide program into subcommands ("add", "report", "edit", "import-from", "export-to").

This is my extension of the project from module 7 completed during the Praktyczny Python course.

### The expense consists of:
- ID - assigned by the program when creating an expense
- date - format: "dd/mm/yyyy", by default program uses today's date but it is possibility to add own (see: [Usage](#usage)).
- amount
- description

### In the future will be added:
- Removing existing expenses
- Assigning a given currency to the database and converting values according to current exchange rates
- Support for more external file types

## Programming tools:

#### Language:
- Python 3.11.6

  #### Libraries:
    - csv
    - dataclasses
    - datetime
    - pickle
    - sys

  #### Third party libraries:
    - click 8.1.7
    - dateutil 2.8.2
    - pytest 7.4.4

:note: **Note:** All necessary tools are pre-installed in the virtual environment.

:warning: **Warning:** Compatibility with previous versions not tested.

## Repository layout:
```
├── data
│       ├── budget.db
│       └── example_expenses.csv
├── src
│       └── run.py
├── tests
│       ├── __init__.py
│       └── test_run.py
├── venv
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```
## Usage:
:bulb: **Tip:** All options of each command can be used in any configuration.

### "add" command:
Requires entering the amount and description of the expense. Optionally, you can enter a path to a custom database file and a date, otherwise the default path and today's date will be used.
    
    python run.py add 149.99 "Telephon installment"
This command will add a new epense to the database file (default: "data/budget.db"). If the database does not already exist, a new one will be started.
    
    python run.py add 50 "Small shopping" --db-filepath=custom_dir/custom_file.db
This command with the "--db-filepath" option will add a new expense to the database file specified by the user. If the database does not already exist, a new one will be started.

    python run.py add .99 "Chewing gum" --dt=13-09-1877
This command with the "--dt" option will add a new expense to the database file with the date specified by the user (default is today's date).  User can pass any separators to date, this program will change them to "/".

---

### "report" command:
Optionally, you can enter the path to a custom database, select a sorting method and change the order, or display expenses as Python code.

    python run.py report
This command displays the database file as an expense table.

    python run.py report --db-filepath=custom_dir/custom_file.db
This command displays the database file specified by user.

    python run.py report --sort=date
This command sorts expenses by date, by default they are sorted by ID's.

    python run.py report --sort=amount
This command sorts expenses by amount.

    python run.py report --descending
This command changes the order of expenses to descending order, by default they are in ascending order.

---

### "edit" command:
Requires the ID of the expense to be edited and at least one of the options ("--dt", "--amount", "--desc"), otherwise an error will be reported.

:warning: **Warning:** ID's cannot be edited.

    python src/run.py edit 13 --db-filepath=dir/file.db --amount=130
This command edits the expense amount in the database file specified by the user.

    python src/run.py edit 24 --dt=12-03-1997
This command edits the expense date.

    python src/run.py edit 5 --amount=1500
This command edits the expense amount.

    python src/run.py edit 190 --desc="Utility fee"
This command edits the description of expense.

    python src/run.py edit 26 --dt=5.12.2000 --amount=500 --desc="Some shopping"
This command edits all values of the expense.

---

### "import-from" command:
Requires a path to an external expense file that will be imported into the database. It only imports amounts and descriptions, a new ID and date will be assigned. Optionally, you can enter a path to a custom database file and a date, otherwise the default path and today's date will be used.
    
    python run.py import-from dir/file.csv
This command imports the amounts and descriptions of expenses into a database file, generates new ID numbers and date(today's date).

    python run.py import-from dir/file.csv --db-filepath=custom_dir/custom_file.db
This command imports expenses to database file specified by user.

    python run.py import-from dir/file.csv --dt=13-05-2005
This command imports expenses and adds the user's date to them. User can pass any separators to date, this program will change them to "/".

---

### "export-to" command:
Requires the path to the file where the expense file will be exported. Optionally, you can enter a path to a custom database file, otherwise the default path will be used.

    python run.py export-to dir/file.csv
This command exports expenses to external CSV file.

    python run.py export-to dir/dir/file.csv --db-filepath=dir/database.db
This command exports expenses from database file specified by user.
