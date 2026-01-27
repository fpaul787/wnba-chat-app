from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
model_name = 'text-embedding-ada-002'

class EmbeddingService:
    """
    Embedding service for generating text embeddings using OpenAI.
    """
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._validated = False

    def validate_connection(self) -> bool:
        """
        Optionally validate the OpenAI client connection.
        Only call this when you need to verify the connection is working.
        """
        try:
            self.client.models.list()
            self._validated = True
            return True
        except Exception as e:
            print(f"Error validating OpenAI client: {e}")
            return False

    def get_embedding_model_name(self) -> str:
        """
        Get the name of the embedding model.
        """
        return model_name
    
    def embed_query(self, text: str) -> list[float]:
        """
        Get the embedding for the given text.
        """
        try:
            return self.client.embeddings.create(
                input=text,
                model=model_name
            ).data[0].embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise