from services.embedding_service import EmbeddingService
from services.vector_store_service import get_vector_store
from services.model_service import get_current_chat_model

class SimpleRagService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.llm = get_current_chat_model()

    def get_embedding(self, text: str):
        """
        Get the embedding for the given text.
        """
        return self.embedding_service.embed_query(text)