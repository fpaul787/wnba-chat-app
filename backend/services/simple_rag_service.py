from services.embedding_service import get_hf_embedding_model
from services.vector_store_service import get_vector_store
from services.model_service import get_current_chat_model

class SimpleRagService:
    def __init__(self):
        self.embedding_model = get_hf_embedding_model()
        self.llm = get_current_chat_model()
        self.vector_store = get_vector_store("", self.embedding_model)