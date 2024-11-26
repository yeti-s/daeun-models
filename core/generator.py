import logging
from typing import Iterator, Union
from langchain_openai import ChatOpenAI
from langchain_core.outputs import LLMResult
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage, BaseMessageChunk
from langchain_community.callbacks import get_openai_callback


NO_SYSTEM_PROMPT_MODELS = ['gemma']

# example of init LLM
# ChatOpenAI(
#     model_name=model_name,
#     api_key=api_key,
#     max_tokens=max_tokens,
#     temperature=temperature,
#     top_p=top_p,
#     n=n,
#     base_url=base_url
# )

def is_system_prompt_available(llm:ChatOpenAI) -> bool:
    for model in NO_SYSTEM_PROMPT_MODELS:
        if model in llm.model_name:
            return False
    return True

def system_to_user_prompt(messages:Union[list[BaseMessage], list[list[BaseMessage]]]) -> list[BaseMessage]:
    system_prompt = None
    if type(messages[0]) is list:
        messages = messages[0]
    if type(messages[0]) is SystemMessage:
        system_prompt = messages.pop(0).content
    
    if system_prompt is not None:
        new_messages = []
        for message in messages:
            if isinstance(message, HumanMessage):
                new_messages.append(HumanMessage(content=f"{system_prompt}\n\n{message.content}"))
            else:
                new_messages.append(message)
        messages = new_messages
    
    return messages
    
def generate(llm:ChatOpenAI, messages:Union[list[BaseMessage], list[list[BaseMessage]]]) -> Union[AIMessage, LLMResult]:
    # convert system message to user message if model do not support system messages
    if not is_system_prompt_available(llm):
        messages = system_to_user_prompt(messages)
    
    with get_openai_callback() as cb:
        if llm.n > 1:
            response = llm.generate([messages])
            logging.debug(f"Prompt Tokens: {cb.prompt_tokens}, completion Tokens: {cb.completion_tokens}")
            return response
        
        response = llm.invoke(messages)
        logging.debug(f"Prompt Tokens: {cb.prompt_tokens}, completion Tokens: {cb.completion_tokens}")
        logging.debug(f'Generated:\n{response.content}')
        return response

def stream(llm:ChatOpenAI, messages:Union[list[BaseMessage], list[list[BaseMessage]]]) -> Iterator[BaseMessageChunk]:
    if not is_system_prompt_available(llm):
        messages = system_to_user_prompt(messages)
        
    return llm.stream(messages)