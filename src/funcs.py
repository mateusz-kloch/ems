from csv import DictReader, DictWriter
from datetime import date
from pickle import load, dump

from dateutil import parser

from src.models import UserExpense
from src.settings import DT_FORMAT
    

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
            restored: list[UserExpense] = load(stream)
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
    id_nums: set[int] = {expense.id_num for expense in expenses}
    new_id: int = 1
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
        dt: str|None = parser.parse(dt, dayfirst=True)
    else:
        dt: str = date.today()
    dt: str = dt.strftime(DT_FORMAT)
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
    new_expense: UserExpense = UserExpense(
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
        sorted_expenses: list[UserExpense] = sorted(expenses, key=lambda x: x.dt.split('/')[::-1], reverse=descending)
    elif sort == 'amount':
        sorted_expenses: list[UserExpense] = sorted(expenses, key=lambda x: x.amount, reverse=descending)
    else:
        sorted_expenses: list[UserExpense] = sorted(expenses, key=lambda x: x.id_num, reverse=descending)
    return sorted_expenses


def calculate_total_expenses_amount(expenses: list[UserExpense]) -> float:
    """
    Calculates the total amount of expenses.

    Args:
        expenses (list[UserExpense]): List of expenses for which the total amount will be calculated.
    
    returns:
        float: Total amount of expenses.
    """
    total: int = 0
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
    ids: set[int] = {expense.id_num for expense in expenses}
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
        file_type: str = 'csv'
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
        reader: DictReader[str] = DictReader(stream)
        csv_expenses: list[dict[str, any]] = [{'amount': float(row['amount']), 'desc': row['desc']} for row in reader]
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
    headers: list[str] = ['id_num', 'dt', 'amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer: DictWriter[str] = DictWriter(stream, fieldnames=headers)
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
    filepath_parts: list[str] = filepath.rsplit('.', maxsplit=1)
    path: str
    extension: str
    path, extension = filepath_parts
    new_filepath: str = f'{path}({str(occurrency)}).{extension}'
    return new_filepath


if __name__ == '__main__':
    pass
