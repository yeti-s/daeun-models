import re
from datetime import datetime

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from core.generator import generate

SYSTEM_PROMPT = f"""당신은 사용자의 일정을 관리하는 AI 어시스턴트입니다.
다음 순서를 따라 사용자의 요청에서 일정을 분석하세요:

1. 사용자의 요청에서 일정의 내용과 날짜 정보를 확인하세요.
2. 필요하다면 이전 대화를 참고하여 필요한 정보를 확인하세요.
3. 다음과 같은 형식으로 일정을 분석하세요.
    Content: {{일정 내용}}
    Date: {{날짜 정보}}(YYYY-MM-DD)
    Question: {{추가 질문(선택)}}

## 추가 정보
현재 시각: {datetime.now().strftime("%a, %d %B, %Y, %I:%M%p")}
"""

USER_PROMPT = """Previous Conversation:
{prev_conv}

User Query:
{query}"""

def get_schedule(llm:ChatOpenAI, query:str, prev_conv:str) -> list[str]:
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=USER_PROMPT.format(prev_conv=prev_conv, query=query))
    ]
    response = generate(llm, messages).content

    content_pattern = r"Content:\s*(.*?)(?=\nDate:|$)"
    date_pattern = r"Date:\s*(.*?)(?=\nQuestion:|$)"
    question_pattern = r"Question:\s*(.*)"

    content_match = re.search(content_pattern, response)
    date_match = re.search(date_pattern, response)
    question_match = re.search(question_pattern, response)

    content = content_match.group(1) if content_match else None
    date = date_match.group(1) if date_match else None
    question = question_match.group(1) if question_match else None
    
    return content, date, question