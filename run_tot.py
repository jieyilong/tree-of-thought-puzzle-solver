import sys
from common.config import Config
from tot.tot import TreeOfThought

#
# Example Sudoku problems:
# '[[*, 3, 1], [*, 2, 3], [3, *, 2]]'
# '[[1, *, *, 2], [*, 1, *, 4], [*, 2, *, *], [*, *, 4, *]]'
#
if __name__ == "__main__":
    if not len(sys.argv) == 2:
        print("""Usage:""")
        print("""    python run_tot.py "<problem_description>" """)
        print("""Example:""")
        print("""    python run_tot.py "please solve this 3x3 sudoku puzzle [[*, 3, 1], [*, 2, 3], [3, *, 2]] where * represents a cell to be filled in." """)
        print("""    python run_tot.py "please solve this 4x4 sudoku puzzle [[*,1,*,*],[*,*,2,*],[*,*,*,4],[1,*,*,*]] where * represents a cell to be filled in." """)
        exit(1)
    
    user_input = sys.argv[1]
    path_to_config_yaml = "./config.yaml"
    config = Config(path_to_config_yaml)
    tot = TreeOfThought(config)

    success, solution = tot.run(user_input)
    print("")
    print("Success :", success)
    print("Solution:", solution)
