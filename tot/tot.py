import common.consts as consts
from common.enums import *
from common.prompter import SudokuPrompter


class TreeOfThought(object):

    def __init__(self) -> None:
        self.llm_agent = None

    def run(self, init_message, constraints, max_num_rounds) -> None:
        problem_type = self._extract_problem_type(init_message)
        totExecutor = self._get_tot_executor(problem_type)
        totExecutor.run(constraints, max_num_rounds)

    def _extract_problem_type(self, init_message):
        messages = self._generate_problem_type_query(init_message)
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

    def run(self, constraints, max_num_rounds) -> None:
        self.llm_agent.read_constraints(constraints)
        for i in range(max_num_rounds):
            messages = self.prompter.generate_prompt() # FIXME
            temperature = self._get_temperature()
            max_tokens = self._get_max_tokens()
            reply = self.llm_agent.get_reply(messages, temperature, max_tokens)
            solution = self.parser.parse_llm_reply(reply)
            if self._validate_solution(solution):
                break
            else:
                self.state.rollback(1) # backtracking

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