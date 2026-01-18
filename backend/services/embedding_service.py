from openai import OpenAI
model_name = 'text-embedding-ada-002'

class EmbeddingService:
    """
    Docstring for EmbeddingService
    """
    def __init__(self):
        self.client = OpenAI(api_key="")

    def get_embedding_model_name(self) -> str:
        """
        Get the name of the embedding model.
        """
        return model_name
    
    def embed_query(self, text: str) -> list[float]:
        """
        Get the embedding for the given text.
        """
        return self.client.embeddings.create(
            input=text,
            model=model_name
        ).data[0].embedding