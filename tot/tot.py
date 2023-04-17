import common.consts as consts
from common.enums import *
from actors.prompter import SudokuPrompter


class TreeOfThought(object):

    def __init__(self) -> None:
        self.llm_agent = None

    def run(self, user_input, max_num_rounds) -> None:
        problem_type = self._extract_problem_type(user_input)
        totExecutor = self._get_tot_executor(problem_type)
        totExecutor.run(max_num_rounds)

    def _extract_problem_type(self, user_input):
        messages = self._generate_problem_type_query(user_input)
        temperature = consts.DEFAULT_TEMPERATURE
        max_tokens = consts.DEFAULT_MAX_TOKENS
        reply = self.llm_agent.get_reply(messages, temperature, max_tokens)
        if not reply.has_key(consts.KEY_PROBLEM_TYPE):
            return False, None
        problem_type = reply[consts.KEY_PROBLEM_TYPE]
        return problem_type

    def _get_tot_executor(self, problem_type: ProblemType):
        if problem_type == ProblemType.Sudoku:
            return TreeOfThoughtExecutorForSudoku()
        elif problem_type == ProblemType.ThreeSAT:
            return TreeOfThoughtExecutorForThreeSAT()
        else:
            raise "Problem type not supported yet"


class TreeOfThoughtExecutorBase(object):

    def __init__(self) -> None:
        self.state = None
        self.llm_agent = None
        self.parser = None
        self.prompter = None

    def run(self, max_num_rounds) -> None:
        messages = self.prompter.generate_initial_prompt()
        for i in range(max_num_rounds):
            temperature = self._get_temperature()
            max_tokens = self._get_max_tokens()
            reply = self.llm_agent.get_reply(messages, temperature, max_tokens)
            solution = self.parser.parse_llm_reply(reply)
            self.state.update_state(solution)

            rollback_steps = 1
            curr_state_is_valid, messages = self.prompter.generate_prompt(rollback_steps) # FIXME
            if curr_state_is_valid:
                print("Problem solved! The final solution is {}".format(solution))
                break
            else:
                self.state.rollback(rollback_steps) # backtracking

    def _get_temperature(self):
        return None
    
    def _get_max_tokens(self):
        return None


class TreeOfThoughtExecutorForSudoku(TreeOfThoughtExecutorBase):

    def __init__(self) -> None:
        super().__init__()
        self.state = None # FIXME
        self.llm_agent = None # FIXME
        self.parser = None # FIXME
        self.prompter = None

    def run(self, constraints, max_num_rounds) -> None:
        super().run(constraints, max_num_rounds)
      
    def _get_temperature(self):
        return None
    
    def _get_max_tokens(self):
        return None


class TreeOfThoughtExecutorForThreeSAT(TreeOfThoughtExecutorBase):
    def __init__(self) -> None:
        super().__init__()
        self.state = None # FIXME
        self.llm_agent = None # FIXME
        self.parser = None # FIXME
        self.prompter = None

    def run(self, constraints, max_num_rounds) -> None:
        super().run(constraints, max_num_rounds)
      
    def _get_temperature(self):
        return None
    
    def _get_max_tokens(self):
        return None