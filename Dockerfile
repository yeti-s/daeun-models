FROM pytorch/pytorch:2.3.1-cuda11.8-cudnn8-runtime

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

# install submodules
RUN apt-get update && apt-get install -y \
    build-essential libsndfile1 git \
    && rm -rf /var/lib/apt/lists/* \
    && ./install_submodules.sh

# start server
CMD ["python", "main.py"]