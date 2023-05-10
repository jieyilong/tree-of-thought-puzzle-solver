
from enum import Enum

class ChatbotType(Enum):
    Invalid = 0
    OpenAI = 1

class PromptGenType(Enum):
    RuleBased = 1
    NeuralNetworkBased = 2

class ProblemType(Enum):
    Sudoku = "sudoku"
    ThreeSAT = "3sat"

class SolverType(Enum):
    ToT = "tot"
    ZeroShot = "zero_shot"
    OneShotWithCoT = "one_shot_with_cot"
    FewShotWithCoT = "few_shot_with_cot"