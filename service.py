import os
import json
import asyncio

from FlagEmbedding import BGEM3FlagModel
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from core.search import GoogleSearchEngine
from core.chunker import RecursiveChunker
from web_search.builder import graph, GENERATE_ANSWER

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

search_engine = GoogleSearchEngine()

async def async_generator(iterator):
    for item in iterator:
        yield item
        await asyncio.sleep(0)

async def stream_response(question:str, history:list[str]):
    for i in range(len(history)):
        if i % 2 == 0:
            history[i] = HumanMessage(content=history[i])
        else:
            history[i] = AIMessage(content=history[i])
            
    init_state = {
        'history': history,
        'generator': generator,
        'engine': search_engine,
        'chunker': chunker,
        'embedder': embedder,
        'question': question,
    }
    
    async for event in async_generator(graph.stream(init_state, stream_mode='updates')):
        for key, item in event.items():
            node = key
            yield json.dumps({
                'node': node,
                'text': ''
            }) + '\n'
            
            if node == GENERATE_ANSWER:
                stream = item['stream']
                async for chunk in async_generator(stream):
                    yield json.dumps({
                        'node': node,
                        'text': chunk.content
                    }, ensure_ascii=False) + '\n'
    
    yield json.dumps({
        'node': 'END',
        'text': ''
    })