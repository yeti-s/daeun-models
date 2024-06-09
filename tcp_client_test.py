import json
import socket
import base64
import soundfile
import numpy as np
from utils import send, receive
from tcp_server import CMD

def test_0(sock:socket) -> None:
    request = {'command': 'invalid command'}
    request = json.dumps(request).encode()
    send(sock, request)
    
    response = receive(sock)
    response = json.loads(response)
    print(CMD.INVALID)
    print(response)

def test_1(sock:socket) -> None:
    request = {'command': CMD.GET_NAME.value}
    request = json.dumps(request).encode()
    send(sock, request)
    
    response = receive(sock)
    response = json.loads(response)
    print(CMD.GET_NAME)
    print(response)

def test_2(sock:socket) -> None:
    request = {
        'command': CMD.TO_SPEECH.value,
        'text': '내 다시는 술먹고 뛰어다니지 않으리.',
        'speed': 1.0
    }
    request = json.dumps(request, ensure_ascii=False).encode()
    send(sock, request)
    
    response = receive(sock)
    response = json.loads(response)
    command = response['command']
    sample_rate = response['sample_rate']
    audio_str = response['audio']
    audio_bin = base64.b64decode(audio_str)
    soundfile.write("test_2.wav", np.frombuffer(audio_bin, np.float32), sample_rate)
    print(CMD.TO_SPEECH)
    print(f'command: {command}')
    print(f'sample_rate: {sample_rate}')
   

def receive_audio(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        print(f"Connected to {ip}:{port}")
        test_0(sock)
        test_1(sock)
        test_2(sock)
            
if __name__ == "__main__":
    receive_audio('0.0.0.0', 9999)