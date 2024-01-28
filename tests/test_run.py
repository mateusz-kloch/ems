"""
This script first tests the basic functions of run.py, mainly checking the happy path,
except functions that use the raise statement: [create_expense, edit_expense, spec_filetype, import_csv].
To perform the tests, it is necessary to import the "UserExpense" class.

Refers to: 
    - read_db
    - generate_new_id_num
    - generate_date
    - create_expense
    - add_new_expense
    - write_db
    - sort_expenses
    - calculate_total_expenses_amount
    - edit_expense,
    - specify_filetype
    - import_csv
    - export_csv
    - generate_new_name

Then will test run.py click commands and exception handling.
The main command is "cli". Cli only contains a pass statement.

cli subcommands:
    - "add"
    - "report"
    - "edit"
    - "import_from"
    - "export_to"

In all subcommands, the "--db-filepath" option is always used for testing purposes,
so that tests can be performed in temporary directories.
"""


from csv import DictReader, DictWriter
from pickle import load, dump
from datetime import date

from click.testing import CliRunner
import pytest

from src.run import (
    UserExpense,
    read_db,
    generate_new_id_num,
    generate_date,
    create_expense,
    add_new_expense,
    write_db,
    sort_expenses,
    calculate_total_expenses_amount,
    edit_expense,
    specify_filetype,
    import_csv,
    export_csv,
    generate_new_name,
    cli
)


def test_read_db_userexpense(tmp_path):
    """
    Test for read_db function.

    This test checks if read_db correctly writes "UserExpense" to database.
    """
    expenses = UserExpense(id_num=1, dt='01/02/2023', amount=1.0, desc='first expense')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(db_filepath)
    assert expenses == restored


def test_read_db_none(tmp_path):
    """
    Test for read_db function.

    This test checks if read_db correctly writes "None" to database.
    """
    expenses = None
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(db_filepath)
    assert expenses == restored


def test_read_db_empty_list(tmp_path):
    """
    Test for read_db function.

    This test checks if read_db correctly writes empty list to database.
    """
    expenses = []
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(db_filepath)
    assert expenses == restored


def test_generate_new_id_num_no_expense_exist():
    """
    Test for generate_new_id_num function.

    This test checks whether generate_new_id_num will correctly calculate the new id_num if no expenses exist.
    """
    expenses = []
    got = generate_new_id_num(expenses)
    expect = 1
    assert got == expect


def test_generate_new_id_num_exist_expense_1():
    """
    Test for generate_new_id_num function.

    This test checks whether generate_new_id_num will correctly calculate a new id_num if there are expense with id_num 1.
    """
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', amount=1.0, desc='first expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 2
    assert got == expect


def test_generate_new_id_num_exist_expenses_1_2():
    """
    Test for generate_new_id_num function.

    This test checks whether generate_new_id_num will correctly calculate a new id_num if there are expenses with id_num 1 and 2.
    """
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', amount=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', amount=1.0, desc='second expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 3
    assert got == expect


