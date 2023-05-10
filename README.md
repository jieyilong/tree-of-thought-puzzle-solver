# Tree of Thought Puzzle Solver Demo


## Setup

Install the required dependencies (Python 3.9+ required):

```shell
pip install -r requirements.txt
```

Create an empty YAML file `config.yaml` under the current directory, and paste in the following content. Then, please set your choice of model (e.g. "gpt-3.5-turbo") and your OpenAI API Key:

```yaml
chatbot:
    type: "openai"
    max_context_length: 8000
    include_chat_history_in_query: false
openai:
    model: <model_name>
    api_key: <your_open_ai_api_key>
```

## Run ToT

```shell
python run_tot.py "<problem_description>"

# Example
python run_tot.py "please solve this 4x4 sudoku puzzle [[*,1,*,*],[*,*,2,*],[*,*,*,4],[1,*,*,*]] where * represents a cell to be filled in."
```

## Run Experiments

```shell
# solver_type: zero_shot, one_shot_with_cot, few_shot_with_cot, tot
python run_expr.py <solver_type> <path/to/problem/set/json>

# Example
python run_expr.py one_shot_with_cot data/benchmarks/sudoku/3x3_sudoku_puzzles.json
python run_expr.py tot data/benchmarks/sudoku/3x3_sudoku_puzzles.json
```