from common.config import Config
from tot.tot import TreeOfThought

if __name__ == "__main__":
    path_to_config_yaml = "./config.yaml"
    config = Config(path_to_config_yaml)
    tot = TreeOfThought(config)

    # Solution: [[1, 4, 3, 2], [3, 1, 2, 4], [4, 2, 1, 3], [2, 3, 4, 1]]
    user_input = "Please solve this 4x4 Sudoku puzzle: [[1, *, *, 2], [*, 1, *, 4], [*, 2, *, *], [*, *, 4, *]]."
    
    #user_input = "Please solve this 3x3 Sudoku puzzle: [[1, *, *], [*, 1, *], [*, 2, *]]."
    
    max_num_rounds = 20
    tot.run(user_input, max_num_rounds)
