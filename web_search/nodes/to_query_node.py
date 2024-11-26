from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from core.generator import generate

SYSTEM_PROMPT = f"""You are an AI assistant that generates web search query based on the user's questions.
If necessary, refer to previous conversations to generate the search query.
Write the search query only without anything.

Additional Information:
Current date: {datetime.now().strftime("%a, %d %B, %Y, %I:%M%p")}"""

USER_PROMPT = "Question:\n{query}\Query:\n"

def to_query(llm:ChatOpenAI, query:str, history:list[BaseMessage]) -> str:
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    messages.extend(history)
    messages.append(HumanMessage(content=USER_PROMPT.format(query=query)))
    return generate(llm, messages).content