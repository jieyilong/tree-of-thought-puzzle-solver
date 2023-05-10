import json
import common.consts as consts
import common.utils as utils
from common.hyperparams import HyperParams
from common.enums import *
from common.hyperparams import HyperParams
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
        if totExecutor is None:
            print("Problem type not supported yet")
            return
        totExecutor.run(user_input, max_num_rounds)

    def _extract_problem_type(self, user_input):
        messages = self._generate_problem_type_query(user_input)
        temperature = HyperParams.DefaultTemperature
        max_tokens = HyperParams.DefaultMaxTokens
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
        self.conversation_history = ""
        self.state_manager_visit_count_map = {}

    def run(self, user_input, max_num_rounds) -> None:
        messages = self.prompter.generate_initial_prompt(user_input)
        for i in range(max_num_rounds):
            temperature = self._get_temperature()
            max_tokens = self._get_max_tokens()
            reply = self.llm_agent.get_reply(messages, temperature, max_tokens)
            self._incr_state_visit_count()

            self.conversation_history += "\nA: {}".format(reply)

            if self._should_repeat(reply):
                continue
            success, solution = self.parser.parse_llm_reply(reply)
            if not success:
                print("Failed to extract solution from the reply, will retry")
                continue # retry
            self.state_manager.update_state(solution)

            rollback_steps = self._get_rollback_steps()
            solution_found, curr_state_is_valid, messages = self.prompter.generate_prompt(self.conversation_history, rollback_steps) # FIXME
            if solution_found:
                print(messages) # FIXME: better print out
                return
            
            if not curr_state_is_valid:
                self.state_manager.rollback(rollback_steps) # backtracking

        print("Sorry, unable to solve the problem within {} rounds of conversations.".format(max_num_rounds))

    def _incr_state_visit_count(self):
        if self.state_manager.get_current_state() is None:
            return
        curr_state_key = json.dumps(self.state_manager.get_current_state().tolist())
        if not (curr_state_key in self.state_manager_visit_count_map):
            self.state_manager_visit_count_map[curr_state_key] = 0
        self.state_manager_visit_count_map[curr_state_key] += 1
        print("\nVISIT COUNT for {}: {}\n".format(curr_state_key, self.state_manager_visit_count_map[curr_state_key]))
    
    def _get_parent_state_visit_count(self):
        parent_state = self.state_manager.get_state(rollback_steps = 1)
        if parent_state is None:
            return 0
        parent_state_key = json.dumps(parent_state.tolist())
        if not (parent_state_key in self.state_manager_visit_count_map):
            return 0
        else:
            return self.state_manager_visit_count_map[parent_state_key]

class TreeOfThoughtExecutorForSudoku(TreeOfThoughtExecutorBase):

    def __init__(self, config) -> None:
        super().__init__()
        self.state_manager = SudokuStateManager()
        self.llm_agent = LLMAgent(config)
        self.parser = LLMReplyParserForSudoku()
        self.prompter = SudokuPrompter(self.llm_agent, self.state_manager, 
            config.chatbot_max_context_length, config.chatbot_include_chat_history_in_query,
            PromptGenType.RuleBased)

    def _should_repeat(self, llm_reply):
        return ("{" not in llm_reply) # FIXME: make this check more generic
    
    def _get_temperature(self):
        return HyperParams.DefaultTemperature
    
    def _get_max_tokens(self):
        return HyperParams.DefaultMaxTokens
    
    def _get_rollback_steps(self):
        max_rollback_steps = self.state_manager.max_rollback_steps()
        parent_state_visit_count = self._get_parent_state_visit_count()
        if parent_state_visit_count >= HyperParams.MaxStateVisitCount:
            rollback_steps = 2 # should backtrack and explore other possibilities
        else:
            rollback_steps = 1
        
        if rollback_steps > max_rollback_steps:
            rollback_steps = max_rollback_steps

        curr_state_key = json.dumps(self.state_manager.get_current_state().tolist())

        print("State History:")
        for state in self.state_manager.sudoku_matrix_history:
            print("        State:", json.dumps(state.tolist()))
        print("max_rollback_steps: {}".format(max_rollback_steps))
        print("parent_state_visit_count: {}".format(parent_state_visit_count))
        print("ROLLBACK STEPS: {}\n".format(rollback_steps))
        return rollback_steps


class TreeOfThoughtExecutorForThreeSAT(TreeOfThoughtExecutorBase):
    def __init__(self, config) -> None:
        super().__init__()
        self.state_manager = None # FIXME
        self.llm_agent = None # FIXME
        self.parser = None # FIXME
        self.prompter = None

    def _should_repeat(self, llm_reply):
        return False
    
    def _get_temperature(self):
        return HyperParams.DefaultTemperature
    
    def _get_max_tokens(self):
        return HyperParams.DefaultMaxTokens
    
    def _get_rollback_steps(self):
        return 1