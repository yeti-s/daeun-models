from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage

from core.generator import generate

SYSTEM_PROMPT = """You are an AI assistant tasked with summarizing conversations between users and AI. Please follow these guidelines to summarize the conversation:

1. Identify the main topics and key points of the conversation.
2. Clearly identify the user's questions or requests.
3. Extract the most important information or suggestions from the AI's responses.
4. Maintain the overall context and flow of the conversation.
5. Exclude unnecessary details or repetitive content.
6. Maintain an objective and neutral tone.
7. The summary should be concise but include all essential information.
8. Follow this summary format:
    - Limit the summary to 3-5 sentences.
    - Summary should be written in Korean.

## Example Output
사용자가 AI 윤리에 대해 질문했습니다. AI는 투명성, 공정성, 그리고 프라이버시를 포함한 주요 원칙을 설명했습니다. 사용자가 실제 사례를 요청하자 AI는 자율주행차와 의료 진단 시스템의 예를 제시했습니다. 대화는 AI 윤리의 중요성과 이 분야에서의 미래 도전에 대한 논의로 마무리되었습니다.

Based on this summary, understand the context of the conversation and prepare the next response."""

USER_PROMPT = """Conversation:
{conversation}
"""

def summarize_conversation(llm:ChatOpenAI, history:list[BaseMessage]) -> str:
    conversation = ''
    for message in history:
        conversation += f'{"user" if isinstance(message, HumanMessage) else "ai"}: {message.content}\n'
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=USER_PROMPT.format(conversation=conversation))
    ]
    
    return generate(llm, messages).content