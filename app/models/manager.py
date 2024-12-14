import time
import logging
from queue import Queue
from typing import Callable
from threading import Thread

from .tts import GenOption, TTS

INFO_TEMPLATE = """Complete audio generation
model: {model}
text: {text}
volume: {volume}
speed: {speed}
pitch: {pitch}
format: {format}
bytes: {bytes}
elapsed: {elapsed}"""

class TTSQueue():
    def __init__(self) -> None:
        self.queue = Queue()
        self.num_models = 0
        self.valid = True
        self.thread = Thread(target=self.__infer__)
        self.thread.start()

    def __infer__(self):
        while self.valid:
            while self.queue.qsize():
                try:
                    model, text, option, handler, inserted_at = self.queue.get()
                    audio_bytes = model.generate(
                        text,
                        option.volume,
                        option.speed,
                        option.pitch,
                        option.format
                    )
                    
                    logging.info(INFO_TEMPLATE.format(
                        model=model.name,
                        text=text,
                        volume=option.volume,
                        speed=option.speed,
                        pitch=option.pitch,
                        format=option.format,
                        bytes=f'{(audio_bytes.getbuffer().nbytes):.2f} KB',
                        elapsed=f'{(time.time()-inserted_at):.2f}s'
                    ))

                    handler(True, audio_bytes)
                except Exception as err:
                    logging.error(f'Error found on generating {text} by {model.name}. {str(err)}')
                    handler(False, audio_bytes)
            # wait for a while to prevent overload
            time.sleep(0.1)
    
    def put(self, model:TTS, text:str, option:GenOption, handler:Callable) -> None:
        self.queue.put((model, text, option, handler, time.time()))

    def close(self):
        self.valid = False
        self.thread.join()


class TTSManager():
    def __init__(self) -> None:
        self.speakers = {}
        self.queues = {}
        self.devices = set()
    
    def add_model(self, name:str, cls:TTS, device:str, option:dict):
        if name in self.speakers:
            return self.speakers[name]

        if device not in self.queues:
            self.queues[device] = TTSQueue()
        
        model = cls(device, option)
        queue = self.queues[device]

        self.speakers[name] = {
            'model': model,
            'queue': queue
        }

    def generate(self, speaker, text:str, option:GenOption, handler:Callable):
        target = self.speakers[speaker]
        model = target['model']
        queue = target['queue']
        queue.put(model, text, option, handler)

    def __infer__(self):
        pass
