import logging
import asyncio

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from core.utils import init_logging

load_dotenv()
init_logging(logging.DEBUG)

from service import stream_response

app = FastAPI()

@app.get("/")
def version():
    return '0.1.0'

@app.post("/search")
async def ask_query(request: Request):
    body = await request.json()
    question = body.get("question", "")
    history = body.get("history", [])
    return StreamingResponse(stream_response(question, history))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)