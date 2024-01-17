from csv import DictReader, DictWriter
from dataclasses import dataclass
from datetime import date
from pickle import load, dump
import sys

import click
from dateutil import parser


DEFAULT_DB_FILEPATH = 'budget.db'
DT_FORMAT = '%d/%m/%Y'
BIG_EXPENSE = 500
HELP_ADD = 'Add new expense to datebase.'
HELP_OPTION_DB_FILEPATH = 'Enter path to database file, default: budget.db'
HELP_OPTION_DT = 'Enter your date, it is recommended to enter day first. If not specified, uses today\'s date.'
HELP_REPORT = 'Viem expenses database as table.'
HELP_OPTION_SORT = 'View expenses sorted by "date" or "value", by default they are sorted by id numbers.'
HELP_OPTION_DESCENDING = 'View expenses in descending order, default: ascending.'
HELP_OPTION_PYTHON = 'View expenses as python code representation.'
HELP_IMPORT_CSV = 'Import data from file, supported file formats: csv.'
HELP_EXPORT_CSV = 'Export data to file, supported file formats: csv.'


@dataclass
class MyExpense:
    id_num: int
    dt : str
    value: float
    desc: str


    def __post_init__(self) -> ValueError:
        if self.value == 0:
            raise ValueError('The expense cannot be equal to zero.')
        if self.value < 0:
            raise ValueError('The expense cannot be negative.')
        if not self.desc or self.desc.isspace():
            raise ValueError('Missing name for new expense.')
    

    def is_big(self) -> bool:
        return self.value >= BIG_EXPENSE


def read_db(db_filepath: str) -> list[MyExpense]:
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    return restored


def generate_new_id_num(expenses: list[MyExpense]) -> int:
    id_nums = {expense.id_num for expense in expenses}
    new_id = 1
    while new_id in id_nums:
        new_id +=1
    return new_id


def generate_date(dt: str|None) -> str:
    if dt:
        dt = parser.parse(dt, dayfirst=True)
    else:
        dt = date.today()
    dt = dt.strftime(DT_FORMAT)
    return dt


def create_expense(id_num: int, dt: str, value: str, desc: str) -> MyExpense:
    new_expense = MyExpense(
        id_num = id_num,
        dt = dt,
        value = float(value),
        desc = desc
        )
    return new_expense


def add_new_expense(expenses: list[MyExpense], new_expense: MyExpense) -> list[MyExpense]:
    expenses.append(new_expense)
    return expenses


def write_db(db_filepath: str, expenses: list[MyExpense]) -> None:
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)


def sort_expenses(expenses: list[MyExpense], sort: str|None, descending: bool) -> list[MyExpense]:
    if sort == 'date':
        sorted_expenses = sorted(expenses, key=lambda x: x.dt.split('/')[::-1], reverse=descending)
    elif sort == 'value':
        sorted_expenses = sorted(expenses, key=lambda x: x.value, reverse=descending)
    else:
        sorted_expenses = sorted(expenses, key=lambda x: x.id_num, reverse=descending)
    return sorted_expenses


def compute_total_expenses_value(expenses: list[MyExpense]) -> float:
    total = 0
    for expense in expenses:
        total += expense.value
    return total


def import_from_csv(csv_filepath: str) -> list[MyExpense]:
    with open(csv_filepath, encoding='utf-8') as stream:
        reader = DictReader(stream)
        csv_content = [row for row in reader]
    if csv_content == []:
        raise ValueError('Missing file content.')
    return csv_content


