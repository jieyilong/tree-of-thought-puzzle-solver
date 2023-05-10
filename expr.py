from common.config import Config
from actors.llm import LLMAgent
from experiments.solve_with_chatbot import *

if __name__ == "__main__":
    path_to_config_yaml = "./config.yaml"
    config = Config(path_to_config_yaml)
    llm_agent = LLMAgent(config)
    
    # zsSolver = ZeroShotSudokuSolver(llm_agent)
    # zsSolver.solve('[["*", "3", "1"], ["*", "2", "3"], ["3", "*", "2"]]')
     
    # osCotSolver = OneShotCotSudokuSolver(llm_agent)
    # success, solution_rows = osCotSolver.solve('[["*", "3", "1"], ["*", "2", "3"], ["3", "*", "2"]]')

    fsCotSolver = FewShotCotSudokuSolver(llm_agent)
    success, solution_rows = fsCotSolver.solve('[["*", "3", "1"], ["*", "2", "3"], ["3", "*", "2"]]')

    print("Success :", success)
    print("Solution:", solution_rows)