from state import *
from checker import *
from enums import PromptGenType


class PrompterBase(object):

    def __init__(self) -> None:
        pass

    def generate_prompt(self) -> str:
        return ""


class SudokuPrompter(PrompterBase):

    def __init__(self, prompt_generation_type: PromptGenType) -> None:
        super().__init__()
        self.state_manager = SudokuStateManager()
        self.prompt_generation_type = prompt_generation_type

    def generate_prompt(self) -> str:
        prompt = ""
        if self.prompt_generation_type == PromptGenType.RuleBased:
            prompt = self._generate_prompt_rule_based()
        elif self.prompt_generation_type == PromptGenType.NeuralNetworkBased:
            prompt = self._generate_prompt_neural_network_based()
        else:
            raise "Invalid prompt_generation_type"
        return prompt

    def _generate_prompt_rule_based(self):
        self.checker = RuleBasedSudokuStateChecker(self.state_manager)
        state_check_result = self.checker.check_current_state()

        if state_check_result.is_valid:
            msg_tmpl = "Great job! The current Sudoku board is valid. The rows are [{}], and the columns are [{}]. Please continue to fill in missing the elements following the Sudoku rules."
            return msg_tmpl.format(state_check_result.rows, state_check_result.cols)
        else:
            msg_tmpl = "Unfortunately there is an error in the current Sudoku board. {} Let us rewind to the previous state and try again."
            return msg_tmpl.format(state_check_result.message)
        
    def _generate_prompt_neural_network_based(self):
        self.checker = LLMBasedSudokuStateChecker(self.state_manager)
        state_check_result = self.checker.check_current_state()
        return None # FIXME