def test_generate_new_id_num_exist_expenses_1_3():
    """
    Test for generate_new_id_num function.

    This test checks whether generate_new_id_num will correctly calculate a new id_num if there are expenses with id_num 1 and 3.
    """
    expenses = [
        UserExpense(id_num=1,dt='01/02/2023',amount=1.0,desc='first expense'),
        UserExpense(id_num=3,dt='01/02/2023',amount=1.0,desc='third expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 2
    assert got == expect


def test_generate_new_id_num_exist_expense_3():
    """
    Test for generate_new_id_num function.

    This test checks whether generate_new_id_num will correctly calculate a new id_num if there are expense with id_num 3.
    """
    expenses = [
        UserExpense(id_num=3, dt='01/02/2023', amount=1.0, desc='third expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 1
    assert got == expect


def test_generate_date_user_date():
    """
    Test for generate_date function.

    This test checks whether generate_date correctly standardizes the user's date to the specified format.
    """
    dt = '23-12-24'
    got = generate_date(dt)
    expect = '23/12/2024'
    assert got == expect


def test_generate_date_another_user_date():
    """
    Test for generate_date function.

    This test checks whether generate_date correctly standardizes the user's date to the specified format.
    """
    dt = '23.12.24'
    got = generate_date(dt)
    expect = '23/12/2024'
    assert got == expect


def test_generate_date_no_input():
    """
    Test for generate_date function.

    This test checks that generate_date correctly determines the date and standardizes it to a specific format if the user does not enter data.
    """
    dt = None
    got = generate_date(dt)
    expect = date.today().strftime('%d/%m/%Y')
    assert got == expect


def test_create_expense():
    """
    Test for create_expense function.

    This test checks whether create_expense correctly creates an object of class "UserExpense".
    """
    id_num = 1
    dt = '12/11/2023'
    amount = 3
    desc = 'first expense'
    got = create_expense(id_num, dt, amount, desc)
    expect = UserExpense(id_num=1, dt='12/11/2023', amount=3.0, desc='first expense')
    assert got == expect


def test_create_expense_zero_amount():
    """
    Test for create_expense function.

    This test checks if create_expense reports "ValueError" if 0 was passed for the expense amount.
    """
    id_num = 1
    dt = '12/11/2023'
    amount = 0
    desc = 'first expense'
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense amount cannot be zero.'


def test_create_expense_negative_amount():
    """
    Test for create_expense function.

    This test checks if create_expense reports "ValueError" if negative number was passed for the expense amount.
    """
    id_num = 1
    dt = '12/11/2023'
    amount = -3
    desc = 'first expense'
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense amount cannot be negative.'


def test_create_expense_none_desc():
    """
    Test for create_expense function.

    This test checks whether create_expense throws a "ValueError" if an expense description has not been passed.
    """
    id_num = 1
    dt = '12/11/2023'
    amount = 3
    desc = None
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_create_expense_empty_desc():
    """
    Test for create_expense function.

    This test checks whether create_expense throws a "ValueError" error if an empty description is passed for an expense.
    """
    id_num = 1
    dt = '12/11/2023'
    amount = 3
    desc = ''
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_create_expense_space_desc():
    """
    Test for create_expense function.

    This test checks whether create_expense reports a "ValueError" if only a spacebar is passed in the expense description.
    """
    id_num = 1
    dt = '12/11/2023'
    amount = 3
    desc = ' '
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_create_expense_tab_desc():
    """
    Test for create_expense function.

    This test checks whether create_expense reports a "ValueError" if only a tab is passed in the expense description.
    """
    id_num = 1
    dt = '12/11/2023'
    amount = 3
    desc = '    '
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_create_expense_new_line_desc():
    """
    Test for create_expense function.

    This test checks whether create_expense reports a "ValueError" if only a new line sign is passed in the expense description.
    """
    id_num = 1
    dt = '12/11/2023'
    amount = 3
    desc = '\n'
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_add_new_expense():
    """
    Test for add_new_expense function.

    This test checks that add_new_expense correctly adds new_expense to the expense list.
    """
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', amount=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', amount=1.0, desc='second expense')
    ]
    new_expense = UserExpense(id_num=3, dt='01/02/2023', amount=1.0, desc='third expense')
    updated_expenses = add_new_expense(expenses, new_expense)
    assert new_expense in updated_expenses


def test_write_db_file_exist(tmp_path):
    """
    Test for write_db function.

    This test checks whether write_db correctly writes the UserExpense list to the database file.
    """
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', amount=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', amount=1.0, desc='second expense')
    ]
    db_filepath = tmp_path/'tmp_file'
    db_file = open(db_filepath, 'w')
    db_file.close()
    write_db(db_filepath, expenses)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    assert len(list(tmp_path.iterdir())) == 1
    assert expenses == restored


def test_write_db_file_not_exist(tmp_path):
    """
    Test for write_db function.

    This test checks that write_db correctly creates the database file and writes the UserExpense list to it.
    """
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', amount=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', amount=1.0, desc='second expense')
    ]
    db_filepath = tmp_path/'tmp_file'
    write_db(db_filepath, expenses)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    assert len(list(tmp_path.iterdir())) == 1
    assert expenses == restored


def test_sort_expeses_by_id_nums_descending_false():
    """
    Test for sort_expenses function.

    This test checks whether sort_expense sorts the "UserExpense" list in the default way if no sort method is specified.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense')
    ]
    sort = None
    descending = False
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense'),
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense')
    ]
    assert got == expect


def test_sort_expeses_by_id_nums_descending_True():
    """
    Test for sort_expenses function.

    This test checks whether sort_expense sorts the "UserExpense" list by default if no sort method is specified and in descending order.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense')
    ]
    sort = None
    descending = True
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense'),
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense')
    ]
    assert got == expect


