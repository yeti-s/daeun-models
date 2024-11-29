from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from core.generator import generate

SYSTEM_PROMPT = f"""You are an AI assistant that generates web search query based on the user's questions.
Refer to previous conversations to generate the search query.
Write the search query only without anything.

Additional Information:
Current date: {datetime.now().strftime("%a, %d %B, %Y, %I:%M%p")}"""

USER_PROMPT = """Previous Conversation:
{prev_conv}

Question:
{question}

Query:
"""

def to_query(llm:ChatOpenAI, question:str, prev_conv:str) -> str:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=USER_PROMPT.format(prev_conv=prev_conv, question=question))
    ]
    return generate(llm, messages).content