from state import *
from checker import *
from enums import PromptGenType


class PrompterBase(object):

    def __init__(self) -> None:
        pass


class SudokuPrompter(PrompterBase):

    PROMPT_TEMPLATES = ["Here is a", "the rows are", "the columns are"]

    def __init__(self, prompt_generation_type: PromptGenType) -> None:
        super().__init__()
        self.state_manager = SudokuStateManager()
        self.checker = SudokuStateChecker(self.state_manager)
        self.prompt_generation_type = prompt_generation_type

    def generate_prompt(self):
        success, prompt = False, None
        if self.prompt_generation_type == PromptGenType.RuleBased:
            success, prompt = self._generate_prompt_rule_based()
        elif self.prompt_generation_type == PromptGenType.NeuralNetworkBased:
            success, prompt = self._generate_prompt_nn_based()
        return success, prompt

    def _generate_prompt_rule_based(self):
        valid = self.checker.check_current_state()

        
        return False, None

    def _generate_prompt_nn_based(self):
        return False, None
