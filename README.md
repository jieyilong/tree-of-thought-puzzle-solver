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

## Run

```shell
python main.py
```
