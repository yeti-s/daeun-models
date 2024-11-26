
from abc import ABC, abstractmethod

from langchain.text_splitter import RecursiveCharacterTextSplitter

class Chunker(ABC):
    @abstractmethod
    def chunk(cls, text: str) -> list[str]:
        pass

class RecursiveChunker(Chunker):
    def chunk(self, text: str) -> list[str]:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=56)
        docs = text_splitter.create_documents([text])
        return [doc.page_content for doc in docs]