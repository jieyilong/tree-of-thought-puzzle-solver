
from enum import Enum

class ChatbotType(Enum):
    OpenAI = 1

class PromptGenType(Enum):
    RuleBased = 1
    NeuralNetworkBased = 2

class ProblemType(Enum):
    Sudoku = 1
    ThreeSAT = 2