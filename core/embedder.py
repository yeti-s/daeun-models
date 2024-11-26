from typing import Union
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# example of init LLM
# HuggingFaceBgeEmbeddings(
#     model_name=EMBEDDING_LLM_NAME, 
#     model_kwargs={"device": "cuda"},
#     encode_kwargs={"normalize_embeddings": True}
# )

def embed(llm:HuggingFaceBgeEmbeddings, text: Union[str, list[str]]) -> list[list[float]]:
    if type(text) == list:
        return llm.embed_documents(text)
    return [llm.embed_query(text)]