def test_sort_expeses_by_date_descending_false():
    """
    Test for sort_expenses function.

    This test checks whether sort_expense sorts the "UserExpense" list by the sort by "date" method.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense')
    ]
    sort = 'date'
    descending = False
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense'),
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense')
    ]
    assert got == expect


def test_sort_expeses_by_date_descending_True():
    """
    Test for sort_expenses function.

    This test checks that sort_expense sorts the "UserExpense" list by sort method by "date" and in descending order.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense')
    ]
    sort = 'date'
    descending = True
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense'),
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense')
    ]
    assert got == expect


def test_sort_expeses_by_amount_descending_false():
    """
    Test for sort_expenses function.

    This test checks whether sort_expense sorts the "UserExpense" list by the sort by "amount" method.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense')
    ]
    sort = 'amount'
    descending = False
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense'),
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense')
    ]
    assert got == expect


def test_sort_expeses_by_amount_descending_True():
    """
    Test for sort_expenses function.

    This test checks that sort_expense sorts the "UserExpense" list by sort method by "amount" and in descending order.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense')
    ]
    sort = 'amount'
    descending = True
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=1, dt='12/03/2023', amount=23.5, desc='first expense'),
        UserExpense(id_num=2, dt='23/04/2023', amount=16.3, desc='second expense'),
        UserExpense(id_num=3, dt='01/02/2023', amount=12.0, desc='third expense')
    ]
    assert got == expect


def test_calculate_total_expenses_amount_1_expense():
    """
    Test for calculate_total_expenses_amount function.

    This test checks whether calculate_total_expenses_amount correctly counts the total amount if only 1 expense is in the "UserExpense" list.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=1.0, desc='first expense')
    ]
    got = calculate_total_expenses_amount(expenses)
    expect = 1.0
    assert got == expect


def test_calculate_total_expenses_amount_2_expenses():
    """
    Test for calculate_total_expenses_amount function.

    This test checks whether calculate_total_expense_amount correctly counts the total amount if there are 2 expenses in the "UserExpense" list.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', amount=2.2, desc='second expense')
    ]
    got = calculate_total_expenses_amount(expenses)
    expect = 3.2
    assert got == expect


def test_edit_expense_dt():
    """
    Test for edit_expense function.

    This test checks that edit_expense correctly modifies the expense date.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt='20/12/2022'
    amount = None
    desc = None
    got = edit_expense(expenses, id_num, dt, amount, desc)
    expect = [UserExpense(id_num=1, dt='20/12/2022', amount=50.0, desc='first expense')]
    assert got == expect


def test_edit_expense_amount():
    """
    Test for edit_expense function.

    This test checks that edit_expense correctly modifies the expense amount.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt = None
    amount = 150
    desc = None
    got = edit_expense(expenses, id_num, dt, amount, desc)
    expect = [UserExpense(id_num=1, dt='13/03/2013', amount=150.0, desc='first expense')]
    assert got == expect


def test_edit_expense_desc():
    """
    Test for edit_expense function.

    This test checks that edit_expense correctly modifies the expense description.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt = None
    amount = None
    desc = 'edited expense'
    got = edit_expense(expenses, id_num, dt, amount, desc)
    expect = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='edited expense')]
    assert got == expect


def test_edit_expense_dt_amount_desc():
    """
    Test for edit_expense function.

    This test verifies that edit_expense correctly modifies the date, amount, and description of the expense.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt = '20/12/2022'
    amount = 150
    desc = 'edited expense'
    got = edit_expense(expenses, id_num, dt, amount, desc)
    expect = [UserExpense(id_num=1, dt='20/12/2022', amount=150.0, desc='edited expense')]
    assert got == expect


