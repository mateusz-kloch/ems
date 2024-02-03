import csv
from dataclasses import dataclass
import pickle
import sys

import click


MY_EXPENSES = 'original_solution/budget.db'
CSV_EXPENSES = 'original_solution/expenses.csv'


@dataclass
class MyExpense:
    id_: int
    amount: float
    big: bool
    desc: str


    def __post_init__(self):
        if self.amount <= 0:
            raise ValueError('The expense cannot be equal to or less than zero')
        if not self.desc or self.desc.isspace():
            raise ValueError('Missing name for new expense')
        

def read_db_file(db_filename: str) -> list[MyExpense]:
    try:
        with open(db_filename, 'rb') as stream:
            restored = pickle.load(stream)
    except (EOFError, FileNotFoundError):
        restored = []
    return restored


def generate_new_id(expenses: list[MyExpense]) -> int:
    ids = {expense.id_ for expense in expenses}
    counter = 1
    while counter in ids:
        counter +=1
    return counter


def create_expense(expenses: list[MyExpense], amount: str, desc: str) -> MyExpense:
    new_id = generate_new_id(expenses)
    amount = float(amount)
    big = False
    if amount >= 1000:
        big = True
    new_expense = MyExpense(
        id_ = new_id,
        amount = float(amount),
        big = big,
        desc = desc
        )
    return new_expense


def add_new_expense(expenses: list[MyExpense], new_expense: MyExpense) -> list[MyExpense]:
    expenses.append(new_expense)
    return expenses


def write_db_file(db_filename: str, updated_expenses: list[MyExpense]) -> None:
    try:
        with open(db_filename, 'wb') as stream:
            pickle.dump(updated_expenses, stream)
        print(f'Saved to: {db_filename}')
    except FileNotFoundError:
        print(f'There is no such path: {db_filename}')
        sys.exit(2)


def import_csv_content(csv_filename: str) -> list[MyExpense]:
    with open(csv_filename, encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        expenses_from_csv = [row for row in reader]
    return expenses_from_csv


def add_my_expense(amount: str, desc: str, db_filename: str):
    expenses = read_db_file(db_filename)
    try:
        new_expense = create_expense(expenses, amount, desc)
    except ValueError as exception:
        print(f'Error: {exception.args[0]}')
        sys.exit(1)
    updated_expenses = add_new_expense(expenses, new_expense)
    write_db_file(db_filename, updated_expenses)


def show_expenses(db_filename: str) -> None:
    expenses = read_db_file(db_filename)
    print('~~ID~~ ~~AMOUNT~~ ~~BIG~~ ~~DESCRIPTION~~')
    print('~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~')
    total = 0
    for expense in expenses:
        total += expense.amount
        if expense.big:
            big = '[!]'
        else:
            big = ''
        print(f'{expense.id_:6} {expense.amount:10} {big:^8} {expense.desc}')
    print('~~~~~~~~~~~~~~~~~')
    print(f'Total: {total:10}')


def show_python_code(db_filename: str) -> None:
    expenses = read_db_file(db_filename)
    print(repr(expenses))


def add_csv_expenses(db_filename: str, csv_filename: str) -> None:
    expenses = read_db_file(db_filename)
    expenses_from_csv = import_csv_content(csv_filename)
    for expense in expenses_from_csv:
        amount , desc = expense.values()
        try:
            new_expense = create_expense(expenses, amount, desc)
        except ValueError as exception:
            print(f'Error: {exception.args[0]}')
            sys.exit(1)
        updated_expenses = add_new_expense(expenses, new_expense)
        write_db_file(db_filename, updated_expenses)


@click.group()
def cli():
    pass


@cli.command()
@click.argument('amount')
@click.argument('desc')
def add(amount: str, desc: str) -> None:
    add_my_expense(amount, desc, MY_EXPENSES)


@cli.command()
def report() -> None:
    show_expenses(MY_EXPENSES)


@cli.command()
def export_python() -> None:
    show_python_code(MY_EXPENSES)


@cli.command()
def import_csv() -> None:
    add_csv_expenses(MY_EXPENSES, CSV_EXPENSES)

if __name__ == '__main__':
    cli()