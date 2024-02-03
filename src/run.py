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


from csv import DictReader, DictWriter
from dataclasses import dataclass
from datetime import date
from pickle import load, dump
import sys

import click
from dateutil import parser


BIG_EXPENSE_THRESHOLD = 500
DEFAULT_DB_FILEPATH = 'data/budget.db'
DT_FORMAT = '%d/%m/%Y'

HELP_ADD = 'Add new expense to datebase.'
HELP_OPTION_DB_FILEPATH = 'Enter path to database file, default: data/budget.db'
HELP_OPTION_DT = 'Enter your date, it is recommended to enter day first. If not specified, uses today\'s date.'
HELP_REPORT = 'Viem expenses database as table.'
HELP_REPORT_OPTION_SORT = 'View expenses sorted by "date" or "amount", by default they are sorted by id numbers.'
HELP_REPORT_OPTION_DESCENDING = 'View expenses in descending order, default: ascending.'
HELP_REPORT_OPTION_PYTHON = 'View expenses as python code representation.'
HELP_EDIT = 'Edit existing expense. Requies to pass at least one of: --dt, --amount, --desc.'
HELP_EDIT_OPTION_DT ='Change date of expense.'
HELP_EDIT_OPTION_AMOUNT = 'Change amount of expense.'
HELP_EDIT_OPTION_DESC = 'Change description of expense.'
HELP_IMPORT_FROM = 'Import data from file, supported file formats: (csv).'
HELP_EXPORT_TO = 'Export data to file, supported file formats: (csv).'


@dataclass
class UserExpense:
    id_num: int
    dt : str
    amount: float
    desc: str


    def __post_init__(self) -> ValueError:
        if self.amount == 0:
            raise ValueError('The expense amount cannot be zero.')
        if self.amount < 0:
            raise ValueError('The expense amount cannot be negative.')
        if not self.desc or self.desc.isspace():
            raise ValueError('Missing description for the expense.')
    

    def is_big(self) -> bool:
        return self.amount >= BIG_EXPENSE_THRESHOLD


def read_db(db_filepath: str) -> list[UserExpense]:
    """
    Reads expenses from a database file and returns a list of expenses.
    
    Args:
        db_filepath (str): Path to the database file from which expenses will be loaded.

    Returns:
        list[UserExpense]: A list of all expenses from the database.
    """
    if db_filepath.endswith('.db'):
        with open(db_filepath, 'rb') as stream:
            restored = load(stream)
        return restored
    else:
        raise TypeError('Missing extension for file or unsupported file type.')


def generate_new_id_num(expenses: list[UserExpense]) -> int:
    """
    Compiles a new unique id number.

    Args:
        expenses (list[UserExpense]): A list of expenses on the basis of which a new id number will be generated.

    Returns:
        int: New id number that does not exist in the database.
    """
    id_nums = {expense.id_num for expense in expenses}
    new_id = 1
    while new_id in id_nums:
        new_id +=1
    return new_id


def generate_date(dt: str|None) -> str:
    """
    If a date has been passed, it will parse it and format it according to the specified scheme.
    Otherwise, it will assume today's date and format it according to a specific scheme.

    Args:
        dt (str|None): The date that will be adjusted or "None" if not specified.

    Returns:
        str: Date adjusted to the database format.
    """
    if dt or dt == '':
        dt = parser.parse(dt, dayfirst=True)
    else:
        dt = date.today()
    dt = dt.strftime(DT_FORMAT)
    return dt


def create_expense(id_num: int, dt: str, amount: float, desc: str) -> UserExpense:
    """
    Collects information about the expense and creates an object of the UserExpense class.

    Args:
        id_num (int): Unique id number.
        dt (str): Standardized date.
        amount (float): amount of the expense.
        desc (str): Short description.

    Return:
        UserExpense: Expense as an object of the UserExpense class.
    """
    new_expense = UserExpense(
        id_num = id_num,
        dt = dt,
        amount = amount,
        desc = desc
        )
    return new_expense


def add_new_expense(expenses: list[UserExpense], new_expense: UserExpense) -> list[UserExpense]:
    """
    Adds a new expense to the expense list.

    Args:
        expenses (list[UserExpense]): List of expenses to which the new one will be added.
        new_expense (UserExpense): An expense that will be added to existing ones.

    Returns:
        list[UserExpense]: Updated expense list.
    """
    expenses.append(new_expense)
    return expenses


def write_db(db_filepath: str, expenses: list[UserExpense]) -> None:
    """
    Saves expenses in the database, overwriting existing data.

    Args:
        db_filepath (str): Path to the database file where expenses will be saved.
        expenses (list[UserExpense]): List of expenses that will be saved in the file.

    Returns:
        None
    """
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)


