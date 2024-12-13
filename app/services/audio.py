import os
from typing import Optional

from ..models.manager import TTSManager
from ..models.tts import GenOption, Melo

MELO_DEVICE = os.getenv('MELO_DEVICE', 'cpu')

global_manager = TTSManager()
global_manager.add_model('melo', Melo, MELO_DEVICE, {})

def generate(speaker:str, text:str, volume:float, speed:float, pitch:float, format:str) -> tuple[bool, bytes]:
    option = GenOption(volume, speed, pitch, format)
    success, audio_bytes = False, None
    def __handler__(result:bool, buffer:Optional[bytes]=None):
        nonlocal success, audio_bytes
        success, audio_bytes = result, buffer
        option.done = True
    
    global_manager.generate(speaker, text, option, __handler__)
    option.wait()

    return success, audio_bytes
