from sentence_transformers import SentenceTransformer

model_name = 'sentence-transformers/all-MiniLM-L6-v2'

def get_embedding_model():
    return SentenceTransformer(model_name)