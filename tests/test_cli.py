from csv import DictReader, DictWriter
from pickle import load, dump
from datetime import date

from click.testing import CliRunner

from src.cli import cli
from src.models import UserExpense


def init_add(amount, desc, db_filepath, dt):
    """
    A function that initiates the "add" command in the test environment.
    
    Usage:
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    """
    return CliRunner().invoke(cli, ['add', '--db-filepath', db_filepath, '--dt', dt, '--', amount, desc])


def init_report(db_filepath, sort, descending, python):
    """
    A function that initiates the "report" command in the test environment.

    Usage:
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    """
    args = ['report', '--db-filepath', db_filepath, '--sort', sort]
    if descending == True:
        args.append('--descending')
    if python == True:
        args.append('--python')
    return CliRunner().invoke(cli, args)


def init_edit(id_num, db_filepath, dt, amount, desc):
    """
    A function that initiates the "edit" command in the test environment.

    Usage:
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    """
    return CliRunner().invoke(cli, ['edit', id_num, '--db-filepath', db_filepath, '--dt', dt, '--amount', amount, '--desc', desc])


def init_import_from(external_filepath, db_filepath, dt):
    """
    A function that initiates the "import-from" command in the test environment.

    Usage:
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    """
    return CliRunner().invoke(cli, ['import-from', external_filepath, '--db-filepath', db_filepath, '--dt', dt])


def init_export_to(external_filepath, db_filepath):
    """
    A function that initiates the "export-to" command in the test environment.

    Usage:
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    """
    return CliRunner().invoke(cli, ['export-to', external_filepath, '--db-filepath', db_filepath])


