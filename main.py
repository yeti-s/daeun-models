# init log first
from app.shared.utils import init_logging
init_logging()

import argparse
import uvicorn
from fastapi import FastAPI
from app.routers.api.v1.tts import api_v1_tts

VERSION = '1.0.1'

app = FastAPI()
app.include_router(api_v1_tts)

@app.get('/')
def home():
    return {'version': VERSION}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=80)
    args = parser.parse_args()

    uvicorn.run('main:app', host=args.host, port=args.port)
    
