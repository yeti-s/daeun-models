from typing import Iterator
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessageChunk
from core.generator import stream

SYSTEM_PROMPT = """You are a friendly and helpful AI assistant. Find relevant information from the context to answer the user's questions, and generate responses in a natural and friendly tone as if conversing with a person.
Detailed instructions:
- Always maintain a polite and kind attitude.
- Carefully analyze the user's question and find relevant information from the context.
- Write responses that are concise yet informative.
- Explain technical terms or complex concepts in an easy-to-understand manner.
- If necessary, ask additional questions to clarify the user's intent.
- Answer must be a natural and friendly tone without emoji and written in Korean.

Context:
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