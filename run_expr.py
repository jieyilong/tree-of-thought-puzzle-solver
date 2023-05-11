import sys
import json
from common.config import Config
from common.hyperparams import HyperParams
from common.enums import SolverType
from actors.llm import LLMAgent
from experiments.chatbot_based_solvers import *
from tot.tot import TreeOfThought

def load_problem_set(path_to_problem_set_json_file):
    f = open(path_to_problem_set_json_file)
    problem_set = json.load(f)
    return problem_set


if __name__ == "__main__":
    if not len(sys.argv) == 3:
        print("""Usage:""")
        print("""    python run_expr.py <solver_type> <path/to/problem/set/json>""")
        print("""    solver_type: zero_shot, one_shot_with_cot, few_shot_with_cot, tot""")
        print("""Example:""")
        print("""    python run_expr.py tot data/benchmarks/sudoku/3x3_sudoku_puzzles.json""")
        exit(1)
    
    solver_type = SolverType(sys.argv[1])
    path_to_problem_set_json = sys.argv[2]
    problem_set = load_problem_set(path_to_problem_set_json)

    path_to_config_yaml = "./config.yaml"
    config = Config(path_to_config_yaml)
    llm_agent = LLMAgent(config)

    num_problems = len(problem_set)
    num_solved_problems = 0
    for problem in problem_set:
        print("---------------------------------------------------------------------------")

        if solver_type == SolverType.ZeroShot:
            solver = ZeroShotSudokuSolver(llm_agent)
            problem_description = problem
        elif solver_type == SolverType.OneShotWithCoT:
            solver = OneShotCotSudokuSolver(llm_agent)
            problem_description = problem
        elif solver_type == SolverType.FewShotWithCoT:
            solver = FewShotCotSudokuSolver(llm_agent)
            problem_description = problem
        elif solver_type == SolverType.ToT:
            solver = TreeOfThought(config)
            problem_description = "Please solve this Sudoku puzzle: {}".format(problem)
        else:
            raise "Solver type {} not supported yet.".format(solver_type)
        
        success, solution = solver.run(problem_description)
        if success:
            num_solved_problems += 1

        print("Success :", success)
        print("Solution:", solution)
        print("---------------------------------------------------------------------------")
        print("")
    
    print("Total number of  problems:", num_problems)
    print("Number of solved problems:", num_solved_problems)

