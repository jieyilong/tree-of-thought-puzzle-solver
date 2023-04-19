import json

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

    def update_state(self, solution) -> bool:
        solution_key = json.dumps(solution.tolist())
        for state in self.sudoku_matrix_history:
            state_key = json.dumps(state.tolist())
            if solution_key == state_key: # duplicate detected
                return False

        self.sudoku_matrix_history.append(solution)
        return True

    def get_current_state(self) -> object:
        return self.get_state(0)
    
    def is_at_initial_state(self) -> bool:
        return len(self.sudoku_matrix_history) == 1
    
    def get_initial_state(self) -> object:
        history_len = len(self.sudoku_matrix_history)
        if history_len == 0:
            return None
        return self.get_state(history_len-1)
        
    def get_state(self, rollback_steps) -> object:
        if len(self.sudoku_matrix_history) <= rollback_steps:
            return None
        return self.sudoku_matrix_history[-(rollback_steps+1)]
    
    def rollback(self, rollback_steps) -> bool:
        if len(self.sudoku_matrix_history) == 0:
            return False
        
        print("START STATE ROLLBACK, current depth: {}".format(len(self.sudoku_matrix_history)))
        for state in self.sudoku_matrix_history:
            print("State:", json.dumps(state.tolist()))

        for i in range(rollback_steps):
            self.sudoku_matrix_history.pop()
        print("STATE ROLLBACK DONE,  current depth: {}\n".format(len(self.sudoku_matrix_history)))

    def max_rollback_steps(self) -> int:
        return len(self.sudoku_matrix_history) - 1