pip install -r requirements.txt
# clone core code of Melo TTS
git clone https://github.com/myshell-ai/MeloTTS.git
cp -r MeloTTS/melo .
rm -rf MeloTTS
python -m unidic download
