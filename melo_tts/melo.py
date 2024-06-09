from model import Model
from melo.api import TTS

class Melo(Model):
    def __init__(self, device:str, config: object) -> None:
        super().__init__(device, config)
        self.tts = TTS(language=config['language'], device=device)
        self.language = config['language']
        self.speaker_ids = self.tts.hps.data.spk2id
        self.model_name = 'Melo TTS'
    
    def get_model_name(self) -> str:
        return self.model_name
    
    def get_sample_rate(self) -> int:
        return self.tts.hps.data.sampling_rate
    
    def to_speech(self, text: str, speed: float) -> bytes:
        audio = self.tts.tts_to_file(text, self.speaker_ids[self.language], speed=speed)
        return audio.tobytes()