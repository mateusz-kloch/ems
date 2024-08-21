import pytest

from src.models import UserExpense


def test_userexpense():
    """
    Test for UserExpense class.

    This test checks whether UserExpense object is created when values are correct.
    """
    expense = UserExpense(
        id_num=1,
        dt='19.07.2015',
        amount=15,
        desc='expense'
    )
    assert expense
    assert type(expense) == UserExpense


def test_userexpense_0_amount():
    """
    Test for UserExpense class.
    
    This test checks whether ValueError is raised when amount is 0.
    """
    with pytest.raises(ValueError) as exception:
        UserExpense(
            id_num=1,
            dt='12/01/1234',
            amount=0,
            desc='zero expense'
        )
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense amount cannot be zero.'


def test_userexpense_negative_amount():
    """
    Test for UserExpense class.

    This test checks whether ValueError is raised when amount is negative number.
    """
    with pytest.raises(ValueError) as exception:
        UserExpense(
            id_num=1,
            dt='23-10-1678',
            amount=-1,
            desc='negative expense'
        )
    assert exception.type == ValueError
    assert str(exception.value) == 'The expense amount cannot be negative.'


def test_userexpense_empty_desc():
    """
    Test for UserExpense class.

    This test checks whether ValueError is raised when desc is empty.
    """
    with pytest.raises(ValueError) as exception:
        UserExpense(
            id_num=1,
            dt='12/01/1234',
            amount=10,
            desc=''
        )
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_userexpense_space_desc():
    """
    Test for UserExpense class.

    This test checks whether ValueError is raised when desc is space only.
    """
    with pytest.raises(ValueError) as exception:
        UserExpense(
            id_num=1,
            dt='12/01/1234',
            amount=10,
            desc=' '
        )
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_userexpense_tab_desc():
    """
    Test for UserExpense class.

    This test checks whether ValueError is raised when desc is tab only.
    """
    with pytest.raises(ValueError) as exception:
        UserExpense(
            id_num=1,
            dt='12/01/1234',
            amount=10,
            desc='  '
        )
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_userexpense_newline_desc():
    """
    Test for UserExpense class.

    This test checks whether ValueError is raised when desc is new line mark only.
    """
    with pytest.raises(ValueError) as exception:
        UserExpense(
            id_num=1,
            dt='12/01/1234',
            amount=10,
            desc='\n'
        )
    assert exception.type == ValueError
    assert str(exception.value) == 'Missing description for the expense.'


def test_userexpense_isbig_true():
    """
    Test for UserExpense class.

    This test checks whether is_big() returns True when amount is grater or equal then `BIG_EXPENSE_THRESHOLD`,
    which is set in src/settings.py.
    """
    expense = UserExpense(
        id_num=1,
        dt='15-04-1923',
        amount=500,
        desc='expense'
    )
    assert expense.is_big() == True


def test_userexpense_isbig_false():
    """
    Test for UserExpense class.

    This test checks whether is_big() returns True when amount is smaller then `BIG_EXPENSE_THRESHOLD`,
    which is set in src/settings.py.
    """
    expense = UserExpense(
        id_num=1,
        dt='15-04-1923',
        amount=499,
        desc='expense'
    )
    assert expense.is_big() == False
