import os
import logging
from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from core.utils import init_logging
from core.search import GoogleSearchEngine, NaverSearchEngine
from core.chunker import RecursiveChunker
from .builder import graph

init_logging(logging.DEBUG)

# LLM
LLM_API_KEY=os.environ['LLM_API_KEY']
GEN_LLM_URL=os.environ['GEN_LLM_URL']
GEN_LLM_NAME=os.environ['GEN_LLM_NAME']
GEN_MAX_TOKENS=os.environ.get('GEN_MAX_TOKENS', 1024)
GEN_TEMPERATURE=os.environ.get('GEN_TEMPERATURE', 0.7)
EMBEDDING_LLM_NAME=os.environ['EMBEDDING_LLM_NAME']

generator = ChatOpenAI(
    model_name = GEN_LLM_NAME,
    base_url= GEN_LLM_URL,
    api_key=LLM_API_KEY,
    max_tokens=GEN_MAX_TOKENS,
    temperature=GEN_TEMPERATURE,
)

chunker = RecursiveChunker()

embedder = HuggingFaceBgeEmbeddings(
    model_name=EMBEDDING_LLM_NAME, 
    model_kwargs={"device": "cuda"},
    encode_kwargs={"normalize_embeddings": True}
)

questions = [
    '노벨 문학상을 받은 작가 이름이 뭐야',
    '올해에 받은 작가 이름 알려줘',
    '그럼 작가의 대표작 두 가지는',
    '아이폰 SE에 대한 최신 소식 알려줘.'
]

history = []

for question in questions:
    for event  in graph.stream({
        'history': history,
        'generator': generator,
        'engine': NaverSearchEngine(),
        'chunker': chunker,
        'embedder': embedder,
        'question': question,
    }, stream_mode='updates'):
        for key, item in event.items():
            
            if 'answer_stream' in item:
                answer = ''
                for ch in item['answer_stream']:
                    answer += ch.content
                    print(ch.content, end='', flush=True)
                    
                history.append(HumanMessage(content=question))
                history.append(AIMessage(content=answer))
                