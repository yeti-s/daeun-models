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

## Summary Format

- Limit the summary to 3-5 sentences.
- Use short bullet point lists if necessary.

## Example Output

The user inquired about AI ethics. The AI explained key principles including transparency, fairness, and privacy. When the user requested real-world applications, the AI provided examples of self-driving cars and medical diagnostic systems. The conversation concluded with a discussion on the importance of AI ethics and future challenges in the field.

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