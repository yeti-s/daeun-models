import json

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from core.generator import generate
from core.utils import combine_messages

SYSTEM_PROMPT = """You are an AI assistant to assess user question is clear or ambiguous.
Carefully review the given question and respond according to the following guidelines:
1. Read the user's question carefully and identify the core content.
2. Identify the main keywords and concepts included in the question.
3. If you need to understand the full context, please refer to the previous conversation.
4. Evaluate whether the question is clear or ambiguous:
    a) If multiple interpretations are possible
    b) If it's overly broad or general
    c) If there is no one of specific date, location, and core content
    d) 0 - clear, 1 - ambiguous
5. Explain the reason of assessment.
6. Follow this output format without anything:
    {
        "reason": {reason},
        "is_ambiguous": {0 or 1}
    }
"""

USER_PROMPT = """Question:
{question}

Assesments:
"""

def check_ambiguity(llm:ChatOpenAI, question:str, history:list[BaseMessage]) -> dict:
    messages = combine_messages(
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=USER_PROMPT.format(question=question)),
        history
    )
    response = generate(llm, messages)
    return json.loads(response)
    