from common.config import Config
from common.hyperparams import HyperParams
from actors.llm import LLMAgent
from experiments.solve_with_chatbot import *
from tot.tot import TreeOfThought


if __name__ == "__main__":
    path_to_config_yaml = "./config.yaml"
    config = Config(path_to_config_yaml)
    llm_agent = LLMAgent(config)

    prob_description = '[["*", "3", "1"], ["*", "2", "3"], ["3", "*", "2"]]'
    
    # zsSolver = ZeroShotSudokuSolver(llm_agent)
    # zsSolver.solve(prob_description)
     
    # osCotSolver = OneShotCotSudokuSolver(llm_agent)
    # success, solution_rows = osCotSolver.solve(prob_description)

    # fsCotSolver = FewShotCotSudokuSolver(llm_agent)
    # success, solution_rows = fsCotSolver.solve()

    # print("Success :", success)
    # print("Solution:", solution_rows)

    tot = TreeOfThought(config)
    max_num_rounds = HyperParams.MaxNumConversationRounds
    user_input = 'Please solve Sudoku puzzle {}'.format(prob_description)
    tot.run(user_input, max_num_rounds)
