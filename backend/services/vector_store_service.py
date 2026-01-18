from pinecone import Pinecone

class VectorStoreService:
    def __init__(self):
        self.index_name = "your-index-name"
        self.client = Pinecone(api_key="")
        self.index = self.client.Index(self.index_name)

    
    def query(self, embedding: list[float], top_k: int = 5, include_metadata: bool = True):
        """
        Query the vector store with the given embedding.
        """
        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=include_metadata
        )
        return results.matches # pyright: ignore[reportAttributeAccessIssue]