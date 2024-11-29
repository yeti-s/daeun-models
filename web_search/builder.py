import time
import logging

from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langgraph.graph import StateGraph, START, END

from core.chunker import Chunker
from core.search import SearchEngine
from .nodes import (
    to_query,
    search, chunk, semantic_search,
    generate_answer
)

INITIALIZE = "INITIALIZE_NODE"
TO_QUERY = "TO_QUERY_NODE"
SEMANTIC_SEARCH = "SEMANTIC_SEARCH_NODE"
GENERATE_ANSWER = "GENERATE_ANSWER_NODE"

# ==================================================================================
# =============================== define states ====================================
# ==================================================================================


class State(TypedDict):
    prev_conv:str
    elapsed:float
    # inputs
    generator:ChatOpenAI
    engine:SearchEngine
    chunker:Chunker
    embedder:HuggingFaceBgeEmbeddings
    question:str
    # created
    query:str
    passages:list[Document]
    stream:str
    
    
# ==================================================================================
# =============================== define nodes =====================================
# ==================================================================================

def initialize_node(state: State) -> dict:
    return {
        'elapsed': time.time(),
    }

def to_query_node(state: State) -> dict:
    prev_conv = state['prev_conv']
    generator = state['generator']
    question = state['question']
    query = to_query(generator, question, prev_conv)
    logging.debug(f"[Elapsed:{TO_QUERY}] {time.time() - state['elapsed']:.2f}")

    return {
        'query': query
    }
    
def semantic_search_node(state: State) -> dict:
    engine = state['engine']
    embedder = state['embedder']
    chunker = state['chunker']
    query = state['query']
    elapsed = state['elapsed']
    pages = search(engine, query)
    logging.debug(f"[Elapsed:{SEMANTIC_SEARCH}-SEARCHING] {time.time() - elapsed:.2f}")
    chunks = chunk(chunker, pages)
    logging.debug(f"[Elapsed:{SEMANTIC_SEARCH}-CHUNKING] {time.time() - elapsed:.2f}")
    passages = semantic_search(embedder, query, chunks)
    logging.debug(f"[Elapsed:{SEMANTIC_SEARCH}] {time.time() - elapsed:.2f}")
    
    return {
        'passages': passages
    }

def generate_answer_node(state: State) -> dict:
    prev_conv = state['prev_conv']
    generator = state['generator']
    question = state['question']
    passages = state['passages']
    stream = generate_answer(generator, question, passages, prev_conv)
    logging.debug(f"[Elapsed:{GENERATE_ANSWER}] {time.time() - state['elapsed']:.2f}")
    
    return {
        'stream': stream,
        'elapsed': time.time() - state['elapsed']
    }


# ==================================================================================
# ============================= define routeres ====================================
# ==================================================================================




# ==================================================================================
# =============================== define graph =====================================
# ==================================================================================

graph_builder = StateGraph(State)

# create nodes
graph_builder.add_node(INITIALIZE, initialize_node)
graph_builder.add_node(TO_QUERY, to_query_node)
graph_builder.add_node(SEMANTIC_SEARCH, semantic_search_node)
graph_builder.add_node(GENERATE_ANSWER, generate_answer_node)

# create edges
graph_builder.add_edge(START, INITIALIZE)
graph_builder.add_edge(INITIALIZE, TO_QUERY)
graph_builder.add_edge(TO_QUERY, SEMANTIC_SEARCH)
graph_builder.add_edge(SEMANTIC_SEARCH, GENERATE_ANSWER)
graph_builder.add_edge(GENERATE_ANSWER, END)

# compile graph
graph = graph_builder.compile()