from csv import DictReader, DictWriter
from pickle import load, dump
from datetime import date

import pytest

from run import (
    MyExpense,
    read_db,
    generate_new_id_num,
    generate_date,
    create_expense,
    add_new_expense,
    write_db,
    sort_expenses,
    compute_total_expenses_value,
    import_from_csv,
    export_to_csv,
    generate_new_name
)


def test_read_db_check_content(tmp_path):
    expenses = MyExpense(id_num=1, dt='01.02.2023', value=1.0, desc='first expense')
    filepath = tmp_path/'tmp_file'
    with open(filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(filepath)
    assert expenses == restored


def test_read_db_None_content(tmp_path):
    expenses = None
    filepath = tmp_path/'tmp_file'
    with open(filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(filepath)
    assert expenses == restored


def test_read_db_empty_content(tmp_path):
    expenses = []
    filepath = tmp_path/'tmp_file'
    with open(filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(filepath)
    assert expenses == restored


def test_generate_new_id_num_no_expense_exists():
    expenses = []
    got = generate_new_id_num(expenses)
    expect = 1
    assert got == expect


def test_generate_new_id_num_exist_expense_1():
    expenses = [
        MyExpense(id_num=1, dt='01.02.2023', value=1.0, desc='first expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 2
    assert got == expect


def test_generate_new_id_num_exist_expenses_1_2():
    expenses = [
        MyExpense(id_num=1, dt='01.02.2023', value=1.0, desc='first expense'),
        MyExpense(id_num=2, dt='01.02.2023', value=1.0, desc='second expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 3
    assert got == expect


def test_generate_new_id_num_exist_expenses_1_3():
    expenses = [
        MyExpense(id_num=1,dt='01.02.2023',value=1.0,desc='first expense'),
        MyExpense(id_num=3,dt='01.02.2023',value=1.0,desc='third expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 2
    assert got == expect


def test_generate_new_id_num_exist_expense_3():
    expenses = [
        MyExpense(id_num=3, dt='01.02.2023', value=1.0, desc='third expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 1
    assert got == expect


def test_generate_date_user_date():
    dt = '23-12-24'
    got = generate_date(dt)
    expect = '23/12/2024'
    assert got == expect


def test_generate_date_no_input():
    dt = None
    got = generate_date(dt)
    expect = date.today().strftime('%d/%m/%Y')
    assert got == expect


def test_create_expense_happy_path():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = 'first expense'
    got = create_expense(id_num, dt, value, desc)
    expect = MyExpense(id_num=1, dt='12/11/2023', value=3.0, desc='first expense')
    assert got == expect


def test_create_expense_negative_value():
    id_num = 1
    dt = '12/11/2023'
    value = -3
    desc = 'first expense'
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense cannot be equal to or less than zero.'


def test_create_expense_0_value():
    id_num = 1
    dt = '12/11/2023'
    value = 0
    desc = 'first expense'
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense cannot be equal to or less than zero.'


def test_create_expense_none_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = None
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_create_expense_empty_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = ''
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_create_expense_space_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = ' '
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_create_expense_tab_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = '    '
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_create_expense_new_line_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = '\n'
    with pytest.raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_add_new_expense():
    expenses = [
        MyExpense(id_num=1, dt='01.02.2023', value=1.0, desc='first expense'),
        MyExpense(id_num=2, dt='01.02.2023', value=1.0, desc='second expense')
    ]
    new_expense = MyExpense(id_num=3, dt='01.02.2023', value=1.0, desc='third expense')
    updated_expenses = add_new_expense(expenses, new_expense)
    assert new_expense in updated_expenses


def test_write_db_file_exists(tmp_path):
    expenses = [
        MyExpense(id_num=1, dt='01.02.2023', value=1.0, desc='first expense'),
        MyExpense(id_num=2, dt='01.02.2023', value=1.0, desc='second expense')
    ]
    filepath = tmp_path/'tmp_file'
    write_db(filepath, expenses)
    assert len(list(tmp_path.iterdir())) == 1


def test_write_db_check_content(tmp_path):
    expenses = [
        MyExpense(id_num=1, dt='01.02.2023', value=1.0, desc='first expense'),
        MyExpense(id_num=2, dt='01.02.2023', value=1.0, desc='second expense')
    ]
    filepath = tmp_path/'tmp_file'
    write_db(filepath, expenses)
    with open(filepath, 'rb') as stream:
        restored = load(stream)
    assert expenses == restored


def test_sort_expeses_by_id_nums_descending_false():
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense')
    ]
    sort = None
    descending = False
    got = sort_expenses(expenses, sort, descending)
    expect = [
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense'),
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense')
    ]
    assert got == expect


def test_sort_expeses_by_id_nums_descending_True():
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense')
    ]
    sort = None
    descending = True
    got = sort_expenses(expenses, sort, descending)
    expect = [
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense'),
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense')
    ]
    assert got == expect


def test_sort_expeses_by_date_descending_false():
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense')
    ]
    sort = 'date'
    descending = False
    got = sort_expenses(expenses, sort, descending)
    expect = [
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense'),
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense')
    ]
    assert got == expect


def test_sort_expeses_by_date_descending_True():
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense')
    ]
    sort = 'date'
    descending = True
    got = sort_expenses(expenses, sort, descending)
    expect = [
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense'),
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense')
    ]
    assert got == expect


def test_sort_expeses_by_value_descending_false():
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense')
    ]
    sort = 'value'
    descending = False
    got = sort_expenses(expenses, sort, descending)
    expect = [
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense'),
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense')
    ]
    assert got == expect


def test_sort_expeses_by_value_descending_True():
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense')
    ]
    sort = 'value'
    descending = True
    got = sort_expenses(expenses, sort, descending)
    expect = [
        MyExpense(id_num=1, dt='12.03.2023', value=23.5, desc='first expense'),
        MyExpense(id_num=2, dt='23.04.2023', value=16.3, desc='second expense'),
        MyExpense(id_num=3, dt='01.02.2023', value=12.0, desc='third expense')
    ]
    assert got == expect


def test_compute_total_expenses_value_1_expense():
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=1.0, desc='first expense')
    ]
    got = compute_total_expenses_value(expenses)
    expect = 1.0
    assert got == expect


def test_compute_total_expenses_value_2_expenses():
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=1.0, desc='first expense'),
        MyExpense(id_num=2, dt='01.02.2023', value=2.2, desc='second expense')
    ]
    got = compute_total_expenses_value(expenses)
    expect = 3.2
    assert got == expect


def test_import_from_csv_happy_path(tmp_path):
    value = 1
    desc = 'first expense'
    fieldnames = ['value', 'desc']
    filepath = tmp_path/'tmp_file.csv'
    with open(filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                'value': value,
                'desc': desc
            }
        )
    got = import_from_csv(filepath)
    expect = [{'value': '1', 'desc': 'first expense'}]
    assert got == expect


