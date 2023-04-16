

class StateBase(object):

    def __init__(self) -> None:
        pass


class SudokuState(StateBase):

    def __init__(self, size) -> None:
        super().__init__()
        self.sudoku_matrix_history = []

    def update_state(self, state_update_instructions) -> None:
        pass

    def get_state_history(self, steps_back) -> object:
        pass
