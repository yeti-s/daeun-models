from typing import Union
from FlagEmbedding import BGEM3FlagModel

# example of init model
# model = BGEM3FlagModel(EMBEDDING_LLM_NAME,  use_fp16=True)

def embed(model:BGEM3FlagModel, text: Union[str, list[str]], batch_size=8, max_length=512) -> list[list[float]]:
    text = [text] if type(text) == str else text
    return model.encode(
        text,
        batch_size=batch_size,
        max_length=max_length,
    )['dense_vecs']