from langchain_core.documents import Document
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

from core.chunker import Chunker
from core.embedder import embed
from core.search import SearchEngine, SearchResult

def search(engine:SearchEngine, query:str, top_k:int=5) -> list[SearchResult]:
    pages = engine.search(query)
    pages = pages[:min(len(pages), top_k)]  # Limit to top_k results
    return pages

def chunk(chunker:Chunker, pages:list[SearchResult]) -> list[Document]:
    links = [page.link for page in pages]
    docs = WebBaseLoader(links).load_and_split(chunker)
    return docs

def semantic_search(model:HuggingFaceBgeEmbeddings, query:str, chunks:list[Document]):
    q_embedding = model.embed_query(query)  # Embed the query
    embeddings = model.embed_documents(chunks)  # Embed the documents
    similarities = cosine_similarity([q_embedding], embeddings).flatten()  # Compute cosine similarity
    sorted_indices = similarities.argsort()[::-1]  # Sort by similarity in descending order
    return [chunks[i] for i in sorted_indices[:15]]  # Return sorted chunks