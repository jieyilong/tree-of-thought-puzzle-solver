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

    def __init__(self, prompt_generation_type: PromptGenType) -> None:
        super().__init__()
        self.state_manager = SudokuStateManager()
        self.prompt_generation_type = prompt_generation_type

    def generate_initial_prompt(self, user_input) -> str:
        msg_tmpl = """Before solving this Sudoku puzzle {}, please return its initial board configuration in the following JSON format: {{ "rows": [] }}""" # FIXME
        role, msg_content = "user", msg_tmpl.format(user_input)
        msgs = self.llm_agent.compose_messages([role], [msg_content])
        return msgs
    
    def generate_prompt(self, rollback_steps) -> str:
        prompt = ""
        if self.prompt_generation_type == PromptGenType.RuleBased:
            prompt = self._generate_prompt_rule_based(rollback_steps)
        elif self.prompt_generation_type == PromptGenType.NeuralNetworkBased:
            prompt = self._generate_prompt_neural_network_based(rollback_steps)
        else:
            raise "Invalid prompt_generation_type"
        return prompt

    def _generate_prompt_rule_based(self, rollback_steps):
        self.checker = RuleBasedSudokuStateChecker(self.state_manager)
        state_check_result = self.checker.check_current_state()

        if state_check_result.is_valid:
            msg_tmpl = "Great job! The current Sudoku board is valid. The rows are [{}], and the columns are [{}]. Please continue to fill in missing the elements following the Sudoku rules."
            role, msg_content = "user", msg_tmpl.format(state_check_result.rows, state_check_result.cols)
        else:
            msg_tmpl = "Unfortunately there is an error in the current Sudoku board. {} Let us rewind to the previous state {} and try again."
            role, msg_content = "user", msg_tmpl.format(state_check_result.message, self.state_manager.get_state(rollback_steps))
        msgs = self.llm_agent.compose_messages([role], [msg_content])
        return msgs
        
    def _generate_prompt_neural_network_based(self, rollback_steps):
        self.checker = LLMBasedSudokuStateChecker(self.state_manager)
        state_check_result = self.checker.check_current_state()
        return None # FIXME
