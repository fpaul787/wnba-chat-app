from langchain_core.prompts import ChatPromptTemplate

from services.embedding_service import get_embedding_model

class RagService:
    def __init__(self):
        self.vector_store = None
        self.embedding_model = get_embedding_model()

    def __create_rag_chain__(self, prompt: str):
        pass

    def __create_chat_model_prompt__(self):
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