def test_import_from_csv_empty_file(tmp_path):
    fieldnames = ['value', 'desc']
    filepath = tmp_path/'tmp_file.csv'
    with open(filepath, 'x', encoding='utf-8') as stream:
        DictWriter(stream, fieldnames=fieldnames)
    with pytest.raises(ValueError) as exception:
        import_from_csv(filepath)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing file content.'


def test_import_from_csv_only_fieldnames_in_file(tmp_path):
    fieldnames = ['value', 'desc']
    filepath = tmp_path/'tmp_file.csv'
    with open(filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
    with pytest.raises(ValueError) as exception:
        import_from_csv(filepath)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing file content.'


def test_export_to_csv_happy_path(tmp_path):
    filepath = tmp_path/'tmp_file.csv'
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=1.0, desc='first expense')
    ]
    export_to_csv(str(filepath), expenses)
    with open(filepath, encoding='utf-8') as stream:
        reader = DictReader(stream)
        got = [row for row in reader]
    expect = [{'desc': 'first expense', 'dt': '12.03.2023', 'id_num': '1', 'value': '1.0'}]
    assert got == expect


def test_export_to_csv_no_extension_in_filepath(tmp_path):
    filepath = tmp_path/'tmp_file'
    expenses = [
        MyExpense(id_num=1, dt='12.03.2023', value=1.0, desc='first expense')
    ]
    with pytest.raises(ValueError) as exception:
        export_to_csv(str(filepath), expenses)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing extension for new file.'


def test_generate_new_name_occurrency_2():
    filepath = 'directory/file.csv'
    occurrency = 2
    got = generate_new_name(filepath, occurrency)
    expect = 'directory/file(2).csv'
    assert got == expect


def test_generate_new_name_occurrency_3():
    filepath = 'directory/file.csv'
    occurrency = 3
    got = generate_new_name(filepath, occurrency)
    expect = 'directory/file(3).csv'
    assert got == expect