def export_to_csv(csv_filepath: str, expenses: list[MyExpense]) -> None:
    if not csv_filepath.endswith('.csv'):
        raise ValueError('Missing extension for new file.')
    fieldnames = ['id_num', 'dt', 'value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        for expense in expenses:
            writer.writerow(
                {
                    'id_num': expense.id_num,
                    'dt': expense.dt,
                    'value': expense.value,
                    'desc' : expense.desc
                }
            )


def generate_new_name(filepath: str, occurrency: int) -> str:
    filepath_parts = filepath.rsplit('.', maxsplit=1)
    path, extension = filepath_parts
    new_filepath = f'{path}({str(occurrency)}).{extension}'
    return new_filepath


@click.group()
def cli():
    pass


@cli.command(help=HELP_ADD)
@click.argument('value', type=float)
@click.argument('description')
@click.option('--db-filepath', default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--dt', help=HELP_OPTION_DT)
def add(value: str, description: str, db_filepath: str, dt: str|None) -> None:
    try:
        expenses = read_db(db_filepath)
    except (EOFError, FileNotFoundError):
        expenses = []
    
    try:
        dt = generate_date(dt)
    except ValueError:
            print('Invalid date format.')
            sys.exit(1)
    
    id_num = generate_new_id_num(expenses)

    try:
        new_expense = create_expense(id_num, dt, value, description)
    except ValueError as exception:
        print(f'Error: {exception.args[0]}')
        sys.exit(2)
    
    updated_expenses = add_new_expense(expenses, new_expense)
    
    try:
        write_db(db_filepath, updated_expenses)
        print(f'Saved to: {db_filepath}.')
    except FileNotFoundError:
        print(f'There is no such path: {db_filepath}.')
        sys.exit(3)


@cli.command(help=HELP_REPORT)
@click.option('--db-filepath', default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--sort', type=click.Choice(['date', 'value']), help=HELP_OPTION_SORT)
@click.option('--descending', is_flag=True, default=False, help=HELP_OPTION_DESCENDING)
@click.option('--python', is_flag=True, default=False, help=HELP_OPTION_PYTHON)
def report(db_filepath: str, sort: str|None, descending: bool, python: bool) -> None:
    try:
        expenses = read_db(db_filepath)
    except (EOFError, FileNotFoundError):
        print('No data has been entered yet.')
        sys.exit(4)
    
    sorted_expenses = sort_expenses(expenses, sort, descending)
    
    if python:
        print(repr(expenses))
    else:
        total = compute_total_expenses_value(expenses)
        print('~~ID~~ ~~~DATE~~~ ~~VALUE~~ ~~BIG~~ ~~~DESCRIPTION~~~')
        print('~~~~~~ ~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~')
        for expense in sorted_expenses:
            if expense.is_big():
                big = '[!]'
            else:
                big = ''
            print(f'{expense.id_num:5}# {expense.dt:10} {expense.value:9} {big:^7} {expense.desc}')
        print('~~~~~~~~~~~~~~~~~')
        print(f'Total: {total:10.2f}')


@cli.command(help=HELP_IMPORT_CSV)
@click.argument('import_path')
@click.option('--db-filepath', default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--dt', help=HELP_OPTION_DT)
def import_csv(import_path: str, db_filepath: str, dt: str|None) -> None:
    try:
        expenses = read_db(db_filepath)
    except (EOFError, FileNotFoundError):
        expenses = []
    
    try:
        csv_content = import_from_csv(import_path)
    except FileNotFoundError:
        print('File not exist.')
        sys.exit(5)
    except ValueError as exception:
        print(f'Error: {exception.args[0]}')
        sys.exit(6)
    
    try:
        dt = generate_date(dt)
    except ValueError:
            print('Invalid date format.')
            sys.exit(7)

    for expense in csv_content:
        id_num = generate_new_id_num(expenses)
        value , desc = expense.values()
        try:
            new_expense = create_expense(id_num, dt, value, desc)
        except ValueError as exception:
            print(f'Error: {exception.args[0]}')
            sys.exit(8)
        
        updated_expenses = add_new_expense(expenses, new_expense)
    
    try:
        write_db(db_filepath, updated_expenses)
        print(f'Saved to: {db_filepath}.')
    except FileNotFoundError:
        print(f'There is no such path: {db_filepath}.')
        sys.exit(9)


@cli.command(help=HELP_EXPORT_CSV)
@click.argument('export_path')
@click.option('--db-filepath', default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
def export_csv(export_path: str, db_filepath: str) -> None:
    try:
        expenses = read_db(db_filepath)
    except (EOFError, FileNotFoundError):
        print('No data has been entered yet, nothing to write.')
        sys.exit(10)
    
    try:
        export_to_csv(export_path, expenses)
        print(f'Saved as: {export_path}.')
    except FileExistsError:
        occurrency = 2
        while True:
            try: 
                new_filepath = generate_new_name(export_path, occurrency)
                export_to_csv(new_filepath, expenses)
                print(f'Saved as: {new_filepath}.')
                break
            except FileExistsError:
                occurrency += 1
    except FileNotFoundError:
        print(f'There is no such path: {export_path}.')
        sys.exit(11)
    except ValueError as extension:
        print(f'Error: {extension.args[0]}')
        sys.exit(12)


if __name__ == '__main__':
    cli()