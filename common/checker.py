
class StateCheckerBase(object):

    def __init__(self, state) -> None:
        self.state = state

    def check_current_state(self) -> bool:
        return False


class SudokuStateChecker(StateCheckerBase):

    def __init__(self, state) -> None:
        super().__init__(state)

    def check_current_state(self) -> bool:
        current_board = self.state.get_current_board()

        # Check constraint 1: the current board should not conflict with the initial board configuration


        # Check constraint 2: the board must be filled with numbers from 1-n with no repeated numbers in each line, horizontally or vertically.
        
    
