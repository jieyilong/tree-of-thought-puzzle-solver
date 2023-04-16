import openai
from enums import ChatbotType
from config import Config 

class LLMAgent(object):

    def __init__(self, chatbot_type: ChatbotType) -> None:
        self.chatbot = self._initialize_chatbot(chatbot_type)

    def get_reply(self, messages, temperature = None, max_tokens = None) -> str:
        return self.chatbot.get_reply(messages, temperature, max_tokens)

    def _initialize_chatbot(self, chatbot_type):
        if chatbot_type == ChatbotType.OpenAI:
            return OpenAIChatbot()
        else:
            raise "Not supported for now!"


class ChatbotBase(object):

    def __init__(self) -> None:
        pass

    def get_reply(self, messages, temperature = None, max_tokens = None) -> str:
        return ""
    
    
class OpenAIChatbot(ChatbotBase):

    def __init__(self) -> None:
        super().__init__()
        self.cfg = Config()
        self.model = self.cfg.openai_model
        openai.api_key = self.cfg.openai_api_key

    def get_reply(self, messages, temperature = None, max_tokens = None) -> str:
        response = openai.ChatCompletion.create(
            model = self.model,
            messages = messages,
            temperature = temperature,
            max_tokens = max_tokens
        )
        reply = response.choices[0].message["content"]
        return reply

