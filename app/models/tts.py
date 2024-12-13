import io
import time
import soundfile as sf

from abc import ABCMeta, abstractmethod
from melo.api import TTS as MeloTTS

from ..shared.utils import info, debug, error, warn


class GenOption():
    def __init__(self, volume:float, speed:float, pitch:float, format:str) -> None:
        self.speed = speed
        self.volume = volume
        self.pitch = pitch
        self.format = format
        self.done = False

    def wait(self) -> None:
        while not self.done:
            # wait for a while to prevent overload
            time.sleep(0.01)

class TTS(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, device:str, config:object) -> None:
        """TTS model interface

        Args:
            device (str): device for inference
            config (object): model options
        """
        pass

    @abstractmethod
    def generate(self, text:str, volume:float, speed:float, pitch:float, format:str) -> bytes:
        """Create audio from text

        Args:
            text (str): text to create audio
            volume (float): audio volume, default 1.0
            speed (float): audio speed, default 1.0
            pitch (float): audio pitch, default 1.0
            formant (str): audio formant, default is 'wav'
        Returns:
            audio(bytes): audio bytes data
        """
        pass
    @abstractmethod
    def get_sample_rate(self) -> int:
        """Get sample rate of model
        """
        pass

class Melo(TTS):
    def __init__(self, device:str, config:object) -> None:
        super().__init__(device, config)
        self.tts = MeloTTS(language='KR', device=device)
        self.speaker_id = self.tts.hps.data.spk2id['KR'] # set speaker korean
        self.name = 'melo'

        # load model
        self.generate('모델을 불러옵니다.')
    
    def get_sample_rate(self) -> int:
        return self.tts.hps.data.sampling_rate
    
    def generate(self, text:str, volume:float, speed:float, pitch:float, format:str) -> bytes:
        audio = self.tts.tts_to_file(text, self.speaker_id, speed=speed)
        # write audio bytes in memory
        audio_bytes = io.BytesIO()
        sf.write(audio_bytes, audio, self.get_sample_rate(), format=format)
        audio_bytes.seek(0)

        return audio_bytes