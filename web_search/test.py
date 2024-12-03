import os
import logging
from dotenv import load_dotenv

load_dotenv()

from FlagEmbedding import BGEM3FlagModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from core.utils import init_logging
from core.search import GoogleSearchEngine, NaverSearchEngine
from core.chunker import RecursiveChunker
from common.summarize_comversation_node import summarize_conversation
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

embedder = BGEM3FlagModel('BAAI/bge-m3',  use_fp16=True)

questions = [
    '노벨 문학상을 받은 작가 이름이 뭐야',
    '올해에 받은 작가 이름 알려줘',
    '그럼 작가의 대표작 두 가지는',
    '아이폰 SE4 출시일과 정보 알려줘'
]

history = []

for question in questions:
    prev_conv = '' if len(history) == 0 else summarize_conversation(generator, history)    
    
    for event  in graph.stream({
        'prev_conv': prev_conv,
        'generator': generator,
        'engine': NaverSearchEngine(),
        'chunker': chunker,
        'embedder': embedder,
        'question': question,
    }, stream_mode='updates'):
        for key, item in event.items():
            print(f'================ {key} ================')
            if 'stream' in item:
                print(f'Q: {question}\n')
                answer = ''
                for ch in item['stream']:
                    answer += ch.content
                    print(ch.content, end='', flush=True)
                print('')
                history.append(HumanMessage(content=question))
                history.append(AIMessage(content=answer))
                