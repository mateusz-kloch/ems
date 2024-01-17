"""
This script first tests the basic functions of run.py, mainly checking the happy path,
except for functions where the raise statement is used: [create_expense, import_csv, import_to_csv].

Refers to: 
    - read_db
    - generate_new_id_num
    - generate_date
    - create_expense
    - add_new_expense
    - write_db
    - sort_expenses
    - compute_total_expenses_value
    - import_csv
    - export_csv
    - generate_new_name

Next will test click commands of run.py and there will be exception handling.
Main command is "cli". Cli contains only pass statement.

cli subcommands:
    - "add"
    - "report"
    - "import_from"
    - "export_to"

In all subcommands option "--db-filepath" is always used for testing purposes,
so that a temporary directory can be used.
"""


from csv import DictReader, DictWriter
from pickle import load, dump
from datetime import date

from click.testing import CliRunner
from pytest import raises

from run import (
    UserExpense,
    read_db,
    generate_new_id_num,
    generate_date,
    create_expense,
    add_new_expense,
    write_db,
    sort_expenses,
    compute_total_expenses_value,
    import_csv,
    export_csv,
    generate_new_name,
    cli
)


def test_read_db_check_content(tmp_path):
    expenses = UserExpense(id_num=1, dt='01/02/2023', value=1.0, desc='first expense')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(db_filepath)
    assert expenses == restored


def test_read_db_None_content(tmp_path):
    expenses = None
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(db_filepath)
    assert expenses == restored


def test_read_db_empty_content(tmp_path):
    expenses = []
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    restored = read_db(db_filepath)
    assert expenses == restored


def test_generate_new_id_num_no_expense_exist():
    expenses = []
    got = generate_new_id_num(expenses)
    expect = 1
    assert got == expect


def test_generate_new_id_num_exist_expense_1():
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', value=1.0, desc='first expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 2
    assert got == expect


def test_generate_new_id_num_exist_expenses_1_2():
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', value=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', value=1.0, desc='second expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 3
    assert got == expect


def test_generate_new_id_num_exist_expenses_1_3():
    expenses = [
        UserExpense(id_num=1,dt='01/02/2023',value=1.0,desc='first expense'),
        UserExpense(id_num=3,dt='01/02/2023',value=1.0,desc='third expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 2
    assert got == expect


def test_generate_new_id_num_exist_expense_3():
    expenses = [
        UserExpense(id_num=3, dt='01/02/2023', value=1.0, desc='third expense')
    ]
    got = generate_new_id_num(expenses)
    expect = 1
    assert got == expect


def test_generate_date_user_date():
    dt = '23-12-24'
    got = generate_date(dt)
    expect = '23/12/2024'
    assert got == expect


def test_generate_date_another_user_date():
    dt = '23.12.24'
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
    expect = UserExpense(id_num=1, dt='12/11/2023', value=3.0, desc='first expense')
    assert got == expect


def test_create_expense_zero_value():
    id_num = 1
    dt = '12/11/2023'
    value = 0
    desc = 'first expense'
    with raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense cannot be equal to zero.'


def test_create_expense_negative_value():
    id_num = 1
    dt = '12/11/2023'
    value = -3
    desc = 'first expense'
    with raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense cannot be negative.'


def test_create_expense_none_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = None
    with raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_create_expense_empty_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = ''
    with raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_create_expense_space_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = ' '
    with raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_create_expense_tab_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = '    '
    with raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_create_expense_new_line_desc():
    id_num = 1
    dt = '12/11/2023'
    value = 3
    desc = '\n'
    with raises(ValueError) as exception:
        create_expense(id_num, dt, value, desc)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing name for new expense.'


def test_add_new_expense():
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', value=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', value=1.0, desc='second expense')
    ]
    new_expense = UserExpense(id_num=3, dt='01/02/2023', value=1.0, desc='third expense')
    updated_expenses = add_new_expense(expenses, new_expense)
    assert new_expense in updated_expenses


def test_write_db_file_exist(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', value=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', value=1.0, desc='second expense')
    ]
    db_filepath = tmp_path/'tmp_file'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    write_db(db_filepath, expenses)
    assert len(list(tmp_path.iterdir())) == 1


def test_write_db_file_not_exist(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', value=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', value=1.0, desc='second expense')
    ]
    db_filepath = tmp_path/'tmp_file'
    write_db(db_filepath, expenses)
    assert len(list(tmp_path.iterdir())) == 1


