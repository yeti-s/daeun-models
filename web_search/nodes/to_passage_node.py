from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from core.generator import generate

system_prompt = "Please write a passage to answer the question in a single sentence. Do not use chinese."
user_prompt = "Question:\n{query}\nPassage:\n"

def to_passage(llm:ChatOpenAI, query:str) -> str:
    message = generate(llm, [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt.format(query=query))
    ])
    return message.content