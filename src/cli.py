"""
Available commands:
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
"""
import sys
from typing import Final

import click

from src.funcs import (
    add_new_expense,
    calculate_total_expenses_amount,
    create_expense,
    edit_expense,
    export_csv,
    generate_date,
    generate_new_id_num,
    generate_new_name,
    import_csv,
    read_db,
    sort_expenses,
    specify_filetype,
    validate_args_to_edit,
    write_db
)
from src.models import UserExpense


DEFAULT_DB_FILEPATH: Final[str] = 'data/budget.db'

HELP_ADD: Final[str] = 'Add new expense to datebase.'
HELP_OPTION_DB_FILEPATH: Final[str] = 'Enter path to database file, default: data/budget.db'
HELP_OPTION_DT: Final[str] = 'Enter your date, it is recommended to enter day first. If not specified, uses today\'s date.'
HELP_REPORT: Final[str] = 'Viem expenses database as table.'
HELP_REPORT_OPTION_SORT: Final[str] = 'View expenses sorted by "date" or "amount", by default they are sorted by id numbers.'
HELP_REPORT_OPTION_DESCENDING: Final[str] = 'View expenses in descending order, default: ascending.'
HELP_REPORT_OPTION_PYTHON: Final[str] = 'View expenses as python code representation.'
HELP_EDIT: Final[str] = 'Edit existing expense. Requies to pass at least one of: --dt, --amount, --desc.'
HELP_EDIT_OPTION_DT: Final[str] ='Change date of expense.'
HELP_EDIT_OPTION_AMOUNT: Final[str] = 'Change amount of expense.'
HELP_EDIT_OPTION_DESC: Final[str] = 'Change description of expense.'
HELP_IMPORT_FROM: Final[str] = 'Import data from file, supported file formats: (csv).'
HELP_EXPORT_TO: Final[str] = 'Export data to file, supported file formats: (csv).'


@click.group()
def cli():
    pass


