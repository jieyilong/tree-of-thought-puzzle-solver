import common.consts as consts
import common.utils as utils
from common.enums import *
from actors.state import SudokuStateManager
from actors.llm import LLMAgent
from actors.parser import LLMReplyParserForSudoku
from actors.prompter import SudokuPrompter


class TreeOfThought(object):

    def __init__(self, config) -> None:
        self.config = config
        self.llm_agent = LLMAgent(config)

    def run(self, user_input, max_num_rounds) -> None:
        success, problem_type = self._extract_problem_type(user_input)
        if not success:
            print("Failed to identify the problem type")
            return
        totExecutor = self._get_tot_executor(problem_type)
        if totExecutor == None:
            print("Problem type not supported yet")
            return
        totExecutor.run(user_input, max_num_rounds)

    def _extract_problem_type(self, user_input):
        messages = self._generate_problem_type_query(user_input)
        temperature = consts.DEFAULT_TEMPERATURE
        max_tokens = consts.DEFAULT_MAX_TOKENS
        reply = self.llm_agent.get_reply(messages, temperature, max_tokens)
        success, json_obj = utils.extract_json_from_text_string(reply)
        if not success:
            return False, None
        if not (consts.KEY_PROBLEM_TYPE in json_obj):
            return False, None
        try:
            problem_type = ProblemType(json_obj[consts.KEY_PROBLEM_TYPE])
        except:
            return False, None
        return True, problem_type
    
    def _generate_problem_type_query(self, user_input):
        msg_tmpl = """The user is asking "{}". What type of problem the user wants to solve? Please give the answer in the following JSON format: {{ "{}": "<problem_type>" }} where <problem_type> can only be "sudoku", "3sat", or "others"."""
        msg_content = msg_tmpl.format(user_input, consts.KEY_PROBLEM_TYPE)
        role = "user"
        msgs = self.llm_agent.compose_messages([role], [msg_content])
        return msgs

    def _get_tot_executor(self, problem_type: ProblemType):
        if problem_type == ProblemType.Sudoku:
            return TreeOfThoughtExecutorForSudoku(self.config)
        elif problem_type == ProblemType.ThreeSAT:
            return TreeOfThoughtExecutorForThreeSAT()
        else:
            return None


class TreeOfThoughtExecutorBase(object):

    def __init__(self) -> None:
        pass

    def run(self, user_input, max_num_rounds) -> None:
        messages = self.prompter.generate_initial_prompt(user_input)
        for i in range(max_num_rounds):
            temperature = self._get_temperature()
            max_tokens = self._get_max_tokens()
            reply = self.llm_agent.get_reply(messages, temperature, max_tokens)
            success, solution = self.parser.parse_llm_reply(reply)
            if not success:
                print("Failed to extract solution from the reply, will retry")
                continue # retry
            self.state.update_state(solution)

            rollback_steps = self._get_rollback_steps()
            curr_state_is_valid, messages = self.prompter.generate_prompt(rollback_steps) # FIXME
            if curr_state_is_valid:
                print("Problem solved! The final solution is {}".format(solution))
                return
            else:
                self.state.rollback(rollback_steps) # backtracking
        print("Sorry, unable to solve the problem within {} rounds of conversations.".format(max_num_rounds))


class TreeOfThoughtExecutorForSudoku(TreeOfThoughtExecutorBase):

    def __init__(self, config) -> None:
        super().__init__()
        self.state = SudokuStateManager()
        self.llm_agent = LLMAgent(config)
        self.parser = LLMReplyParserForSudoku()
        self.prompter = SudokuPrompter(self.llm_agent, PromptGenType.RuleBased)

    def _get_temperature(self):
        return consts.DEFAULT_TEMPERATURE
    
    def _get_max_tokens(self):
        return consts.DEFAULT_MAX_TOKENS
    
    def _get_rollback_steps(self):
        return 1


class TreeOfThoughtExecutorForThreeSAT(TreeOfThoughtExecutorBase):
    def __init__(self, config) -> None:
        super().__init__()
        self.state = None # FIXME
        self.llm_agent = None # FIXME
        self.parser = None # FIXME
        self.prompter = None

    def _get_temperature(self):
        return consts.DEFAULT_TEMPERATURE
    
    def _get_max_tokens(self):
        return consts.DEFAULT_MAX_TOKENS
    
    def _get_rollback_steps(self):
        return 1