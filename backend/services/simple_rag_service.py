from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService
from services.model_service import ModelService

class SimpleRagService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.llm_model = ModelService()

    def get_embedding(self, text: str):
        """
        Get the embedding for the given text.
        """
        return self.embedding_service.embed_query(text)
    
    def query_vector_store(self, query: str):
        """
        Query the vector store with the given text.
        """
        query_embedding = self.get_embedding(query)
        results = self.vector_store_service.query(query_embedding, top_k=5, include_metadata=True)

        return results
    
    def generate_answer(self, query: str):
        """
        Generate an answer to the query using the LLM and context from the vector store.
        """
        results = self.query_vector_store(query)
        context_chunks = [match.metadata['text'] for match in results if 'text' in match.metadata]
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
        return response