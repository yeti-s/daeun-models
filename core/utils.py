import os
import logging
from datetime import datetime

def init_logging(level=logging.INFO, file=None):
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        filename=os.path.join('logs', f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log') if file is None else file,
        format = '%(asctime)s [%(levelname)s] %(message)s',
        datefmt = '%Y-%m-%d %I:%M:%S %p',
        level=level,
        encoding='utf-8'
    )    