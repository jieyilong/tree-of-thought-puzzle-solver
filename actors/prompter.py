import json
import random
from actors.state import *
from actors.checker import *
from common.enums import PromptGenType


class PrompterBase(object):

    def __init__(self) -> None:
        pass

    def generate_initial_prompt(self) -> str:
        return ""
    
    def generate_prompt(self) -> str:
        return ""


class SudokuPrompter(PrompterBase):

    def __init__(self, llm_agent, state_manager, max_llm_context_length, include_chat_history_in_query, prompt_generation_type: PromptGenType) -> None:
        super().__init__()
        self.prompt_msg_buffer = ""
        self.llm_agent = llm_agent
        self.state_manager = state_manager
        self.max_llm_context_length = max_llm_context_length
        self.include_chat_history_in_query = include_chat_history_in_query
        self.prompt_generation_type = prompt_generation_type

    def generate_initial_prompt(self, user_input) -> str:
        msg_tmpl = """{} Before solving this Sudoku puzzle, please return its initial board configuration in the following JSON format: {{ "rows": [] }}. Please use "*" to represent the missing values. Do not provide a solution yet.""" # FIXME
        role, msg_content = "user", msg_tmpl.format(user_input)
        msgs = self.llm_agent.compose_messages([role], [msg_content])
        return msgs
    
    def generate_prompt(self, conversation_history, rollback_steps):
        if self.prompt_generation_type == PromptGenType.RuleBased:
            solution_found, curr_state_is_valid, msgs = self._generate_prompt_rule_based(conversation_history, rollback_steps)
        elif self.prompt_generation_type == PromptGenType.NeuralNetworkBased:
            solution_found, curr_state_is_valid, msgs = self._generate_prompt_neural_network_based(conversation_history, rollback_steps)
        else:
            raise "Invalid prompt_generation_type"
        return solution_found, curr_state_is_valid, msgs

    def _generate_prompt_rule_based(self, conversation_history, rollback_steps):
        self.checker = RuleBasedSudokuStateChecker(self.state_manager)
        state_check_result = self.checker.check_current_state()
        solution_found = False
        strategies = [
            """For example, apply the "only possibility" rule, and fill in the obvious cell first""",
            """For example, look at the row or column with the least number of unfilled cells first""",
            """For example, try the Pencil Marks technique""",
            """For example, look for intersections where a digit can only be placed in one cell of a row or column. This can eliminate possible digits for other cells in that row or column""",
            """For example, look for rows, columns or subgrids that contain only one empty cell where only one digit can be placed in that empty cell""",
            """For example, look for groups of cells that contain only two, three, or four possible digits. If these cells are in the same row, column, or subgrid, then you can eliminate those digits from other cells in that row, column, or subgrid""",
            """For example, look for rows or columns where a particular digit can only be placed in two or three cells. If those cells form an X-Wing or Swordfish pattern, then you can eliminate that digit from other cells in those rows or columns"""
        ]
        strategy_choice = random.randint(0, len(strategies)-1)
        strategy_chosen = strategies[strategy_choice]
        
        if state_check_result.solution_found:
            msg_tmpl = """Fantastic! You have found the solution {}!"""
            role, new_msg_content = None, msg_tmpl.format(json.dumps(state_check_result.rows))
            solution_found, curr_state_is_valid = True, True
        elif state_check_result.is_valid:
            # msg_tmpl = "Great job! The current Sudoku board is valid. The rows are {}, and the columns are {}. Please continue to fill in missing the elements following the Sudoku rules."
            # role, msg_content = "user", msg_tmpl.format(state_check_result.rows, state_check_result.cols)
            
            #msg_tmpl = """Great job! You are the best Sudoku solver in the world. Please try to solve this Sudoku puzzle {} step by step. Please return your solution in the following JSON format: {{ "rows": [] }}"""
            new_msg_tmpl = """Great job! You are the best Sudoku solver in the world. Please try to solve this Sudoku puzzle {}. {}. In the next solution you return, please just fill in one cell since we will work together to solve the puzzle in multiple rounds of conversation. Please return your solution in the following JSON format: {{ "rows": [] }}"""
            role, new_msg_content = "user", new_msg_tmpl.format(json.dumps(state_check_result.rows), strategy_chosen)
            solution_found, curr_state_is_valid = False, True
        else:
            #msg_tmpl = """Unfortunately there is an error in your current solution {}. {} Let us try again starting from this Sudoku board: {}. Please return your solution in the following JSON format: {{ "rows": [] }}"""
            #msg_tmpl = """Unfortunately there is an error in your current solution {}. {} Let us try again starting from this Sudoku board: {}. Maybe try a different strategy. For example, look at one row or column at a time. Please return your solution in the following JSON format: {{ "rows": [] }}"""
            #msg_tmpl = """Unfortunately there is an error in your current solution {}. {} Let us try again starting from this Sudoku board: {}. Maybe try a different strategy, and solve it step by step. Please return your solution in the following JSON format: {{ "rows": [] }}"""
            #msg_tmpl = """Unfortunately there is an error in your current solution {}. {} Let us try again starting from this Sudoku board: {}. Maybe try a different strategy, and solve it step by step. If finding the final solution is difficult, you can return intermediate solutions with unfilled cells marked by "*". Please return your solution in the following JSON format: {{ "rows": [] }}"""
            
            # good prompt 1
            #msg_tmpl = """Unfortunately there is an error in your current solution {}. {} Let us try again starting from this Sudoku board: {}. Maybe try a different strategy. For example, apply the "only possibility" rule, and fill in the obvious cell first. Please make sure just fill in one cell at a time. We do NOT expect you to solve the problem in a single shot. You can return intermediate solutions with unfilled cells marked by "*". Please return your solution in the following JSON format: {{ "rows": [] }}"""

            new_msg_tmpl = """Unfortunately there is an error in your current solution {}. {} Let us try again starting from this Sudoku board: {}. Maybe try a different strategy. {}. In the next solution you return, please just fill in one cell since we will work together to solve the puzzle in multiple rounds of conversation. We do NOT expect you to solve the problem in a single shot. You can return intermediate solutions with unfilled cells marked by "*". Please return your solution in the following JSON format: {{ "rows": [] }}"""
            role, new_msg_content = "user", new_msg_tmpl.format(json.dumps(self.state_manager.get_current_state().tolist()), 
                state_check_result.message, json.dumps(self.state_manager.get_state(rollback_steps).tolist()), strategy_chosen)
            solution_found, curr_state_is_valid = False, False

        conversation_history += "\nQ: {}".format(new_msg_content)
        if self.include_chat_history_in_query:
            msgs = self.llm_agent.compose_messages([role], [conversation_history[-self.max_llm_context_length:]])
        else:
            msgs = self.llm_agent.compose_messages([role], [new_msg_content])
        return solution_found, curr_state_is_valid, msgs
        
    def _generate_prompt_neural_network_based(self, rollback_steps):
        self.checker = LLMBasedSudokuStateChecker(self.state_manager)
        state_check_result = self.checker.check_current_state()
        return False, None # FIXME