@cli.command(help=HELP_ADD)
@click.argument('amount', type=float)
@click.argument('desc', type=str)
@click.option('--db-filepath', type=str, default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--dt', type=str, help=HELP_OPTION_DT)
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
        expenses: list[UserExpense] = read_db(db_filepath)
    except TypeError as exception:
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except (EOFError, FileNotFoundError):
        expenses: list[UserExpense] = []
    
    try:
        dt: str = generate_date(dt)
    except ValueError:
            click.echo('ERROR: Invalid date format.')
            sys.exit(2)
    
    id_num: int = generate_new_id_num(expenses)

    try:
        new_expense: UserExpense = create_expense(id_num, dt, amount, desc)
    except ValueError as exception:
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(2)
    
    updated_expenses: list[UserExpense] = add_new_expense(expenses, new_expense)
    
    try:
        write_db(db_filepath, updated_expenses)
        click.echo(f'Saved to: {db_filepath}.')
    except FileNotFoundError:
        click.echo(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)


@cli.command(help=HELP_REPORT)
@click.option('--db-filepath', type=str, default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--sort', type=click.Choice(['date', 'amount']), help=HELP_REPORT_OPTION_SORT)
@click.option('--descending', type=str, is_flag=True, default=False, help=HELP_REPORT_OPTION_DESCENDING)
@click.option('--python', type=str, is_flag=True, default=False, help=HELP_REPORT_OPTION_PYTHON)
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
        expenses: list[UserExpense] = read_db(db_filepath)
    except FileNotFoundError:
        click.echo(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)
    except TypeError as exception:
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except EOFError:
        click.echo('ERROR: No data has been entered yet, nothing to display.')
        sys.exit(4)
    
    sorted_expenses: list[UserExpense] = sort_expenses(expenses, sort, descending)
    
    if python:
        click.echo(repr(expenses))
    else:
        total = calculate_total_expenses_amount(expenses)
        click.echo('~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~')
        click.echo('~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~')
        for expense in sorted_expenses:
            if expense.is_big():
                big = '[!]'
            else:
                big = ''
            click.echo(f'{expense.id_num:5}# {expense.dt:10} {expense.amount:10.2f} {big:^7} {expense.desc}')
        click.echo('~~~~~~~~~~~~~~~~~')
        click.echo(f'Total: {total:10.2f}')


@cli.command(help=HELP_EDIT)
@click.argument('id-num', type=int)
@click.option('--db-filepath', type=str, default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--dt', type=str, help=HELP_EDIT_OPTION_DT)
@click.option('--amount', type=float, help=HELP_EDIT_OPTION_AMOUNT)
@click.option('--desc', type=str, help=HELP_EDIT_OPTION_DESC)
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
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(2)
    
    if dt:
        try:
            dt: str = generate_date(dt)
        except ValueError:
                click.echo('ERROR: Invalid date format.')
                sys.exit(2)
    
    try:
        expenses: list[UserExpense] = read_db(db_filepath)
    except FileNotFoundError:
        click.echo(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)
    except TypeError as exception:
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except EOFError:
        click.echo('ERROR: No data has been entered yet, nothing to edit.')
        sys.exit(4)
    
    try:
        updated_expenses: list[UserExpense] = edit_expense(expenses, id_num, dt, amount, desc)
    except ValueError as exception:
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(2)

    try:
        write_db(db_filepath, updated_expenses)
        click.echo(f'Saved to: {db_filepath}.')
    except FileNotFoundError:
        click.echo(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)


@cli.command(help=HELP_IMPORT_FROM)
@click.argument('import-path', type=str)
@click.option('--db-filepath', type=str, default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
@click.option('--dt', type=str, help=HELP_OPTION_DT)
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
        file_type: str = specify_filetype(import_path)
    except TypeError as exception:
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(1)

    try:
        expenses: list[UserExpense] = read_db(db_filepath)
    except TypeError as exception:
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except (EOFError, FileNotFoundError):
        expenses: list[UserExpense] = []
    
    if file_type == 'csv':
        try:
            file_content: list[dict] = import_csv(import_path)
        except FileNotFoundError:
            click.echo('ERROR: File not exist.')
            sys.exit(3)
        except ValueError as exception:
            click.echo(f'ERROR: {exception.args[0]}')
            sys.exit(2)
        except KeyError:
            click.echo(f'ERROR: Invalid headers in {import_path}.')
            sys.exit(5)
    
    try:
        dt: str = generate_date(dt)
    except ValueError:
            click.echo('ERROR: Invalid date format.')
            sys.exit(2)

    for expense in file_content:
        
        id_num: int = generate_new_id_num(expenses)
        amount: float
        desc: str
        amount, desc = expense.values()
        try:
            new_expense: UserExpense = create_expense(id_num, dt, amount, desc)
        except ValueError as exception:
            click.echo(f'ERROR: {exception.args[0]}')
            sys.exit(2)
        
        updated_expenses: list[UserExpense] = add_new_expense(expenses, new_expense)
    
    try:
        write_db(db_filepath, updated_expenses)
        click.echo(f'Saved to: {db_filepath}.')
    except FileNotFoundError:
        click.echo(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)


@cli.command(help=HELP_EXPORT_TO)
@click.argument('export-path', type=str)
@click.option('--db-filepath', type=str, default=DEFAULT_DB_FILEPATH, help=HELP_OPTION_DB_FILEPATH)
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
        file_type: str = specify_filetype(export_path)
    except TypeError as exception:
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    
    try:
        expenses: list[UserExpense] = read_db(db_filepath)
    except FileNotFoundError:
        click.echo(f'ERROR: There is no such path: {db_filepath}.')
        sys.exit(3)
    except TypeError as exception:
        click.echo(f'ERROR: {exception.args[0]}')
        sys.exit(1)
    except EOFError:
        click.echo('ERROR: No data has been entered yet, nothing to write.')
        sys.exit(4)
    
    if file_type == 'csv':
        try:
            export_csv(export_path, expenses)
            click.echo(f'Saved as: {export_path}.')
        except FileExistsError:
            occurrency: int = 2
            while True:
                try: 
                    new_filepath: str = generate_new_name(export_path, occurrency)
                    export_csv(new_filepath, expenses)
                    click.echo(f'Saved as: {new_filepath}.')
                    break
                except FileExistsError:
                    occurrency += 1
        except FileNotFoundError:
            click.echo(f'ERROR: There is no such path: {export_path}.')
            sys.exit(3)


if __name__ == '__main__':
    pass
