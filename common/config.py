import yaml
from common.enums import *

class Config:

    def __init__(self, path_to_config_yaml) -> None:
        with open(path_to_config_yaml, 'r') as file:
            configs = yaml.safe_load(file)
        
        # Chatbot configs
        chatbot_type_str = configs["chatbot"]["type"]
        if chatbot_type_str == "openai":
            self.chatbot_type = ChatbotType.OpenAI
        else:
            self.chatbot_type = ChatbotType.Invalid

        # OpenAI configs
        self.openai_model = configs["openai"]["model"]
        self.openai_api_key = configs["openai"]["api_key"]
