from pinecone import Pinecone
from typing import Any, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class VectorStoreService:
    def __init__(self):
        self.index_name = "wnba-chat-pinecone-rag"
        
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable not set")
            
        try:
            self.client = Pinecone(api_key=api_key)
            self.index = self.client.Index(self.index_name)
        except Exception as e:
            raise Exception(f"Error initializing Pinecone index '{self.index_name}': {e}")

    
    def query(self, embedding: List[float], top_k: int = 5, include_metadata: bool = True) -> List[Any]:
        """
        Query the vector store with the given embedding.
        
        Args:
            embedding: Vector embedding to search for
            top_k: Number of results to return (1-10000)
            include_metadata: Whether to include metadata in results
            
        Returns:
            List of matching results with scores and metadata
            
        Raises:
            ValueError: If embedding is invalid or top_k is out of range
            ConnectionError: If Pinecone service is unavailable
            RuntimeError: If query execution fails
        """
        # Input validation
        if not embedding or not isinstance(embedding, list):
            raise ValueError("Embedding must be a non-empty list of floats")
        
        if not all(isinstance(x, (int, float)) for x in embedding):
            raise ValueError("All embedding values must be numeric")
        
        if not (1 <= top_k <= 10000):
            raise ValueError("top_k must be between 1 and 10000")
        
        try:
            # Execute the query
            response = self.index.query(
                vector=embedding,
                top_k=top_k,
                include_metadata=include_metadata
            )
            
            # Validate response structure
            if not hasattr(response, 'matches'):
                raise RuntimeError("Invalid response format from Pinecone")
            
            matches = response.matches # pyright: ignore[reportAttributeAccessIssue]
            if matches is None:
                return []
            
            # Validate each match has required attributes
            validated_matches = []
            for match in matches:
                if hasattr(match, 'id') and hasattr(match, 'score'):
                    validated_matches.append(match)
                else:
                    print(f"Warning: Invalid match format: {match}")
            
            return validated_matches
            
        except Exception as e:
            # Handle unexpected errors
            raise RuntimeError(f"Unexpected error during vector query: {e}")