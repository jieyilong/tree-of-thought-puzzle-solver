import numpy as np

class StateBase(object):

    def __init__(self) -> None:
        pass

    def update_state(self, state_update_instructions) -> bool:
        pass

    def get_current_state(self) -> object:
        return None
    
    def rollback(self, steps) -> object:
        pass

class SudokuState(StateBase):

    def __init__(self) -> None:
        super().__init__()
        self.sudoku_matrix_history = []

    def update_state(self, state_update_instructions) -> bool:
        success, board_matrix = self._extract_sudoku_board(state_update_instructions)
        if success:
            self.sudoku_matrix_history.append(board_matrix)

    def _extract_sudoku_board(self, state_update_instructions):
        return False, None # FIXME

    def get_current_state(self) -> object:
        if len(self.sudoku_matrix_history) == 0:
            return None
        return self.sudoku_matrix_history[-1]
    
    def rollback(self, steps) -> bool:
        if len(self.sudoku_matrix_history) == 0:
            return False
        for i in range(steps):
            self.sudoku_matrix_history.pop()
