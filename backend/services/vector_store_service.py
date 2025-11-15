from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings, OpenAIEmbeddings

def get_vector_store(index_name: str, embeddings: HuggingFaceEmbeddings | OpenAIEmbeddings) -> FAISS:
    """
    Get the vector store instance.
    """
    return FAISS.load_local(index_name, embeddings=embeddings)