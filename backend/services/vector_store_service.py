from pinecone import Pinecone
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class VectorStoreService:
    def __init__(self):
        self.index_name = "wnba-chat-pinecone-rag"
        self.client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        try:
            self.index = self.client.Index(self.index_name)
        except Exception as e:
            raise Exception(f"Error initializing Pinecone index: {e}")

    
    def query(self, embedding: List[float], top_k: int = 5, include_metadata: bool = True):
        """
        Query the vector store with the given embedding.
        """
        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=include_metadata
        )
        return results.matches # pyright: ignore[reportAttributeAccessIssue]