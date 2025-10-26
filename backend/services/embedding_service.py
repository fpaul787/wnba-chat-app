from langchain_huggingface import HuggingFaceEmbeddings

model_name = 'sentence-transformers/all-MiniLM-L6-v2'

def get_hf_embedding_model(cache_folder="./embeddings_cache"):
    """
    Get the Hugging Face embedding model.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name=get_embedding_model_name(),
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
        cache_folder=cache_folder
    )
    return embeddings

def get_embedding_model_name():
    """
    Get the name of the embedding model.
    """
    return model_name