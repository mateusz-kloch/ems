"""
This script serves as a toolkit for run.py tests.
All args for a given function are the same as for the command it inits.
"""
from click.testing import CliRunner

from src.run import cli


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
