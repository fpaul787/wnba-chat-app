from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()


MODEL_NAME = "gpt-4o-mini"

class ModelService:
    """
    Service to interact with the OpenAI chat model.
    """
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        try:
            self.client.models.list()
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            raise
        self.model_name = MODEL_NAME
    
    def query_model(self, messages: List[ChatCompletionMessageParam]):
        """
        Query the chat model with the given messages.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error querying model: {e}")
            raise