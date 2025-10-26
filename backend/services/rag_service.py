from langchain_core.prompts import ChatPromptTemplate

from services.embedding_service import get_hf_embedding_model
from services.vector_store_service import get_vector_store

class RagService:
    def __init__(self):
        self.embedding_model = get_hf_embedding_model()
        self.vector_store = get_vector_store("", self.embedding_model)

    def __create_rag_chain__(self, prompt: ChatPromptTemplate):
        pass

    def __create_chat_model_prompt__(self, query: str) -> ChatPromptTemplate:
        template = """
        Use the following pieces of context to answer the question at the end. 
        Please follow the following rules:
        1. If you don't know the answer, don't try to make up an answer. Just say "I can't answer that".

        {context}

        Question: {question}
        """
        prompt = ChatPromptTemplate.from_template(template)
        return prompt

    def __generate_response__(self, query: str) -> dict:
        prompt = self.__create_chat_model_prompt__(query)
        rag_chain = self.__create_rag_chain__(prompt)
        response = None
        return {
            "answer": response,
        }

    def query(self, query) -> dict:
        return self.__generate_response__(query)
