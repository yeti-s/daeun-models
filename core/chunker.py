
from abc import ABC, abstractmethod

from langchain.text_splitter import RecursiveCharacterTextSplitter

class Chunker(ABC):
    @abstractmethod
    def chunk(self, text: str) -> list[str]:
        pass
    
    @abstractmethod
    def split_documents(self, documents: list[str]) -> list[str]:
        pass

class RecursiveChunker(Chunker):
    def chunk(self, text: str) -> list[str]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=56)
        docs = text_splitter.split_text([text])
        return [doc.page_content for doc in docs]
    
    def split_documents(self, documents: list[str]) -> list[str]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=56)
        docs = text_splitter.split_documents(documents)
        return [doc.page_content for doc in docs]