def test_write_db_check_content(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='01/02/2023', value=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', value=1.0, desc='second expense')
    ]
    db_filepath = tmp_path/'tmp_file'
    write_db(db_filepath, expenses)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    assert expenses == restored


def test_sort_expeses_by_id_nums_descending_false():
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense')
    ]
    sort = None
    descending = False
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense'),
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense')
    ]
    assert got == expect


def test_sort_expeses_by_id_nums_descending_True():
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense')
    ]
    sort = None
    descending = True
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense'),
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense')
    ]
    assert got == expect


def test_sort_expeses_by_date_descending_false():
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense')
    ]
    sort = 'date'
    descending = False
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense'),
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense')
    ]
    assert got == expect


def test_sort_expeses_by_date_descending_True():
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense')
    ]
    sort = 'date'
    descending = True
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense'),
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense')
    ]
    assert got == expect


def test_sort_expeses_by_value_descending_false():
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense')
    ]
    sort = 'value'
    descending = False
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense'),
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense')
    ]
    assert got == expect


def test_sort_expeses_by_value_descending_True():
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense')
    ]
    sort = 'value'
    descending = True
    got = sort_expenses(expenses, sort, descending)
    expect = [
        UserExpense(id_num=1, dt='12/03/2023', value=23.5, desc='first expense'),
        UserExpense(id_num=2, dt='23/04/2023', value=16.3, desc='second expense'),
        UserExpense(id_num=3, dt='01/02/2023', value=12.0, desc='third expense')
    ]
    assert got == expect


def test_compute_total_expenses_value_1_expense():
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=1.0, desc='first expense')
    ]
    got = compute_total_expenses_value(expenses)
    expect = 1.0
    assert got == expect


def test_compute_total_expenses_value_2_expenses():
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='01/02/2023', value=2.2, desc='second expense')
    ]
    got = compute_total_expenses_value(expenses)
    expect = 3.2
    assert got == expect


def test_import_csv_happy_path(tmp_path):
    value = 1
    desc = 'first expense'
    fieldnames = ['value', 'desc']
    csv_filepath = tmp_path/'file.csv'
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {
                'value': value,
                'desc': desc
            }
        )
    got = import_csv(csv_filepath)
    expect = [{'value': '1', 'desc': 'first expense'}]
    assert got == expect


def test_import_csv_empty_file(tmp_path):
    fieldnames = ['value', 'desc']
    csv_filepath = tmp_path/'file.csv'
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        DictWriter(stream, fieldnames=fieldnames)
    with raises(ValueError) as exception:
        import_csv(csv_filepath)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing file content.'


def test_import_csv_only_fieldnames_in_file(tmp_path):
    fieldnames = ['value', 'desc']
    csv_filepath = tmp_path/'file.csv'
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
    with raises(ValueError) as exception:
        import_csv(csv_filepath)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing file content.'


def test_export_csv_happy_path(tmp_path):
    csv_filepath = tmp_path/'file.csv'
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=1.0, desc='first expense')
    ]
    export_csv(str(csv_filepath), expenses)
    with open(csv_filepath, encoding='utf-8') as stream:
        reader = DictReader(stream)
        got = [row for row in reader]
    expect = [{'desc': 'first expense', 'dt': '12/03/2023', 'id_num': '1', 'value': '1.0'}]
    assert got == expect


def test_export_csv_no_extension_in_filepath(tmp_path):
    csv_filepath = tmp_path/'file'
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=1.0, desc='first expense')
    ]
    with raises(ValueError) as exception:
        export_csv(str(csv_filepath), expenses)
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing extension for new file.'


def test_generate_new_name_occurrency_2():
    db_filepath = 'directory/file.csv'
    occurrency = 2
    got = generate_new_name(db_filepath, occurrency)
    expect = 'directory/file(2).csv'
    assert got == expect


def test_generate_new_name_occurrency_3():
    db_filepath = 'directory/file.csv'
    occurrency = 3
    got = generate_new_name(db_filepath, occurrency)
    expect = 'directory/file(3).csv'
    assert got == expect


