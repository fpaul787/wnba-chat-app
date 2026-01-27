from models import Content
from embedding_service import EmbeddingService
from vector_store_service import VectorStoreService
from model_service import ModelService
from content_store import ContentStoreService
from typing import Dict, List

class SimpleRagService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        if not self.embedding_service.validate_connection():
            raise ConnectionError("Failed to validate EmbeddingService connection.")
        self.vector_store_service = VectorStoreService()
        self.llm_model = ModelService()
        self.content_store = ContentStoreService()

    def _get_embedding(self, text: str):
        """
        Get the embedding for the given text.
        """
        return self.embedding_service.embed_query(text)
    
    def _query_vector_store(self, query: str):
        """
        Query the vector store with the given text.
        """
        query_embedding = self._get_embedding(query)
        results = self.vector_store_service.query(query_embedding, top_k=5, include_metadata=True)
        return results
    
    def _fetch_chunks(self, ids: List[str]) -> List[Content]:
        """
        Fetch text chunks from Databricks based on the given IDs.
        """
        return self.content_store.get_content_by_ids(ids)
        
    def _validate_query(self, query: str):
        # Type validation
        if not isinstance(query, str):
            raise TypeError("Query must be a string")
        
        # Empty/whitespace validation
        if not query or not query.strip():
            raise ValueError("Query cannot be empty or only whitespace")
        
        # Length validation
        if len(query) > 1500:  # Adjust based on your needs
            raise ValueError("Query too long")
        
        if len(query.strip()) < 3:
            raise ValueError("Query too short (minimum 3 characters)")
    
    def generate_answer(self, query: str) -> Dict:
        """
        Generate an answer to the query using the LLM and context from the vector store.
        """
        self._validate_query(query)
        vector_results = self._query_vector_store(query)
        ids = [match.id for match in vector_results]
        content_chunks_data = self._fetch_chunks(ids)
        context_chunks = [content.text for content in content_chunks_data]
        context = "\n\n".join(context_chunks)

        prompt = f"""
        Answer the question based on the context below. If the context does not provide enough information, say "I don't know".
        Context: {context}
        Question: {query}
        """

        response = self.llm_model.query_model(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"answer": response}