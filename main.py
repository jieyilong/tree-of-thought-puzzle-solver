from common.config import Config
from tot.tot import TreeOfThought

if __name__ == "__main__":
    path_to_config_yaml = "./config.yaml"
    config = Config(path_to_config_yaml)
    tot = TreeOfThought(config)

    user_input = "Please solve this Sudoku puzzle: [[1, *, *, 2], [*, 1, *, 4], [*, 2, *, *], [*, *, 4, *]]."
    max_num_rounds = 20
    tot.run(user_input, max_num_rounds)
    