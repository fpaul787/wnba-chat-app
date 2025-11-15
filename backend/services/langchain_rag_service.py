from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from services.embedding_service import get_hf_embedding_model
from services.vector_store_service import get_vector_store
from services.model_service import get_current_chat_model

class RagService:
    def __init__(self):
        self.embedding_model = get_hf_embedding_model()
        self.llm = get_current_chat_model()
        self.vector_store = get_vector_store("", self.embedding_model)

    def __get_retriever__(self):
        retriever = self.vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        return retriever

    def __create_rag_chain__(self, prompt: ChatPromptTemplate):
        retriever = self.__get_retriever__()
        rag_chain = (
            {
                "context": retriever,
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    def __create_chat_prompt__(self) -> ChatPromptTemplate:
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
        prompt = self.__create_chat_prompt__()
        rag_chain = self.__create_rag_chain__(prompt)
        response = rag_chain.invoke(query)
        return {
            "answer": response,
        }

    def query(self, query) -> dict:
        return self.__generate_response__(query)