def test_add_db_exist(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=1.0, desc='first expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    value = '1.5'
    description = 'expense'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [
        UserExpense(id_num=1, dt='12/03/2023', value=1.0, desc='first expense'),
        UserExpense(id_num=2, dt=expect_dt, value=1.5, desc='expense')
    ]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_with_dt_db_exist(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', value=1.0, desc='first expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    value = '1.5'
    description = 'expense'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [
        UserExpense(id_num=1, dt='12/03/2023', value=1.0, desc='first expense'),
        UserExpense(id_num=2, dt='13/02/2024', value=1.5, desc='expense')
    ]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_empty_db_file(tmp_path):
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    value = '1.5'
    description = 'expense'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, dt=expect_dt, value=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_with_dt_empty_db_file(tmp_path):
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    value = '1.5'
    description = 'expense'
    dt = '01/02/2003'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, dt='01/02/2003', value=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_db_not_exist(tmp_path):
    value = '1.5'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, dt=expect_dt, value=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_with_dt_db_not_exist(tmp_path):
    value = '1.5'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, dt='13/02/2024', value=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_invalid_dt(tmp_path):
    value = '10'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = 'asd'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 1
    assert result.output.strip() == 'Invalid date format.'


def test_add_zero_value(tmp_path):
    value = '0'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'Error: The expense cannot be equal to zero.'
    

def test_add_negative_value(tmp_path):
    value = '-1'
    description = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', '--db-filepath', db_filepath, '--dt', dt, '--', value, description,])
    assert result.exit_code == 2
    assert result.output.strip() == 'Error: The expense cannot be negative.'


def test_add_empty_desc(tmp_path):
    value = '1'
    description = ''
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'Error: Missing name for new expense.'


def test_add_space_desc(tmp_path):
    value = '1'
    description = ' '
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'Error: Missing name for new expense.'


def test_add_tab_desc(tmp_path):
    value = '1'
    description = ' '
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'Error: Missing name for new expense.'


def test_add_new_line_desc(tmp_path):
    value = '1'
    description = '\n'
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 2
    assert result.output.strip() == 'Error: Missing name for new expense.'


def test_add_invalid_path():
    value = '10'
    description = 'expense'
    db_filepath = 'invalid_dir/file.db'
    dt = '13/02/2024'
    runner = CliRunner()
    result = runner.invoke(cli, ['add', value, description, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 3
    assert result.output.strip() == f'There is no such path: {db_filepath}.'


def test_report_db_filepath(tmp_path):
    expenses = [UserExpense(id_num=1, dt='13/11/1954', value=124.65, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~VALUE~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954    124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     124.65'


def test_report_db_filepath_show_big(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', value=499, desc='first expense'),
        UserExpense(id_num=2, dt='12/03/2023', value=500, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~VALUE~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954       499         first expense\n    2# 12/03/2023       500   [!]   second expense\n~~~~~~~~~~~~~~~~~\nTotal:     999.00'


def test_report_db_filepath_sort_default(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', value=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', value=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', value=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~VALUE~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954    124.65         first expense\n    2# 12/09/2021       300         second expense\n    3# 02/05/1999       499         third expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_default_descending(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', value=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', value=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', value=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--descending'])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~VALUE~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    3# 02/05/1999       499         third expense\n    2# 12/09/2021       300         second expense\n    1# 13/11/1954    124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_date(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', value=124.65, desc='first expense'),
        UserExpense(id_num=2, dt='12/09/2021', value=300, desc='second expense'),
        UserExpense(id_num=3, dt='02/05/1999', value=499, desc='third expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--sort', 'date',])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~VALUE~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954    124.65         first expense\n    3# 02/05/1999       499         third expense\n    2# 12/09/2021       300         second expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_date_descending(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', value=124.65, desc='first expense'),
        UserExpense(id_num=2, dt='12/09/2021', value=300, desc='second expense'),
        UserExpense(id_num=3, dt='02/05/1999', value=499, desc='third expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--sort', 'date', '--descending'])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~VALUE~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    2# 12/09/2021       300         second expense\n    3# 02/05/1999       499         third expense\n    1# 13/11/1954    124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_value(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', value=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', value=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', value=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--sort', 'value',])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~VALUE~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954    124.65         first expense\n    2# 12/09/2021       300         second expense\n    3# 02/05/1999       499         third expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_db_filepath_sort_value_descending(tmp_path):
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', value=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', value=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', value=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--sort', 'value', '--descending'])
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~VALUE~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    3# 02/05/1999       499         third expense\n    2# 12/09/2021       300         second expense\n    1# 13/11/1954    124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_show_python_code(tmp_path):
    expenses = [UserExpense(id_num=1, dt='12/03/2001', value=12, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath, '--python'])
    assert result.exit_code == 0
    assert result.output.strip() == '[UserExpense(id_num=1, dt=\'12/03/2001\', value=12, desc=\'first expense\')]'


def test_report_empty_db_file(tmp_path):
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 4
    assert result.output.strip() == 'No data has been entered yet.'


def test_report_db_file_not_exist():
    db_filepath = 'not_exist_file.db'
    runner = CliRunner()
    result = runner.invoke(cli, ['report', '--db-filepath', db_filepath])
    assert result.exit_code == 4
    assert result.output.strip() == 'No data has been entered yet.'


def test_import_from_with_content_expenses_empty(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, value=10, dt=expect_dt, desc='first expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'
    

def test_import_from_with_content_expenses_not_exist(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, value=10, dt=expect_dt, desc='first expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_import_from_with_content_user_dt(tmp_path):
    dt = '23.05.1984'
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath, '--dt', dt])
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, value=10, dt='23/05/1984', desc='first expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'
    

def test_import_from_csv_not_exist(tmp_path):
    csv_filepath = 'not_exist_file.csv'
    db_filepath = tmp_path/'file.db'
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 5
    assert result.output.strip() == 'File not exist.'


def test_import_from_only_fieldnames_in_csv(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 6
    assert result.output.strip() == 'Error: Missing file content.'


def test_import_from_empty_csv(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    stream = open(csv_filepath, 'x', encoding='utf-8')
    stream.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 6
    assert result.output.strip() == 'Error: Missing file content.'


def test_import_from_invalid_user_dt(tmp_path):
    dt = 'awd1'
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath, '--dt', dt])
    assert result.exit_code == 7
    assert result.output.strip() == 'Invalid date format.'


def test_import_from_0_value_in_csv(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 0, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 8
    assert result.output.strip() == 'Error: The expense cannot be equal to zero.'


def test_import_from_negative_value_in_csv(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': -1, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 8
    assert result.output.strip() == 'Error: The expense cannot be negative.'


def test_import_from_no_desc_in_csv(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 10, 'desc': ''})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 8
    assert result.output.strip() == 'Error: Missing name for new expense.'


def test_import_from_space_desc_in_csv(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 10, 'desc': ' '})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 8
    assert result.output.strip() == 'Error: Missing name for new expense.'


def test_import_from_tab_desc_in_csv(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 10, 'desc': ' '})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 8
    assert result.output.strip() == 'Error: Missing name for new expense.'


def test_import_from_new_line_desc_in_csv(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 10, 'desc': '\n'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 8
    assert result.output.strip() == 'Error: Missing name for new expense.'


def test_import_from_invalid_db_path(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = 'invalid_dir/file.db'
    fieldnames = ['value', 'desc']
    with open(csv_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'value': 10, 'desc': 'first expense'})
    runner = CliRunner()
    result = runner.invoke(cli, ['import-from', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 9
    assert result.output.strip() == f'There is no such path: {db_filepath}.'


def test_export_to(tmp_path):
    expenses = [UserExpense(id_num=1, dt='15/09/1857', value=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    with open(csv_filepath, encoding='utf-8') as stream:
        reader = DictReader(stream)
        restored = [row for row in reader]
    expect = [{'id_num': '1', 'dt': '15/09/1857', 'value': '567', 'desc': 'first expension'}]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved as: {csv_filepath}.'


def test_export_to_1_csv_filepath_already_exist(tmp_path):
    expenses = [UserExpense(id_num=1, dt='15/09/1857', value=567, desc='first expension')]
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
    expenses = [UserExpense(id_num=1, dt='15/09/1857', value=567, desc='first expension')]
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
    expenses = [UserExpense(id_num=1, dt='15/09/1857', value=567, desc='first expension')]
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


def test_export_to_db_file_not_exist(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = 'not_exist_file.db'
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 10
    assert result.output.strip() == 'No data has been entered yet, nothing to write.'


def test_export_to_empty_db_file(tmp_path):
    csv_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 10
    assert result.output.strip() == 'No data has been entered yet, nothing to write.'


def test_export_to_invalid_csv_filepath(tmp_path):
    expenses = [UserExpense(id_num=1, dt='15/09/1857', value=567, desc='first expension')]
    csv_filepath = 'invalid_dir/file.csv'
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 11
    assert result.output.strip() == f'There is no such path: {csv_filepath}.'


def test_export_to_missing_extension_in_csv_filepath(tmp_path):
    expenses = [UserExpense(id_num=1, dt='15/09/1857', value=567, desc='first expension')]
    csv_filepath = str(tmp_path/'file')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    runner = CliRunner()
    result = runner.invoke(cli, ['export-to', csv_filepath, '--db-filepath', db_filepath])
    assert result.exit_code == 12
    assert result.output.strip() == 'Error: Missing extension for new file.'