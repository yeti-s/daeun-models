import json
import socket
import base64
from enum import Enum
from model import Model
from utils import send, receive, info, debug, error

class CMD(Enum):
    INVALID = 0
    GET_NAME = 1
    TO_SPEECH = 2

class TCPServer():
    def __init__(self, host:str, port:int, model:Model) -> None:
        self.host = host
        self.port = port
        self.model = model
        self.valid = True
        self.cmd_func_map = {
            CMD.GET_NAME: self.__get_name__,
            CMD.TO_SPEECH: self.__to_speech__
        }
    
    def __respond_with_message__(self, cmd:CMD, msg:str) -> bytes:
        response = {
            'command': cmd.value,
            'message': msg
        }
        return json.dumps(response).encode()
    
    def __get_name__(self, request:dict) -> bytes:
        return self.__respond_with_message__(CMD.GET_NAME, self.model.get_model_name())
    
    def __to_speech__(self, request:dict) -> bytes:
        text = request['text']
        speed = request['speed']
        audio_bin = self.model.to_speech(text, speed)
        audio_bin = base64.b64encode(audio_bin)
        audio_str = audio_bin.decode()
        response = {
            'command': CMD.TO_SPEECH.value,
            'audio': audio_str,
            'sample_rate': self.model.get_sample_rate()
        }
        return json.dumps(response).encode()
    
    def __create_response__(self, requset:bytearray) -> bytes:
        try:
            data = json.loads(requset.decode())
            info(f'Receive: {data}')
            return self.cmd_func_map[CMD(data['command'])](data)

        except Exception as err:
            error(str(err))
            return self.__respond_with_message__(CMD.INVALID, str(err))
    
    def __listen__(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_sock:
            s_sock.bind((self.host, self.port))
            s_sock.listen()
            info(f'Listening on {self.host}:{self.port}')
            
            c_sock, addr = s_sock.accept()
            info(f'Connected by {addr}')
            
            while True:
                request = receive(c_sock)
                if not request:
                    info(f'Close connection with {addr}')
                    return True
                
                try:
                    response = self.__create_response__(request)
                    send(c_sock, response)
                    info(f'Send {len(response)} bytes to {addr}')
                except Exception as e:
                    error(str(e))
    
    def listen(self) -> None:
        """
        Start listening socket
        """
        while self.valid:
            self.__listen__()
    
    def close(self) -> None:
        """
        Don't listen any more when the last socket closed
        """
        self.valid = False