def test_add_db_exist(tmp_path):
    """
    Test for "add" subcommand.

    This test verifies that "add" correctly writes the new expense to the existing expenses in the database file.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=1.0, desc='first expense')
    ]
    db_filepath = tmp_path/'file.db'
    amount = '1.5'
    desc = 'expense'
    dt = None
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
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
    Test for "add" subcommand.

    This test verifies that "add" correctly writes the new expense with the given date to the existing database file.
    """
    expenses = [
        UserExpense(id_num=1, dt='12/03/2023', amount=1.0, desc='first expense')
    ]
    db_filepath = tmp_path/'file.db'
    amount = '1.5'
    desc = 'expense'
    dt = '13/02/2024'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
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
    Test for "add" subcommand.

    This test verifies that "add" correctly writes the new expense to an existing empty database file.
    """
    db_filepath = tmp_path/'file.db'
    amount = '1.5'
    desc = 'expense'
    dt = None
    db_file = open(db_filepath, 'wb')
    db_file.close()
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, dt=expect_dt, amount=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_with_dt_empty_db_file(tmp_path):
    """
    Test for "add" subcommand.

    This test verifies that "add" correctly writes the new expense with the given date to an existing empty database file.
    """
    db_filepath = tmp_path/'file.db'
    amount = '1.5'
    desc = 'expense'
    dt = '01/02/2003'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, dt='01/02/2003', amount=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_db_not_exist(tmp_path):
    """
    Test for "add" subcommand.

    This test verifies that "add" correctly creates the database file and writes the new expense to it.
    """
    amount = '1.5'
    desc = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, dt=expect_dt, amount=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_with_dt_db_not_exist(tmp_path):
    """
    Test for "add" subcommand.

    This test verifies that "add" correctly creates a database file and writes a new expense to it with the given date.
    """
    amount = '1.5'
    desc = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = '13/02/2024'
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, dt='13/02/2024', amount=1.5, desc='expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_add_db_filepath_missing_extension(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when the database file extension is missing.
    """
    db_filepath = str(tmp_path/'file')
    amount = '1'
    desc = 'expense'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_add_db_filepath_another_missing_extension(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when the database file extension is missing.
    """
    db_filepath = str(tmp_path/'file.')
    amount = '1'
    desc = 'expense'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_add_db_filepath_unsupported_extension(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when the database file extension is not supported.
    """
    db_filepath = str(tmp_path/'file.txt')
    amount = '1'
    desc = 'expense'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_add_invalid_dt(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when an invalid date format is provided.
    """
    amount = '10'
    desc = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = 'asd'
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Invalid date format.'


def test_add_zero_amount(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when a zero expense amount is provided.
    """
    amount = '0'
    desc = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: The expense amount cannot be zero.'
    

def test_add_negative_amount(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when a negative expense amount is provided.
    """
    amount = '-1'
    desc = 'expense'
    db_filepath = tmp_path/'file.db'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: The expense amount cannot be negative.'


def test_add_empty_desc(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when no expense description is provided.
    """
    amount = '1'
    desc = ''
    db_filepath = tmp_path/'file.db'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_add_space_desc(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when an expense description containing only a space is provided.
    """
    amount = '1'
    desc = ' '
    db_filepath = tmp_path/'file.db'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_add_tab_desc(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when an expense description containing only a tab is provided.
    """
    amount = '1'
    desc = ' '
    db_filepath = tmp_path/'file.db'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_add_newline_desc(tmp_path):
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when an expense description containing only a new line tag is provided.
    """
    amount = '1'
    desc = '\n'
    db_filepath = tmp_path/'file.db'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_add_invalid_path():
    """
    Test for "add" subcommand.

    This test checks whether "add" correctly handles an exception when an invalid database path is specified.
    """
    amount = '10'
    desc = 'expense'
    db_filepath = 'invalid_dir/file.db'
    dt = None
    result = init_add(amount=amount, desc=desc, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 3
    assert result.output.strip() == f'ERROR: There is no such path: {db_filepath}.'


def test_report(tmp_path):
    """
    Test for "report" subcommand.

    This test verifies that "report" correctly displays the expense from the database file.
    """
    expenses = [UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    sort = None
    descending = False
    python = False
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     124.65'


def test_report_show_big(tmp_path):
    """
    Test for "report" subcommand.

    This test verifies that "report" correctly tags an expense as big with a "[!]" if the threshold has been reached.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=499, desc='first expense'),
        UserExpense(id_num=2, dt='12/03/2023', amount=500, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    sort = None
    descending = False
    python = False
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     499.00         first expense\n    2# 12/03/2023     500.00   [!]   second expense\n~~~~~~~~~~~~~~~~~\nTotal:     999.00'


def test_report_sort_default(tmp_path):
    """
    Test for "report" subcommand.

    This test verifies that "report" correctly sorts expenses using the default method.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    sort = None
    descending = False
    python = False
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     124.65         first expense\n    2# 12/09/2021     300.00         second expense\n    3# 02/05/1999     499.00         third expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_sort_default_descending(tmp_path):
    """
    Test for "report" subcommand.

    This test verifies that "report" correctly sorts expenses using the default method in descending order.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    sort = None
    descending = True
    python = False
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    3# 02/05/1999     499.00         third expense\n    2# 12/09/2021     300.00         second expense\n    1# 13/11/1954     124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_sort_date(tmp_path):
    """
    Test for "report" subcommand.

    This test verifies that "report" correctly sorts expenses using the "date" method.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense')
    ]
    db_filepath = tmp_path/'file.db'
    sort = 'date'
    descending = False
    python = False
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     124.65         first expense\n    3# 02/05/1999     499.00         third expense\n    2# 12/09/2021     300.00         second expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_sort_date_descending(tmp_path):
    """
    Test for "report" subcommand.

    This test verifies that "report" correctly sorts expenses using the "date" method in descending order.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense')
    ]
    db_filepath = tmp_path/'file.db'
    sort = 'date'
    descending = True
    python = False
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    2# 12/09/2021     300.00         second expense\n    3# 02/05/1999     499.00         third expense\n    1# 13/11/1954     124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_sort_amount(tmp_path):
    """
    Test for "report" subcommand.

    This test verifies that "report" correctly sorts expenses using the "amount" method.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    sort = 'amount'
    descending = False
    python = False
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    1# 13/11/1954     124.65         first expense\n    2# 12/09/2021     300.00         second expense\n    3# 02/05/1999     499.00         third expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_sort_amount_descending(tmp_path):
    """
    Test for "report" subcommand.

    This test verifies that "report" correctly sorts expenses using the "amount" method in descending order.
    """
    expenses = [
        UserExpense(id_num=1, dt='13/11/1954', amount=124.65, desc='first expense'),
        UserExpense(id_num=3, dt='02/05/1999', amount=499, desc='third expense'),
        UserExpense(id_num=2, dt='12/09/2021', amount=300, desc='second expense')
    ]
    db_filepath = tmp_path/'file.db'
    sort = 'amount'
    descending = True
    python = False
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 0
    assert result.output.strip() == '~~ID~~ ~~~DATE~~~ ~~AMOUNT~~ ~~BIG~~ ~~~DESCRIPTION~~~\n~~~~~~ ~~~~~~~~~~ ~~~~~~~~~~ ~~~~~~~ ~~~~~~~~~~~~~~~~~\n    3# 02/05/1999     499.00         third expense\n    2# 12/09/2021     300.00         second expense\n    1# 13/11/1954     124.65         first expense\n~~~~~~~~~~~~~~~~~\nTotal:     923.65'


def test_report_python_code(tmp_path):
    """
    Test for "report" subcommand.

    This test checks whether "report" displays expenses as a representation of Python code.
    """
    expenses = [UserExpense(id_num=1, dt='12/03/2001', amount=12, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    sort = None
    descending = False
    python = True
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 0
    assert result.output.strip() == '[UserExpense(id_num=1, dt=\'12/03/2001\', amount=12, desc=\'first expense\')]'


def test_report_db_file_not_exist():
    """
    Test for "report" subcommand.

    This test checks whether "report" correctly handles an exception when the database does not exist.
    """
    db_filepath = 'not_exist_file.db'
    sort = None
    descending = False
    python = False
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 3
    assert result.output.strip() == f'ERROR: There is no such path: {db_filepath}.'


def test_report_db_filepath_missing_extension(tmp_path):
    """
    Test for "report" subcommand.

    This test checks whether "report" correctly handles an exception when the database file extension is missing.
    """
    db_filepath = str(tmp_path/'file')
    sort = None
    descending = False
    python = False
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_report_db_filepath_another_missing_extension(tmp_path):
    """
    Test for "report" subcommand.

    This test checks whether "report" correctly handles an exception when the database file extension is missing.
    """
    db_filepath = str(tmp_path/'file.')
    sort = None
    descending = False
    python = False
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_report_db_filepath_unsupported_extension(tmp_path):
    """
    Test for "report" subcommand.

    This test checks whether "report" correctly handles an exception when the database file extension is not supported.
    """
    db_filepath = str(tmp_path/'file.txt')
    sort = None
    descending = False
    python = False
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_report_empty_db_file(tmp_path):
    """
    Test for "report" subcommand.

    This test checks whether "report" correctly handles an exception when the database file is empty.
    """
    db_filepath = tmp_path/'file.db'
    sort = None
    descending = False
    python = False
    db_file = open(db_filepath, 'wb')
    db_file.close()
    result = init_report(db_filepath=db_filepath, sort=sort, descending=descending, python=python)
    assert result.exit_code == 4
    assert result.output.strip() == 'ERROR: No data has been entered yet, nothing to display.'


def test_edit(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly edits expenses in the database file.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, dt='20/12/2022', amount=150.0, desc='edited expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_edit_no_atributes(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when no values have been passed to change.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = None
    amount = None
    desc = None
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: No values have been passed.'


def test_edit_invalid_date(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when an invalid date has passed.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = 'date'
    amount = '150'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Invalid date format.'


def test_edit_database_not_exists():
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when the database file does not exist.
    """
    db_filepath = 'not_exist_file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 3
    assert result.output.strip() == f'ERROR: There is no such path: {db_filepath}.'


def test_edit_db_filepath_missing_extension(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when the database file extension is missing.
    """
    db_filepath = str(tmp_path/'file')
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_edit_db_filepath_another_missing_extension(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when the database file extension is missing.
    """
    db_filepath = str(tmp_path/'file.')
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_edit_db_filepath_unsupported_extension(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when the database file extension is not supported.
    """
    db_filepath = str(tmp_path/'file.txt')
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_edit_empty_database(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when the database file is empty.
    """
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 4
    assert result.output.strip() == 'ERROR: No data has been entered yet, nothing to edit.'


def test_edit_invalid_id_num(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when the database file does not contain the ID selected for editing.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '2'
    dt = '20/12/2022'
    amount = '150'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 2
    assert result.output.strip() == f'ERROR: ID {id_num}# not exists in database.'


def test_edit_0_amount(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when a zero expense amount is provided.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '0'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: The expense amount cannot be zero.'


def test_edit_negative_amount(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when a negative expense amount is provided.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '-1'
    desc = 'edited expense'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: The expense amount cannot be negative.'


def test_edit_empty_desc(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when a empty expense description is provided.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = ''
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_edit_space_desc(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when an expense description containing only a space is provided.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = ' '
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_edit_tab_desc(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when an expense description containing only a tab is provided.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = '    '
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_edit_newline_desc(tmp_path):
    """
    Test for "edit" subcommand.

    This test checks whether "edit" correctly handles an exception when an expense description containing only a new line tag is provided.
    """
    expenses = [UserExpense(id_num=1, dt='13/03/2013', amount=50.0, desc='first expense')]
    db_filepath = tmp_path/'file.db'
    id_num = '1'
    dt = '20/12/2022'
    amount = '150'
    desc = '\n'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_edit(id_num=id_num, db_filepath=db_filepath, dt=dt, amount=amount, desc=desc)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_with_content_expenses_empty(tmp_path):
    """
    Test for "import-from" subcommand.

    This test verifies that "import-from" correctly writes expenses from a file to a database file that contains other expenses.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt=None
    db_file = open(db_filepath, 'wb')
    db_file.close()
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, amount=10, dt=expect_dt, desc='first expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'
    

def test_import_from_with_content_expenses_not_exist(tmp_path):
    """
    Test for "import-from" subcommand.

    This test verifies that "import-from" correctly creates a database file and writes expenses from the file to it.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt=None
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect_dt = date.today().strftime('%d/%m/%Y')
    expect = [UserExpense(id_num=1, amount=10, dt=expect_dt, desc='first expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_import_from_with_content_user_dt(tmp_path):
    """
    Test for "import-from" subcommand.

    This test verifies that "import-from" correctly writes expenses from the file with the given date to the database file.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = '23.05.1984'
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    with open(db_filepath, 'rb') as stream:
        restored = load(stream)
    expect = [UserExpense(id_num=1, amount=10, dt='23/05/1984', desc='first expense')]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved to: {db_filepath}.'


def test_import_from_missing_extension_in_external_filepath(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the imported file has no extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file')
    db_filepath = tmp_path/'file.db'
    dt = None
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_another_missing_extension_in_external_filepath(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the imported file has an invalid extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.')
    db_filepath = tmp_path/'file.db'
    dt = None
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_unsupported_extension_in_external_filepath(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the imported file has an invalid extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.txt')
    db_filepath = tmp_path/'file.db'
    dt = None
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_missing_extension_in_db_filepath(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the database file extension is missing.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file'
    dt = None
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_another_missing_extension_in_db_filepath(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the database file extension is missing.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.'
    dt = None
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_unsupported_extension_in_db_filepath(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the database file extension is not supported.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.txt'
    dt = None
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_import_from_csv_not_exist(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the imported file does not exist.
    """
    external_filepath = 'not_exist_file.csv'
    db_filepath = tmp_path/'file.db'
    dt = None
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 3
    assert result.output.strip() == 'ERROR: File not exist.'


def test_import_from_only_headers_in_csv(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the imported file contains only headers.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = None
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing file content.'


def test_import_from_empty_csv(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the imported file is empty.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = None
    stream = open(external_filepath, 'x', encoding='utf-8')
    stream.close()
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing file content.'


def test_import_from_invalid_headers_in_csv(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the imported file contains invalid headers.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = None
    headers = ['inv_amount', 'inv_desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'inv_amount': 10, 'inv_desc': 'first expense'})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 5
    assert result.output.strip() == f'ERROR: Invalid headers in {external_filepath}.'


def test_import_from_invalid_user_dt(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when an invalid date format is provided.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = 'awd1'
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Invalid date format.'


def test_import_from_0_amount_in_csv(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when one of the imported amounts is 0.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = None
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 0, 'desc': 'first expense'})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: The expense amount cannot be zero.'


def test_import_from_negative_amount_in_csv(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when one of the imported amounts is negative.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = None
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': -1, 'desc': 'first expense'})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: The expense amount cannot be negative.'


def test_import_from_no_desc_in_csv(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when one of the imported descriptions is empty.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = None
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': ''})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_space_desc_in_csv(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when one of the imported descriptions contains only a space.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = None
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': ' '})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_tab_desc_in_csv(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when one of the imported descriptions contains only a tab.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = None
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': ' '})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_newline_desc_in_csv(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when one of the imported descriptions contains only a newline tag.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    dt = None
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': '\n'})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 2
    assert result.output.strip() == 'ERROR: Missing description for the expense.'


def test_import_from_invalid_db_path(tmp_path):
    """
    Test for "import-from" subcommand.

    This test checks whether "import-from" correctly handles an exception when the database file path is invalid.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = 'invalid_dir/file.db'
    dt = None
    headers = ['amount', 'desc']
    with open(external_filepath, 'x', encoding='utf-8') as stream:
        writer = DictWriter(stream, fieldnames=headers)
        writer.writeheader()
        writer.writerow({'amount': 10, 'desc': 'first expense'})
    result = init_import_from(external_filepath=external_filepath, db_filepath=db_filepath, dt=dt)
    assert result.exit_code == 3
    assert result.output.strip() == f'ERROR: There is no such path: {db_filepath}.'


def test_export_to(tmp_path):
    """
    Test for "export-to" subcommand.

    This test verifies that "export-to" correctly writes expenses from the database file to the external file.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    with open(external_filepath, encoding='utf-8') as stream:
        reader = DictReader(stream)
        restored = [row for row in reader]
    expect = [{'id_num': '1', 'dt': '15/09/1857', 'amount': '567', 'desc': 'first expension'}]
    assert restored == expect
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved as: {external_filepath}.'


def test_export_to_1_external_filepath_already_exist(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly generates a new name for an external file if a file with the same name already exists.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    csv_file = open(external_filepath, 'x')
    csv_file.close()
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    expect_external_filepath = str(tmp_path/'file(2).csv')
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved as: {expect_external_filepath}.'


def test_export_to_1_2_external_filepath_already_exists(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly generates a new names for an external file if a files with the same name already exists.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.csv')
    another_external_filepath = str(tmp_path/'file(2).csv')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    csv_file = open(external_filepath, 'x')
    csv_file.close()
    another_csv_file = open(another_external_filepath, 'x')
    another_csv_file.close()
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    expect_external_filepath = str(tmp_path/'file(3).csv')
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved as: {expect_external_filepath}.'


def test_export_to_2_external_filepath_already_exist(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks that "export-to" correctly ignores a previously generated name if a name for the external file is not already in use.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    first_external_filepath = str(tmp_path/'file.csv')
    second_external_filepath = str(tmp_path/'file(2).csv')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    csv_file = open(second_external_filepath, 'x')
    csv_file.close()
    result = init_export_to(external_filepath=first_external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 0
    assert result.output.strip() == f'Saved as: {first_external_filepath}.'


def test_export_to_missing_extension_in_external_filepath(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly handles an exception when the external file does not have an extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_another_missing_extension_in_external_filepath(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly handles an exception when an external file has an invalid extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_unsupported_extension_in_external_filepath(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly handles an exception when an external file has an invalid extension.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.txt')
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_db_file_not_exist(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly handles an exception when the database file does not exist.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = 'not_exist_file.db'
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 3
    assert result.output.strip() == f'ERROR: There is no such path: {db_filepath}.'


def test_export_to_missing_extension_in_db_filepath(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly handles an exception when the database file extension is missing.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_another_missing_extension_in_db_filepath(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly handles an exception when the database file extension is missing.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_unsupported_extension_in_db_filepath(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly handles an exception when the database file extension is unsupported.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.txt'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 1
    assert result.output.strip() == 'ERROR: Missing extension for file or unsupported file type.'


def test_export_to_empty_db_file(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly handles an exception when the database file is empty.
    """
    external_filepath = str(tmp_path/'file.csv')
    db_filepath = tmp_path/'file.db'
    db_file = open(db_filepath, 'wb')
    db_file.close()
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 4
    assert result.output.strip() == 'ERROR: No data has been entered yet, nothing to write.'


def test_export_to_invalid_external_filepath(tmp_path):
    """
    Test for "export-to" subcommand.

    This test checks whether "export-to" correctly handles an exception when the path to an external file is invalid.
    """
    expenses = [UserExpense(id_num=1, dt='15/09/1857', amount=567, desc='first expension')]
    external_filepath = 'invalid_dir/file.csv'
    db_filepath = tmp_path/'file.db'
    with open(db_filepath, 'wb') as stream:
        dump(expenses, stream)
    result = init_export_to(external_filepath=external_filepath, db_filepath=db_filepath)
    assert result.exit_code == 3
    assert result.output.strip() == f'ERROR: There is no such path: {external_filepath}.'
