from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.generator import generate

system_prompt = "Please write a query for web searching to answer the question."
user_prompt = "Question:\n{query}\Query:\n"

def to_query(llm:ChatOpenAI, query:str) -> str:
    message = generate(llm, [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt.format(query=query))
    ])
    return message.content