import os
import struct
import logging
import socket
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=os.path.join('/logs', datetime.now().strftime('%Y-%m-%dT%H-%M-%S-tts.log')),
    filemode='a'
)

def info(msg:str) -> None:
    logging.info(msg)

def debug(msg:str) -> None:
    logging.debug(msg)

def error(msg:str) -> None:
    logging.error(msg)

def warning(msg:str) -> None:
    logging.warning(msg)

def send(sock:socket, msg:str) -> None:
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recvall(sock:socket, n:int) -> bytearray:
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def receive(sock:socket) -> None:
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    return recvall(sock, msglen)