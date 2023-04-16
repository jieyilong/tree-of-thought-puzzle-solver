from state import *


class PrompterBase(object):

    def __init__(self) -> None:
        pass


class SudokuPrompter(PrompterBase):

    def __init__(self) -> None:
        super().__init__()
        self.state = SudokuState()

    def generate_prompt(self) -> str:
        pass

    def _generate_prompt_rule_based(self) -> str:
        pass

    def _generate_prompt_nn_based(self) -> str:
        pass