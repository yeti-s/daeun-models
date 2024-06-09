from abc import ABCMeta, abstractmethod

class Model(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, device:str, config:object) -> None:
        """TTS model interface

        Args:
            device (str): device for inference
            config (object): model options
        """
        pass
    @abstractmethod
    def get_model_name(self) -> str:
        """Get model name
        """
        pass
    @abstractmethod
    def to_speech(self, text:str, speed:float) -> bytes:
        """Create audio from text

        Args:
            text (str): text to create audio
            speed (float): audio speed, default 1.0
        """
        pass
    @abstractmethod
    def get_sample_rate(self) -> int:
        """Get sample rate of model
        """
        pass