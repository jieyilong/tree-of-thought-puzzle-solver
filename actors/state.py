import numpy as np

class StateManagerBase(object):

    def __init__(self) -> None:
        pass

    def update_state(self, state_update_instructions) -> bool:
        pass

    def get_current_state(self) -> object:
        return None
    
    def get_state(self, rollback_steps) -> object:
        return None
    
    def rollback(self, rollback_steps) -> object:
        pass


class SudokuStateManager(StateManagerBase):

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
        return self.get_state(0)
    
    def get_state(self, rollback_steps) -> object:
        if len(self.sudoku_matrix_history) <= rollback_steps:
            return None
        return self.sudoku_matrix_history[-(rollback_steps+1)]
    
    def rollback(self, rollback_steps) -> bool:
        if len(self.sudoku_matrix_history) == 0:
            return False
        for i in range(rollback_steps):
            self.sudoku_matrix_history.pop()
