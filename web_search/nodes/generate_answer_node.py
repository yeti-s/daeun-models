from typing import Iterator
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessageChunk
from core.generator import stream

SYSTEM_PROMPT = """You are an AI assistant to answer question using the provided contexts in Korean.

Contexts:
{passages}
"""

USER_PROMPT = """Question:
{question}

Answer:
"""

def generate_answer(llm:ChatOpenAI, question:str, passages:list[str]) -> Iterator[BaseMessageChunk]:
    return stream(llm, [
        SystemMessage(content=SYSTEM_PROMPT.format(passages="\n".join(passages))),
        HumanMessage(content=USER_PROMPT.format(question=question))
    ])