def sort_expenses(expenses: list[UserExpense], sort: str|None, descending: bool) -> list[UserExpense]:
    """
    Sorts the list of expenses according to specific criteria.

    Args:
        expenses (list[UserExpense]): A list of expenses that will be sorted.
        sort (str|None): Sort type or "None" if not specified.
        descending (bool): The order of the sorted expense list.

    Returns:
        list[UserExpense]: Sorted list of expenses.
    """
    if sort == 'date':
        sorted_expenses = sorted(expenses, key=lambda x: x.dt.split('/')[::-1], reverse=descending)
    elif sort == 'amount':
        sorted_expenses = sorted(expenses, key=lambda x: x.amount, reverse=descending)
    else:
        sorted_expenses = sorted(expenses, key=lambda x: x.id_num, reverse=descending)
    return sorted_expenses


def calculate_total_expenses_amount(expenses: list[UserExpense]) -> float:
    """
    Calculates the total amount of expenses.

    Args:
        expenses (list[UserExpense]): List of expenses for which the total amount will be calculated.
    
    returns:
        float: Total amount of expenses.
    """
    total = 0
    for expense in expenses:
        total += expense.amount
    return total


def validate_args_to_edit(dt: str|None, amount: float|None, desc: str|None) -> ValueError|None:
    if not dt and not amount and not desc:
        raise ValueError('No values have been passed.')


def edit_expense(expenses: list[UserExpense], id_num: int, dt: str|None, amount: float|None, desc: str|None) -> list[UserExpense]:
    """
    Edits expense of id number specified by user.

    Args:
        expenses (list[UserExpense]): The list of expenses that will be modified.
        id_num (int): The identification number of the expense that will be modified.
        dt (str|None): New expense date, if defined.
        amount (float|None): New expense amount, if defined.
        desc (str): New expense description, if defined.

    Returns:
        list[UserExpense]: Modified expense list.
    """
    ids = {expense.id_num for expense in expenses}
    if id_num not in ids:
        raise ValueError(f'ID {id_num}# not exists in database.')
    if amount != None and amount == 0:
        raise ValueError('The expense amount cannot be zero.')
    if amount != None and amount < 0:
        raise ValueError('The expense amount cannot be negative.')
    if desc != None and len(desc) < 1 or desc != None and desc.isspace():
        raise ValueError('Missing description for the expense.')
    for expense in expenses:
        if expense.id_num == id_num:
            if dt:
                expense.dt = dt
            if amount:
                expense.amount = amount
            if desc:
                expense.desc = desc
    return expenses


def specify_filetype(filepath: str) -> str:
    """
    Specifies the file type.
    If the file is not supported or is missing an extension, it throws a "TypeError".
    
    Args:
        filepath (str): The path to the file whose type will be specified.

    returns:
        str: File type.
    """
    if filepath.endswith('.csv'):
        file_type = 'csv'
    else:
        raise TypeError('Missing extension for file or unsupported file type.')
    return file_type


def import_csv(csv_filepath: str) -> list[dict]:
    """
    Reads the content of a csv file and extracts the amount and description of the expense.
    If the file content is empty, it throws "ValueError"

    Args:
        csv_filepath (str): Path to the csv file from which expenses will be imported.

    Returns:
        list[dict]: A list of rows from the csv file content in the form of dictionaries containing amounts for "amount" and "desc".
    """
    with open(csv_filepath, encoding='utf-8') as stream:
        reader = DictReader(stream)
        csv_expenses = [{'amount': float(row['amount']), 'desc': row['desc']} for row in reader]
    if csv_expenses == []:
        raise ValueError('Missing file content.')
    return csv_expenses


def export_csv(csv_filepath: str, expenses: list[UserExpense]) -> None:
    """
    Exports expenses to csv file.

    Args:
        csv_filepath (str): Path to the csv file to which expenses will be exported.
        expenses (list[UserExpense]): List of expenses that will be exported.
    Returns:
        None
    """
    headers = ['id_num', 'dt', 'amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(
                {
                    'id_num': expense.id_num,
                    'dt': expense.dt,
                    'amount': expense.amount,
                    'desc' : expense.desc
                }
            )


def generate_new_name(filepath: str, occurrency: int) -> str:
    """
    Adds occurrence to filename.
    For example, if "file.extension" already exists, a new name is returned: "file(2).extension".
    "file(2).extension" -> "file(3).extension", etc.

    Args:
        filepath (str): The path of the file for which a new name will be generated.
        occurrency (int): A number specifying which occurrence of a given filename.

    Returns:
        str: The new file path with the occurrency in the file name.
    """
    filepath_parts = filepath.rsplit('.', maxsplit=1)
    path, extension = filepath_parts
    new_filepath = f'{path}({str(occurrency)}).{extension}'
    return new_filepath


@click.group()
def cli():
    pass


