from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import List


MODEL_NAME = "gpt-4o-mini"

class ModelService:
    """
    Docstring for ModelService
    """
    def __init__(self):
        self.client = OpenAI(api_key="")
        self.model_name = MODEL_NAME
    
    def query_model(self, messages: List[ChatCompletionMessageParam]):
        """
        Query the chat model with the given messages.
        """
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )
        return response.choices[0].message.content