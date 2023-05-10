import common.utils as utils
from common.config import Config
from actors.checker import RuleBasedSudokuStateChecker
from actors.parser import LLMReplyParserForSudoku
from actors.llm import LLMAgent

class ChatBotBasedSudokuSolver(object):

    def __init__(self, llm_agent) -> None:
        self.llm_agent = llm_agent
        self.parser = LLMReplyParserForSudoku()

    def generate_prompt(self, init_board):
        role, msg_content = "user", self._generate_message_content(init_board)
        msgs = self.llm_agent.compose_messages([role], [msg_content])
        return msgs

    # sudoku_puzzle_instance_str should have the following format:
    #     [[*, 3, 1], [*, 2, 3], [3, *, 2]]
    def solve(self, sudoku_puzzle_instance_str):
        prompt = self.generate_prompt(sudoku_puzzle_instance_str)
        llm_reply = self.llm_agent.get_reply(prompt)

        success, solution = self.parser.parse_llm_reply(llm_reply)
        if not success:
            print("Failed to extract solution from the reply")
            return False, None
        
        success, json_obj = utils.extract_json_from_text_string('{{"rows": {} }}'.format(sudoku_puzzle_instance_str))
        if not success:
            return False, None
        success, init_board = self.parser.extract_sudoku_board(json_obj)
        if not success:
            raise "Invalid initial board: {}".format(sudoku_puzzle_instance_str)
        
        result = RuleBasedSudokuStateChecker.check_sudoku_board(init_board, solution)

        return result.is_valid, result.rows
        

class ZeroShotSudokuSolver(ChatBotBasedSudokuSolver):

    def _generate_message_content(self, sudoku_puzzle_instance) -> str:
        msg_tmpl = """Please solve this Sudoku puzzle {} where * represents a cell to be filled in. Please return your solution in the following JSON format: {{ "rows": [] }}."""
        msg_content = msg_tmpl.format(sudoku_puzzle_instance)
        return msg_content
    

class OneShotCotSudokuSolver(ChatBotBasedSudokuSolver):

    def _generate_message_content(self, sudoku_puzzle_instance) -> str:
        msg_tmpl = """Here is an example showing how to solve a 3x3 Sudoku puzzle [[*, 3, 1], [*, 2, 3], [3, *, 2]]. First, notice that the only missing number in the first row is 2, so we can fill in the first cell in the first row with 2.\n\n"""  + \
                   """Similarly, the first cell in the second row should be 2. Finally, the only missing number in the second column is 1. Hence, we can fill that cell with 1.""" + \
                   """In conclusion, the puzzle solution is [[2, 3, 1], [1, 2, 3], [3, 1, 2]].\n\n"""  + \
                   """Now, please solve this Sudoku puzzle {} where * represents a cell to be filled in. Please return your solution in the following JSON format: {{ "rows": [] }}."""
        msg_content = msg_tmpl.format(sudoku_puzzle_instance)
        return msg_content
    

class FewShotCotSudokuSolver(ChatBotBasedSudokuSolver):

    def _generate_message_content(self, sudoku_puzzle_instance) -> str:
        msg_tmpl = """Here is an example showing how to solve a 3x3 Sudoku puzzle [[*, 3, 1], [*, 2, 3], [3, *, 2]]. First, notice that the only missing number in the first row is 2, so we can fill in the first cell in the first row with 2.\n\n"""  + \
                   """Similarly, the first cell in the second row should be 2. Finally, the only missing number in the second column is 1. Hence, we can fill that cell with 1.""" + \
                   """In conclusion, the puzzle solution is [[2, 3, 1], [1, 2, 3], [3, 1, 2]].\n\n"""  + \
                   """Here is another example showing how to solve Sudoku puzzle [[1, *, *], [*, 1, *], [*, 2, *]]. First, notice that the second column already has 1 and 2, so the first cell in the second row needs to be 3.""" + \
                   """After this step, the first row has 1 and 3. Hence the last cell in the first row must be 2. Now, look at the cell at the intersection of the second row and the third column. It must be 3.""" + \
                   """As a result, the cell at the intersection of the third row and the third column must be 1. The remaining cells are now easy to fill in.""" + \
                   """In conclusion, the puzzle solution is [[1, 3, 2], [2, 1, 3], [3, 2, 1]].\n\n"""  + \
                   """Now, please solve this Sudoku puzzle {} where * represents a cell to be filled in. Please return your solution in the following JSON format: {{ "rows": [] }}.""" 
        msg_content = msg_tmpl.format(sudoku_puzzle_instance)
        return msg_content
