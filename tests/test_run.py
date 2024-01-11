from pickle import load, dump

from run import MyExpense, read_db


def test_read_db(tmp_path):
    sample = MyExpense(
        id_num = 1,
        dt = '01.02.2023',
        value = 1.0,
        desc = 'first sample'
    )
    tmp_file = tmp_path/'tmp_file'
    with open(tmp_file, 'wb') as stream:
        dump(sample, stream)
    restored = read_db(tmp_file)
    assert sample == restored