from common.hyperparams import HyperParams
from common.config import Config
from tot.tot import TreeOfThought

if __name__ == "__main__":
    path_to_config_yaml = "./config.yaml"
    config = Config(path_to_config_yaml)
    tot = TreeOfThought(config)

    # Solution: [[1, 4, 3, 2], [3, 1, 2, 4], [4, 2, 1, 3], [2, 3, 4, 1]]
    #user_input = "Please solve this 4x4 Sudoku puzzle: [[1, *, *, 2], [*, 1, *, 4], [*, 2, *, *], [*, *, 4, *]]."
    
    #user_input = "please solve this 4x4 sudoku puzzle [[3,*,*,2],[1,*,3,*],[*,1,*,3],[4,*,*,1]]."

    # GOOD TEST CASE: even the ChatGPT web cannot solve these
    #user_input = "please solve this 5x5 sudoku puzzle [[*,1,*,*,*],[*,*,3,*,2],[*,*,*,3,*],[*,4,*,1,*],[*,*,1,*,*]] where * meaning an empty cell to be filled in."
   
    # GOOD TEST CASE: Each row/column of this puzzle has 3-4 unknowns, which seems to be a sweetspot for ToT vs. ChatGPT
    #user_input = "please solve this 5x5 sudoku puzzle [[*,1,*,5,4],[1,*,3,*,2],[5,2,*,3,*],[*,4,*,1,*],[4,*,1,*,5]] where * meaning an empty cell to be filled in."
    user_input = "please solve this 5x5 sudoku puzzle [[*,2,*,*,4],[*,*,3,*,1],[*,1,*,3,*],[*,4,*,2,*],[*,*,2,*,*]] where * meaning an empty cell to be filled in."

    #user_input = "please solve this 4x4 sudoku puzzle [[*,1,*,*],[*,*,2,*],[*,*,*,4],[1,*,*,*]]."
    #user_input = "please solve this 4x4 sudoku puzzle [[2,1,*,*],[*,*,3,*],[*,*,*,4],[4,*,*,*]], where * meaning an empty cell to be filled in."
    
    #user_input = "Please solve this 9x9 Sudoku puzzle: [[1, *, *, 2, *, *, *, 9, *], [*, *, 5, *, *, 6, *, *, *], [*, 4, *, 1, *, *, *, *, *], [*, *, 3, *, 5, *, *, *, *], [*, *, *, *, 1, 2, *, *, *], [*, *, *, *, *, *, *, *, *], [*, *, *, *, *, *, *, 8, *], [*, *, *, *, *, 8, *, *, *], [*, *, *, *, *, 7, *, *, *]]."
    #user_input = "Please solve this 9x9 Sudoku puzzle: [[4,2,*,9,*,3,8,*,6],[9,1,*,*,8,*,2,*,4],[6,*,3,*,5,*,*,*,9],[*,7,1,*,4,*,6,9,*],[3,*,9,*,2,6,*,8,5],[*,*,*,*,9,*,3,*,*],[*,9,*,*,6,*,4,*,*],[1,*,*,*,*,9,5,*,*],[7,*,4,5,*,8,*,*,*]]."
    #user_input = "Please solve this 3x3 Sudoku puzzle: [[1, *, *], [*, 1, *], [*, 2, *]]."
    
    max_num_rounds = HyperParams.MaxNumConversationRounds
    tot.run(user_input, max_num_rounds)
