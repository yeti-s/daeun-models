

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from ....services.audio import generate

api_v1_tts = APIRouter(prefix='/api/v1')

class ToSpeechParams(BaseModel):
    text:str
    speaker:str
    volume:float=1.0
    speed:float=1.0
    pitch:float=1.0
    format:str='mp3'

@api_v1_tts.post("/tts")
async def to_speech(params:ToSpeechParams):
    success, audio_bytes = generate(
        params.speaker,
        params.text,
        params.volume,
        params.speed,
        params.pitch,
        params.format
    )

    if success:
        return StreamingResponse(content=audio_bytes, media_type=f'audio/{params.format}')
    return HTTPException(400, detail='Wrong text found.')