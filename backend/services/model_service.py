from langchain_openai import ChatOpenAI

MODEL_NAME = "gpt-4o-mini"
def get_current_chat_model():
    return ChatOpenAI(model=MODEL_NAME)