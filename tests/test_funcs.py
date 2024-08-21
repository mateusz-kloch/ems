from csv import DictReader, DictWriter
from pickle import load, dump
from datetime import date

import pytest

from src.funcs import (
    read_db,
    generate_new_id_num,
    generate_date,
    create_expense,
    add_new_expense,
    write_db,
    sort_expenses,
    calculate_total_expenses_amount,
    validate_args_to_edit,
    edit_expense,
    specify_filetype,
    import_csv,
    export_csv,
    generate_new_name,
)
from src.models import UserExpense


def test_read_db_userexpense(tmp_path):
    """
    Test for read_db function.

    This test checks if read_db correctly loads "UserExpense" from database.
    """
    expenses = UserExpense(id_num=1, dt='01/02/2023', amount=1.0, desc='first expense')
    db_filepath = str(tmp_path/'file.db')
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(db_filepath)
    assert expenses == restored


def test_read_db_none(tmp_path):
    """
    Test for read_db function.

    This test checks if read_db correctly loads "None" from database.
    """
    expenses = None
    db_filepath = str(tmp_path/'file.db')
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(db_filepath)
    assert expenses == restored


def test_read_db_empty_list(tmp_path):
    """
    Test for read_db function.

    This test checks if read_db correctly loads empty list from database.
    """
    expenses = []
    db_filepath = str(tmp_path/'file.db')
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(db_filepath)
    assert expenses == restored


def test_read_db_missing_extension(tmp_path):
    """
    Test for read_db function.

    This test checks whether read_db reports a "TypeError" if the file extension was not passed.
    """
    expenses = []
    db_filepath = str(tmp_path/'file')
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    with pytest.raises(TypeError) as exception:
        read_db(db_filepath)
    assert exception.type == TypeError
    assert str(exception.value) == 'Missing extension for file or unsupported file type.'


def test_read_db_another_missing_extension(tmp_path):
    """
    Test for read_db function.

    This test checks whether read_db reports a "TypeError" if the file extension was not passed.
    """
    expenses = []
    db_filepath = str(tmp_path/'file.')
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    with pytest.raises(TypeError) as exception:
        read_db(db_filepath)
    assert exception.type == TypeError
    assert str(exception.value) == 'Missing extension for file or unsupported file type.'


def test_read_db_unsupported_extension(tmp_path):
    """
    Test for read_db function.

    This test checks whether read_db reports a "TypeError" if an unsupported file extension is passed.
    """
    expenses = []
    db_filepath = str(tmp_path/'file.txt')
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    with pytest.raises(TypeError) as exception:
        read_db(db_filepath)
    assert exception.type == TypeError
    assert str(exception.value) == 'Missing extension for file or unsupported file type.'


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
    assert type(got) == type(expect)
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


def test_create_expense_newline_desc():
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


def test_validate_args_to_edit():
    dt = None
    amount = None
    desc = None
    with pytest.raises(ValueError) as exception:
        validate_args_to_edit(dt, amount, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'No values have been passed.'


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