@cli.command(help=HELP_ADD)
@click.argument('amount', type=float)
@click.argument('desc')
@click.option('--db-filepath', default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--dt', help=HELP_OPTION_DT)
def add(amount: float, desc: str, db_filepath: str, dt: str|None) -> None:
    """
    Adds an expense to the database if it exists or creates a new one.
    It is possible to add one expenses at a time.

    Args:
        amount (float): The amount of the expense that will be added.
        desc (str): Short description of expense.
    
    Options: (can be used in any configuration)
        --db-filepath (str): The path to custom database.
        --dt (str|None): The date that will be assigned to the expense. It is recommend to enter day, month and year. By default todays date will be assigned.
        
    Returns:
        None
        
    Usage examples:
        python src/run.py add 149.99 "Telephon installment"
        python src/run.py add 50 "Small shopping" --db-filepath=dir/dir/file.db
        python src/run.py add .99 "Chewing gum" --dt=13-09-1877
        python src/run.py add 230 "Shopping" --dt=5.4.1967
        python src/run.py add 25 "Electricity bill" --dt="12 06 2015" 
    """
    try:
        expenses = read_db(db_filepath)
    except TypeError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except (EOFError, FileNotFoundError):
        expenses = []
    
    try:
        dt = generate_date(dt)
    except ValueError:
            print('ERROR: Invalid date format.')
            sys.exit(2)
    
    id_num = generate_new_id_num(expenses)

    try:
        new_expense = create_expense(id_num, dt, amount, desc)
    except ValueError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(2)
    
    updated_expenses = add_new_expense(expenses, new_expense)
    
    try:
        write_db(db_filepath, updated_expenses)
        print(f'Saved to: {db_filepath}.')
    except FileNotFoundError:
        print(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)


@cli.command(help=HELP_REPORT)
@click.option('--db-filepath', default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--sort', type=click.Choice(['date', 'amount']), help=HELP_REPORT_OPTION_SORT)
@click.option('--descending', is_flag=True, default=False, help=HELP_REPORT_OPTION_DESCENDING)
@click.option('--python', is_flag=True, default=False, help=HELP_REPORT_OPTION_PYTHON)
def report(db_filepath: str, sort: str|None, descending: bool, python: bool) -> None:
    """
    Shows expenses database as table.
    If the expense amount exceeds a certain threshold, the expense will be marked with a "[!]" sign.
    
    Options: (can be used in any configuration)
        --db-filepath (str): The path to custom database.
        --sort (str|None): Specifies expenses sorting method, select: "date" or "amount". By default they are sorted by id numbers.
        --descending (bool): Changes order of expenses. Default order is ascending.
        --python (bool): Displays python code representations instead of expense table.
    
    Returns:
        None
        
    Usage examples:
        python src/run.py report
        python src/run.py report --db-filepath=dir/database.db
        python src/run.py report --sort=date
        python src/run.py report --sort=amount --descending
        python src/run.py report --python
    """
    try:
        expenses = read_db(db_filepath)
    except FileNotFoundError:
        print(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)
    except TypeError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except EOFError:
        print('ERROR: No data has been entered yet, nothing to display.')
        sys.exit(4)
    
    sorted_expenses = sort_expenses(expenses, sort, descending)
    
    if python:
        print(repr(expenses))
    else:
        total = calculate_total_expenses_amount(expenses)
        print('~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~')
        print('~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~')
        for expense in sorted_expenses:
            if expense.is_big():
                big = '[!]'
            else:
                big = ''
            print(f'{expense.id_num:5}# {expense.dt:10} {expense.amount:10.2f} {big:^7} {expense.desc}')
        print('~~~~~~~~~~~~~~~~~')
        print(f'Total: {total:10.2f}')


@cli.command(help=HELP_EDIT)
@click.argument('id-num', type=int)
@click.option('--db-filepath', default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--dt', help=HELP_EDIT_OPTION_DT)
@click.option('--amount', type=float, help=HELP_EDIT_OPTION_AMOUNT)
@click.option('--desc', help=HELP_EDIT_OPTION_DESC)
def edit(id_num: int, db_filepath: str, dt: str|None, amount: float|None, desc: str|None) -> None:
    """
    Edits components of expense in database.
    The expense to be edited is identified by an id number.
    If no option is specified (--dt, --amount, --desc) or option is empty, no changes will be made.

    Args:
        id-num (int): The identification number of the expense that will be edited.

    Options: (can be used in any configuration)
        --db-filepath (str): The path to custom database.
        --dt (str): Specifies new dt for the expense.
        --amount (float): Specifies new amount for the expense.
        --desc (str): Specifies new description for the expense.

    Returns:
        None

    Usage examples:
        python src/run.py edit 13 --db-filepath=dir/file.db --amount=130
        python src/run.py edit 24 --dt=12-03-1997
        python src/run.py edit 5 --amount=1500
        python src/run.py edit 190 --desc="Utility fee"
        python src/run.py edit 26 --dt=5.12.2000 --amount=500 --desc="Some shopping"
    """
    try:
        validate_args_to_edit(dt, amount, desc)
    except ValueError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(2)
    
    if dt:
        try:
            dt = generate_date(dt)
        except ValueError:
                print('ERROR: Invalid date format.')
                sys.exit(2)
    
    try:
        expenses = read_db(db_filepath)
    except FileNotFoundError:
        print(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)
    except TypeError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except EOFError:
        print('ERROR: No data has been entered yet, nothing to edit.')
        sys.exit(4)
    
    try:
        updated_expenses = edit_expense(expenses, id_num, dt, amount, desc)
    except ValueError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(2)

    try:
        write_db(db_filepath, updated_expenses)
        print(f'Saved to: {db_filepath}.')
    except FileNotFoundError:
        print(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)


@cli.command(help=HELP_IMPORT_FROM)
@click.argument('import-path')
@click.option('--db-filepath', default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--dt', help=HELP_OPTION_DT)
def import_from(import_path: str, db_filepath: str, dt: str|None) -> None:
    """
    Imports expenses from file to the database if it exists or creates a new one.
    It is possible to import expenses from one file at a time.
    At this time only csv files are supported.

    Args:
        import-path (str): Path to the file from which expenses will be imported.
    
    Options: (can be used in any configuration)
        --db-filepath (str): The path to custom database.
        --dt (str|None): The date that will be assigned to the expenses from file. It is recommend to enter day, month and year. By default todays date will be assigned.
    
    Returns:
        None
        
    Usage examples:
        python src/run.py import-from dir/file.csv
        python src/run.py import-from "some dir/file.csv" --db-filepath=dir/database.db
        python src/run.py import-from dir/dir/file.csv --dt=13-05-2005
    
    Path to a sample csv file with expenses: data/example_expenses.csv
    """
    try:
        file_type = specify_filetype(import_path)
    except TypeError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(1)

    try:
        expenses = read_db(db_filepath)
    except TypeError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except (EOFError, FileNotFoundError):
        expenses = []
    
    if file_type == 'csv':
        try:
            file_content = import_csv(import_path)
        except FileNotFoundError:
            print('ERROR: File not exist.')
            sys.exit(3)
        except ValueError as exception:
            print(f'ERROR: {exception.args[0]}')
            sys.exit(2)
        except KeyError:
            print(f'ERROR: Invalid headers in {import_path}.')
            sys.exit(5)
    
    try:
        dt = generate_date(dt)
    except ValueError:
            print('ERROR: Invalid date format.')
            sys.exit(2)

    for expense in file_content:
        
        id_num = generate_new_id_num(expenses)
        amount, desc = expense.values()
        try:
            new_expense = create_expense(id_num, dt, amount, desc)
        except ValueError as exception:
            print(f'ERROR: {exception.args[0]}')
            sys.exit(2)
        
        updated_expenses = add_new_expense(expenses, new_expense)
    
    try:
        write_db(db_filepath, updated_expenses)
        print(f'Saved to: {db_filepath}.')
    except FileNotFoundError:
        print(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)


@cli.command(help=HELP_EXPORT_TO)
@click.argument('export-path')
@click.option('--db-filepath', default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
def export_to(export_path: str, db_filepath: str) -> None:
    """
    Export expenses from database to file.
    It is possible to export expenses to one file at a time.
    At this time only csv files are supported.

    Args:
        export-path (str): Path to the csv file to which expenses will be exported.
    
    Options:
        --db-filepath (str): The path to custom database.
    
    Returns:
        None
        
    Usage examples:
        python src/run.py export-to dir/file.csv
        python src/run.py export-to dir/dir/file.csv --db-filepath=dir/database.db
    """
    try:
        file_type = specify_filetype(export_path)
    except TypeError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    
    try:
        expenses = read_db(db_filepath)
    except FileNotFoundError:
        print(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)
    except TypeError as exception:
        print(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except EOFError:
        print('ERROR: No data has been entered yet, nothing to write.')
        sys.exit(4)
    
    if file_type == 'csv':
        try:
            export_csv(export_path, expenses)
            print(f'Saved as: {export_path}.')
        except FileExistsError:
            occurrency = 2
            while True:
                try: 
                    new_filepath = generate_new_name(export_path, occurrency)
                    export_csv(new_filepath, expenses)
                    print(f'Saved as: {new_filepath}.')
                    break
                except FileExistsError:
                    occurrency += 1
        except FileNotFoundError:
            print(f'ERROR: There is no such path: {export_path}.')
            sys.exit(3)


if __name__ == '__main__':
    cli()