def test_edit_expense_invalid_id_num():
    """
    Test for edit_expense function.

    This test checks that edit_expense correctly reports a "ValueError" if an invalid id number is passed.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 2
    dt = '20/12/2022'
    amount = 150
    desc = 'edited expense'
    with pytest.raises(ValueError) as exception:
        edit_expense(expenses, id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == f'ID {id_num}# not exists in database.'


def test_edit_expense_0_amount():
    """
    Test for edit_expense function.

    This test checks that edit_expense correctly reports "ValueError" if a zero amount is passed.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt = '20/12/2022'
    amount = 0
    desc = 'edited expense'
    with pytest.raises(ValueError) as exception:
        edit_expense(expenses, id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense amount cannot be zero.'


def test_edit_expense_negative_amount():
    """
    Test for edit_expense function.

    This test checks that edit_expense correctly reports "ValueError" if a negative amount is passed.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt = '20/12/2022'
    amount = -1
    desc = 'edited expense'
    with pytest.raises(ValueError) as exception:
        edit_expense(expenses, id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense amount cannot be negative.'


def test_edit_expense_empty_desc():
    """
    Test for edit_expense function.

    This test checks that edit_expense correctly reports "ValueError" if a empty description is passed.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt = '20/12/2022'
    amount = 150
    desc = ''
    with pytest.raises(ValueError) as exception:
        edit_expense(expenses, id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_edit_expense_space_desc():
    """
    Test for edit_expense function.
    
    This test checks that edit_expense correctly reports "ValueError" if a space is passed as the description.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt = '20/12/2022'
    amount = 150
    desc = ' '
    with pytest.raises(ValueError) as exception:
        edit_expense(expenses, id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_edit_expense_tab_desc():
    """
    Test for edit_expense function.
    
    This test checks that edit_expense correctly reports "ValueError" if a tab is passed as the description.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt = '20/12/2022'
    amount = 150
    desc = '    '
    with pytest.raises(ValueError) as exception:
        edit_expense(expenses, id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_edit_expense_newline_desc():
    """
    Test for edit_expense function.
    
    This test checks that edit_expense correctly reports "ValueError" if a new line tag is passed as the description.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = 1
    dt = '20/12/2022'
    amount = 150
    desc = '\n'
    with pytest.raises(ValueError) as exception:
        edit_expense(expenses, id_num, dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_specify_filetype():
    """
    Test for specify_filetype function.

    This test checks that specify_filetype correctly specifies the file type.
    """
    csv_filepath = 'dir/file.csv'
    got = specify_filetype(csv_filepath)
    expect = 'csv'
    assert got == expect


def test_specify_filetype_unsupported_extension():
    """
    Test for specify_filetype function.

    This test checks that specify_filetype correctly reports a "TypeError" if an unsupported file extension is passed.
    """
    csv_filepath = 'dir/file.txt'
    with pytest.raises(TypeError) as exception:
        specify_filetype(csv_filepath)
    assert exception.type == TypeError
    assert str(exception.value) == 'Missing extension for file or unsupported file type.'


def test_specify_filetype_invalid_extension():
    """
    Test for specify_filetype function.

    This test checks that specify_filetype correctly reports a "TypeError" if an invalid file extension is passed.
    """
    csv_filepath = 'dir/file.wa'
    with pytest.raises(TypeError) as exception:
        specify_filetype(csv_filepath)
    assert exception.type == TypeError
    assert str(exception.value) == 'Missing extension for file or unsupported file type.'


def test_specify_filetype_missing_extension():
    """
    Test for specify_filetype function.

    This test checks that specify_filetype correctly reports a "TypeError" if a file extension was not passed.
    """
    csv_filepath = 'dir/file'
    with pytest.raises(TypeError) as exception:
        specify_filetype(csv_filepath)
    assert exception.type == TypeError
    assert str(exception.value) == 'Missing extension for file or unsupported file type.'


def test_specify_filetype_another_missing_extension():
    """
    Test for specify_filetype function.

    This test checks that specify_filetype correctly reports a "TypeError" if a file extension was not passed but there is dot at end of filepath.
    """
    csv_filepath = 'dir/file.'
    with pytest.raises(TypeError) as exception:
        specify_filetype(csv_filepath)
    assert exception.type == TypeError
    assert str(exception.value) == 'Missing extension for file or unsupported file type.'


def test_import_csv(tmp_path):
    """
    Test for import_csv function.

    This test checks that import_csv correctly imports the contents of the csv file as a dictionary list.
    """
    amount = 1
    desc = 'first expense'
    headers = ['amount', 'desc']
    csv_filepath = tmp_path/'file.csv'
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow(
            {
                'amount': amount,
                'desc': desc
            }
        )
    got = import_csv(csv_filepath)
    expect = [{'amount': 1, 'desc': 'first expense'}]
    assert got == expect


def test_import_csv_empty_file(tmp_path):
    """
    Test for import_csv function.

    This test checks that import_csv correctly reports a "ValueError" if the csv file is empty.
    """
    headers = ['amount', 'desc']
    csv_filepath = tmp_path/'file.csv'
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        DictWriter(stream, fieldnames=headers)
    with pytest.raises(ValueError) as exception:
        import_csv(csv_filepath)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing file content.'


def test_import_csv_only_headers_in_file(tmp_path):
    """
    Test for import_csv function.

    This test checks whether import_csv correctly reports a "ValueError" if the csv file only contains headers.
    """
    headers = ['amount', 'desc']
    csv_filepath = tmp_path/'file.csv'
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
    with pytest.raises(ValueError) as exception:
        import_csv(csv_filepath)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing file content.'


def test_export_csv(tmp_path):
    """
    Test for export_csv function.

    This test checks that export_csv correctly creates a csv file and writes the "UserExpense" list to it.
    """
    csv_filepath = tmp_path/'file.csv'
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='12/03/2023', amount=3.0, desc='second expense')
    ]
    export_csv(str(csv_filepath), expenses)
    with open(csv_filepath, encoding='utf-8') as stream:
        reader = DictReader(stream)
        got = [row for row in reader]
    expect = [
        {'id_num': '1', 'dt': '12/03/2023', 'amount': '1.0', 'desc': 'first expense'},
        {'id_num': '2', 'dt': '12/03/2023', 'amount': '3.0', 'desc': 'second expense'}
    ]
    assert len(list(tmp_path.iterdir())) == 1
    assert got == expect


def test_generate_new_name_occurrency_2():
    """
    Test for generate_new_name function.

    This test checks whether generate_new_name correctly generates a new name for a file if a file with the same name already exists.
    """
    db_filepath = 'directory/file.csv'
    occurrency = 2
    got = generate_new_name(db_filepath, occurrency)
    expect = 'directory/file(2).csv'
    assert got == expect


def test_generate_new_name_occurrency_3():
    """
    Test for generate_new_name function.

    This test checks whether generate_new_name correctly generates a new name for a file if a file with the same name already exists.
    """
    db_filepath = 'directory/file.csv'
    occurrency = 3
    got = generate_new_name(db_filepath, occurrency)
    expect = 'directory/file(3).csv'
    assert got == expect


def test_add_db_exist(tmp_path):
    """
    Test for cli command: "add".

    This test verifies that the "add" correctly writes the new expense to the existing expenses in the database file.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=1.0, desc='first expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    amount = '1.5'
    description = 'expense'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [
        UserExpense(id_num=1, dt='12/03/2023', amount=1.0, desc='first expense'),
        UserExpense(id_num=2, dt=expect_dt, amount=1.5, desc='expense')
    ]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_with_dt_db_exist(tmp_path):
    """
    Test for cli command: "add".

    This test verifies that the "add" correctly writes the new expense with the given date to the existing database file.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=1.0, desc='first expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    amount = '1.5'
    description = 'expense'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [
        UserExpense(id_num=1, dt='12/03/2023', amount=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='13/02/2024', amount=1.5, desc='expense')
    ]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_empty_db_file(tmp_path):
    """
    Test for cli command: "add".

    This test verifies that the "add" correctly writes the new expense to an existing empty database file.
    """
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    amount = '1.5'
    description = 'expense'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, dt=expect_dt, amount=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_with_dt_empty_db_file(tmp_path):
    """
    Test for cli command: "add".

    This test verifies that the "add" correctly writes the new expense with the given date to an existing empty database file.
    """
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    amount = '1.5'
    description = 'expense'
    dt = '01/02/2003'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, dt='01/02/2003', amount=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_db_not_exist(tmp_path):
    """
    Test for cli command: "add".

    This test verifies that the "add" correctly creates the database file and writes the new expense to it.
    """
    amount = '1.5'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, dt=expect_dt, amount=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_with_dt_db_not_exist(tmp_path):
    """
    Test for cli command: "add".

    This test verifies that the "add" correctly creates a database file and writes a new expense to it with the given date.
    """
    amount = '1.5'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, dt='13/02/2024', amount=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_invalid_dt(tmp_path):
    """
    Test for cli command: "add"

    This test checks whether the "add" correctly handles an exception when an invalid date format is provided.
    """
    amount = '10'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = 'asd'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Invalid date format.'


def test_add_zero_amount(tmp_path):
    """
    Test for cli command: "add"

    This test checks whether the "add" correctly handles an exception when a zero expense amount is provided.
    """
    amount = '0'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: The expense amount cannot be zero.'
    

def test_add_negative_amount(tmp_path):
    """
    Test for cli command: "add"

    This test checks whether the "add" correctly handles an exception when a negative expense amount is provided.
    """
    amount = '-1'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', '--db-filepath', db_filepath, '--dt', dt, '--', amount, description,])
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: The expense amount cannot be negative.'


def test_add_empty_desc(tmp_path):
    """
    Test for cli command: "add"

    This test checks whether the "add" correctly handles an exception when no expense description is provided.
    """
    amount = '1'
    description = ''
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_add_space_desc(tmp_path):
    """
    Test for cli command: "add"

    This test checks whether the "add" correctly handles an exception when an expense description containing only a space is provided.
    """
    amount = '1'
    description = ' '
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_add_tab_desc(tmp_path):
    """
    Test for cli command: "add"

    This test checks whether the "add" correctly handles an exception when an expense description containing only a tab is provided.
    """
    amount = '1'
    description = ' '
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_add_new_line_desc(tmp_path):
    """
    Test for cli command: "add"

    This test checks whether the "add" correctly handles an exception when an expense description containing only a new line tag is provided.
    """
    amount = '1'
    description = '\n'
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_add_invalid_path():
    """
    Test for cli command: "add"

    This test checks whether the "add" correctly handles an exception when an invalid database path is specified.
    """
    amount = '10'
    description = 'expense'
    db_filepath = 'invalid_dir/file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', amount, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 3
    assert result.output.strip() == f'ERROR: There is no such path: {db_filepath}.'


def test_report_db_filepath(tmp_path):
    """
    Test for cli command: "report"

    This test verifies that the "report" correctly displays the expense from the database file.
    """
    expenses = [UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     124.65'


def test_report_db_filepath_show_big(tmp_path):
    """
    Test for cli command: "report"

    This test verifies that the "report" correctly tags an expense as big with a "[!]" if the threshold has been reached.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=499, desc='first expense'),
        UserExpense(id_num=2, dt='12/03/2023', amount=500, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     499.00         first expense\n    2# 12/03/2023     500.00   [!]   second expense\n~~~~~~~~~~~~~~~~~\nTotal:     999.00'


def test_report_db_filepath_sort_default(tmp_path):
    """
    Test for cli command: "report"

    This test verifies that the "report" correctly sorts expenses using the default method.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     124.65         first expense\n    2# 12/09/2021     300.00         second expense\n    3# 02/05/1999     499.00         third expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_default_descending(tmp_path):
    """
    Test for cli command: "report"

    This test verifies that the "report" correctly sorts expenses using the default method in descending order.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--descending'])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    3# 02/05/1999     499.00         third expense\n    2# 12/09/2021     300.00         second expense\n    1# 13/11/1954     124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_date(tmp_path):
    """
    Test for cli command: "report"

    This test verifies that the "report" correctly sorts expenses using the "date" method.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--sort', 'date',])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     124.65         first expense\n    3# 02/05/1999     499.00         third expense\n    2# 12/09/2021     300.00         second expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_date_descending(tmp_path):
    """
    Test for cli command: "report"

    This test verifies that the "report" correctly sorts expenses using the "date" method in descending order.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--sort', 'date', '--descending'])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    2# 12/09/2021     300.00         second expense\n    3# 02/05/1999     499.00         third expense\n    1# 13/11/1954     124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_amount(tmp_path):
    """
    Test for cli command: "report"

    This test verifies that the "report" correctly sorts expenses using the "amount" method.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--sort', 'amount',])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     124.65         first expense\n    2# 12/09/2021     300.00         second expense\n    3# 02/05/1999     499.00         third expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_amount_descending(tmp_path):
    """
    Test for cli command: "report"

    This test verifies that the "report" correctly sorts expenses using the "amount" method in descending order.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--sort', 'amount', '--descending'])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    3# 02/05/1999     499.00         third expense\n    2# 12/09/2021     300.00         second expense\n    1# 13/11/1954     124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_show_python_code(tmp_path):
    """
    Test for cli command: "report"

    This test checks whether the "report" displays expenses as a representation of Python code.
    """
    expenses = [UserExpense(id_num=1, dt='12/03/2001', amount=12, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--python'])
    assert result.exit_code == 0
    assert result.output.strip() == '[UserExpense(id_num=1, dt=\'12/03/2001\', amount=12, desc=\'first expense\')]'


def test_report_empty_db_file(tmp_path):
    """
    Test for cli command: "report"

    This test checks whether the "report" correctly handles an exception when the database file is empty.
    """
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 4
    assert result.output.strip() == 'ERROR: No data has been entered yet.'


def test_report_db_file_not_exist():
    """
    Test for cli command: "report"

    This test checks whether the "report" correctly handles an exception when the database does not exist.
    """
    db_filepath = 'not_exist_file.db'
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 4
    assert result.output.strip() == 'ERROR: No data has been entered yet.'


def test_edit(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, dt='20/12/2022', amount=150.0, desc='edited expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_edit_no_atributes(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '1'
    dt = None
    amount = None
    desc = None
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 5
    assert result.output.strip() == 'ERROR: No values have been passed.'


def test_edit_invalid_date(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '1'
    dt = 'date'
    amount = '150'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 6
    assert result.output.strip() == 'ERROR: Invalid date format.'


def test_edit_database_not_exists():
    db_filepath = 'not_exist_file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 7
    assert result.output.strip() == 'ERROR: No data has been entered yet, nothing to edit.'


def test_edit_empty_database(tmp_path):
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 7
    assert result.output.strip() == 'ERROR: No data has been entered yet, nothing to edit.'


def test_edit_invalid_id_num(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '2'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 8
    assert result.output.strip() == f'ERROR: ID {id_num}# not exists in database.'


def test_edit_0_amount(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '1'
    dt = '20/12/2022'
    amount = '0'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 8
    assert result.output.strip() == 'ERROR: The expense amount cannot be zero.'


def test_edit_negative_amount(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '1'
    dt = '20/12/2022'
    amount = '-1'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 8
    assert result.output.strip() == 'ERROR: The expense amount cannot be negative.'


def test_edit_empty_desc(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = ''
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 8
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_edit_space_desc(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = ' '
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 8
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_edit_tab_desc(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = '    '
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 8
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_edit_newline_desc(tmp_path):
    db_filepath = tmp_path/'file.db'
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = '\n'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])
    assert result.exit_code == 8
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_with_content_expenses_empty(tmp_path):
    """
    Test for cli command: "import-from"

    This test verifies that the "import-from" correctly writes expenses from a file to a database file that contains other expenses.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, amount=10, dt=expect_dt, desc='first expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'
    

def test_import_from_with_content_expenses_not_exist(tmp_path):
    """
    Test for cli command: "import-from"

    This test verifies that the "import-from" correctly creates a database file and writes expenses from the file to it.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, amount=10, dt=expect_dt, desc='first expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_import_from_with_content_user_dt(tmp_path):
    """
    Test for cli command: "import-from"

    This test verifies that the "import-z" correctly writes expenses from the file with the given date to the database file.
    """
    dt = '23.05.1984'
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath, '--dt', dt])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, amount=10, dt='23/05/1984', desc='first expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_import_from_missing_extension_in_csv_filepath(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when the imported file has no extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 9
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_invalid_extension_in_csv_filepath(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when the imported file has an invalid extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.aw')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 9
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_another_invalid_extension_in_csv_filepath(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when the imported file has an invalid extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 9
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_unsupported_extension_in_csv_filepath(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when the imported file has an unsupported extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 9
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_csv_not_exist(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when the imported file does not exist.
    """
    csv_filepath = 'not_exist_file.csv'
    db_filepath = tmp_path/'file.db'
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 10
    assert result.output.strip() == 'ERROR: File not exist.'


def test_import_from_only_headers_in_csv(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when the imported file contains only headers.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 11
    assert result.output.strip() == 'ERROR: Missing file content.'


def test_import_from_empty_csv(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when the imported file is empty.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    stream = open(csv_filepath, 'x', encoding='utf-8')
    stream.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 11
    assert result.output.strip() == 'ERROR: Missing file content.'


def test_import_from_invalid_headers_in_csv(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when the imported file contains invalid headers.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['inv_amount', 'inv_desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'inv_amount': 10, 'inv_desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 12
    assert result.output.strip() == f'ERROR: Invalid headers in {csv_filepath}.'


def test_import_from_invalid_user_dt(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when an invalid date format is provided.
    """
    dt = 'awd1'
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 13
    assert result.output.strip() == 'ERROR: Invalid date format.'


def test_import_from_0_amount_in_csv(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when one of the imported amounts is 0.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 0, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 14
    assert result.output.strip() == 'ERROR: The expense amount cannot be zero.'


def test_import_from_negative_amount_in_csv(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when one of the imported amounts is negative.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': -1, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 14
    assert result.output.strip() == 'ERROR: The expense amount cannot be negative.'


def test_import_from_no_desc_in_csv(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when one of the imported descriptions is empty.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': ''})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 14
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_space_desc_in_csv(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when one of the imported descriptions contains only a space.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': ' '})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 14
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_tab_desc_in_csv(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when one of the imported descriptions contains only a tab.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': ' '})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 14
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_new_line_desc_in_csv(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when one of the imported descriptions contains only a newline tag.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': '\n'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 14
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_invalid_db_path(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "import-from" correctly handles an exception when the database file path is invalid.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = 'invalid_dir/file.db'
    headers = ['amount', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 15
    assert result.output.strip() == f'ERROR: There is no such path: {db_filepath}.'


def test_export_to(tmp_path):
    """
    Test for cli command: "export-to"

    This test verifies that "export-to" correctly writes expenses from the database file to the external file.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    with open(csv_filepath, encoding='utf-8') as stream:
        reader = DictReader(stream)
        restored = [row for row in reader]
    expect = [{'id_num': '1', 'dt': '15/09/1857', 'amount': '567', 'desc': 'first expension'}]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved as: {csv_filepath}.'


def test_export_to_1_csv_filepath_already_exist(tmp_path):
    """
    Test for cli command: "export-to"

    This test checks whether the "export-to" command correctly generates a new name for an external file if a file with the same name already exists.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    csv_file = open(csv_filepath, 'x')
    csv_file.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    expect_csv_filepath = str(tmp_path/'file(2).csv')
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved as: {expect_csv_filepath}.'


def test_export_to_1_2_csv_filepath_already_exists(tmp_path):
    """
    Test for cli command: "export-to"

    This test checks whether the "export-to" command correctly generates a new names for an external file if a files with the same name already exists.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.csv')
    another_csv_filepath = str(tmp_path/'file(2).csv')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    csv_file = open(csv_filepath, 'x')
    csv_file.close()
    another_csv_file = open(another_csv_filepath, 'x')
    another_csv_file.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    expect_csv_filepath = str(tmp_path/'file(3).csv')
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved as: {expect_csv_filepath}.'


def test_export_to_2_csv_filepath_already_exist(tmp_path):
    """
    Test for cli command: "export-to"

    This test checks that the "export-to" command correctly ignores a previously generated name if a name for the external file is not already in use.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    first_csv_filepath = str(tmp_path/'file.csv')
    second_csv_filepath = str(tmp_path/'file(2).csv')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    csv_file = open(second_csv_filepath, 'x')
    csv_file.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', first_csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved as: {first_csv_filepath}.'


def test_export_to_missing_extension_in_csv_filepath(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "export-to" command correctly handles an exception when the external file does not have an extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 16
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_invalid_extension_in_csv_filepath(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "export-to" command correctly handles an exception when an external file has an invalid extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.1a')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 16
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_another_invalid_extension_in_csv_filepath(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "export-to" command correctly handles an exception when an external file has an invalid extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 16
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_unsupported_extension_in_csv_filepath(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "export to" command correctly handles an exception when an external file has an unsupported extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.txt')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 16
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_db_file_not_exist(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "export to" command correctly handles an exception when the database file does not exist.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = 'not_exist_file.db'
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 17
    assert result.output.strip() == 'ERROR: No data has been entered yet, nothing to write.'


def test_export_to_empty_db_file(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "export to" command correctly handles an exception when the database file is empty.
    """
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 17
    assert result.output.strip() == 'ERROR: No data has been entered yet, nothing to write.'


def test_export_to_invalid_csv_filepath(tmp_path):
    """
    Test for cli command: "import-from"

    This test checks whether the "export to" command correctly handles an exception when the path to an external file is invalid.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    csv_filepath = 'invalid_dir/file.csv'
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 18
    assert result.output.strip() == f'ERROR: There is no such path: {csv_filepath}.'