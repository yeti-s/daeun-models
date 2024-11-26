from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader

from core.chunker import Chunker
from core.search import SearchEngine, SearchResult

def search(engine:SearchEngine, query:str, top_k:int=5) -> list[SearchResult]:
    pages = engine.search(query)
    pages = pages[:min(len(pages), top_k)]  # Limit to top_k results
    return pages

def chunk(chunker:Chunker, pages:list[SearchResult]) -> list[Document]:
    links = [page.link for page in pages]
    docs = WebBaseLoader(links).load_and_split(chunker)
    return docs