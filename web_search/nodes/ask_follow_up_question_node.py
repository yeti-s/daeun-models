from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from core.generator import generate
from core.utils import combine_messages


SYSTEM_PROMPT = """You are an AI assistant designed to analyze user questions and generate follow-up question to resolve ambiguities.
You will receive the user's original question and an explanation of why that question is ambiguous.
Your task is as follows:
1. Carefully read the user's original question.
2. Analyze the provided ambiguity explanation.
3. If you need to understand the full context, please refer to the previous conversation.
4. Generate clear and specific single follow-up question to resolve the ambiguity in the original question.
5. Write follow-up question in Korean without anything.
"""

USER_PROMPT = """Question:
{question}

Explanation:
{explanation}
"""

def ask_follow_up_question(llm:ChatOpenAI, question:str, explanation:str, history:list[BaseMessage]) -> str:
    messages = combine_messages(
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=USER_PROMPT.format(question=question, explanation=explanation)),
        history
    )
    return generate(llm, messages).content