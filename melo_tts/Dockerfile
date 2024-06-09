FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential libsndfile1 git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN git clone https://github.com/myshell-ai/MeloTTS.git
COPY . /app/MeloTTS

WORKDIR /app/MeloTTS
RUN pip install -r melo_tts/requirements.txt
RUN python -m unidic download
RUN mkdir /logs

CMD ["python", "server.py"]