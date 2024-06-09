import os
import json

from utils import info, debug, error
from melo_tts.melo import Melo
from tcp_server import TCPServer

HOST = os.environ['HOST'] if 'HOST' in os.environ else '0.0.0.0' 
PORT = os.environ['PORT'] if 'PORT' in os.environ else '9999' 
DEVICE = os.environ['DEVICE'] if 'DEVICE' in os.environ else 'cpu' 
MODEL = os.environ['MODEL'] if 'MODEL' in os.environ else 'melo'
MODELS = {
    'melo': Melo
}

if __name__ == "__main__":
    config = json.load(open('configs.json', 'r'))[MODEL]
    info(f'model:{MODEL} host:{HOST} port:{PORT} device:{DEVICE} config:{config}')
    
    model = MODELS[MODEL](DEVICE, config)
    server = TCPServer(HOST, int(PORT), model)
    server.listen()
    