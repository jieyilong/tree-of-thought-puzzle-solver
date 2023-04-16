
class StateCheckerBase(object):

    def __init__(self) -> None:
        pass

    def check_state(self, state) -> bool:
        return False


class SudokuStateChecker(StateCheckerBase):

    def __init__(self) -> None:
        super().__init__()

    def check_state(self, sudoku_state) -> bool:
        return False
    
    