import json
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

    def __init__(self, llm_agent, state_manager, prompt_generation_type: PromptGenType) -> None:
        super().__init__()
        self.llm_agent = llm_agent
        self.state_manager = state_manager
        self.prompt_generation_type = prompt_generation_type

    def generate_initial_prompt(self, user_input) -> str:
        msg_tmpl = """{} Before solving this Sudoku puzzle, please return its initial board configuration in the following JSON format: {{ "rows": [] }}. Please use "*" to represent the missing values. Do not provide a solution yet.""" # FIXME
        role, msg_content = "user", msg_tmpl.format(user_input)
        msgs = self.llm_agent.compose_messages([role], [msg_content])
        return msgs
    
    def generate_prompt(self, rollback_steps):
        if self.prompt_generation_type == PromptGenType.RuleBased:
            curr_state_is_valid, msgs = self._generate_prompt_rule_based(rollback_steps)
        elif self.prompt_generation_type == PromptGenType.NeuralNetworkBased:
            curr_state_is_valid, msgs = self._generate_prompt_neural_network_based(rollback_steps)
        else:
            raise "Invalid prompt_generation_type"
        return curr_state_is_valid, msgs

    def _generate_prompt_rule_based(self, rollback_steps):
        self.checker = RuleBasedSudokuStateChecker(self.state_manager)
        state_check_result = self.checker.check_current_state()

        if state_check_result.is_valid:
            # msg_tmpl = "Great job! The current Sudoku board is valid. The rows are {}, and the columns are {}. Please continue to fill in missing the elements following the Sudoku rules."
            # role, msg_content = "user", msg_tmpl.format(state_check_result.rows, state_check_result.cols)
            msg_tmpl = """Great job! You are the best Sudoku solver in the world. Please try to solve this Sudoku puzzle {} step by step. Please return your solution in the following JSON format: {{ "rows": [] }}"""
            role, msg_content = "user", msg_tmpl.format(json.dumps(state_check_result.rows))
            curr_state_is_valid = True
        else:
            msg_tmpl = """Unfortunately there is an error in your current solution {}. {} Let us try again starting from this Sudoku board: {}. Please return your solution in the following JSON format: {{ "rows": [] }}"""
            role, msg_content = "user", msg_tmpl.format(json.dumps(self.state_manager.get_current_state().tolist()), 
                                                        state_check_result.message, json.dumps(self.state_manager.get_state(rollback_steps).tolist()))
            curr_state_is_valid = False
        msgs = self.llm_agent.compose_messages([role], [msg_content])
        return curr_state_is_valid, msgs
        
    def _generate_prompt_neural_network_based(self, rollback_steps):
        self.checker = LLMBasedSudokuStateChecker(self.state_manager)
        state_check_result = self.checker.check_current_state()
        return False, None # FIXME
