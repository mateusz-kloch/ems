# EMS (EXPENSE MANAGEMENT SYSTEM)

## This program was created to enable users to control and manage their budget. The user can create his own database, manually add expenses to it or import them from CSV files and extract the database in the form of expense reports to external CSV files.

## In the future will be added:
- Possibility to edit existing expenses
- Possibility of assigning a given currency to the database and converting values according to current exchange rates
- Support for more external file types

### Programming tools:

#### Language:
- Python 3.11.6
  ##### Libraries:
    - csv
    - dataclasses
    - datetime
    - pickle
    - sys

  ##### Third party libraries:
    - click 8.1.7
    - dateutil 2.8.2
    - pytest 7.4.4

##### All necessary tools are pre-installed in the virtual environment.
##### Compatibility with previous versions not tested.

### Directories layout:
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
