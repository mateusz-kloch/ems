from dataclasses import dataclass

from src.settings import BIG_EXPENSE_THRESHOLD


@dataclass
class UserExpense:
    id_num: int
    dt : str
    amount: float
    desc: str

    def __post_init__(self) -> ValueError:
        if self.amount == 0:
            raise ValueError('The expense amount cannot be zero.')
        if self.amount < 0:
            raise ValueError('The expense amount cannot be negative.')
        if not self.desc or self.desc.isspace():
            raise ValueError('Missing description for the expense.')
    
    def is_big(self) -> bool:
        return self.amount >= BIG_EXPENSE_THRESHOLD
    

if __name__ == '__main__':
    pass
