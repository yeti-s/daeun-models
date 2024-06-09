# 🔊 TTS TCP Server

프로젝트 [다은 서버](https://github.com/yeti-s/daeun-server)와 통신하기 위한 `TCP` 서버를 제작하였습니다.

# 🤔 How to use

### Build
아래 명령어를 사용하여 빌드할 수 있습니다.
```
$ docker build -tag {tag} -f {model}_tts/Dockerfile .
```
이미 빌드된 이미지를 도커 허브에 올려두었으니, 이를 사용할 수도 있습니다.

### Run
직접 빌드한 이미지를 사용하는 경우
```
$ docker run -p {port}:{port}/tcp -v {log_dir}:/logs --name {name} {image_name}
```
도커 허브에 올려진 이미지를 사용하는 경우
```
$ docker run -p {port}:{port}/tcp -v {log_dir}:/logs --name {name} sel9371/daeun-tts:{model}
```

컨테이너 환경 변수는 다음과 같습니다.
- **HOST**: TCP 서버의 호스트입니다. 기본 값은 `0.0.0.0`입니다.
- **PORT**: TCP 서버의 포트입니다. 기본 값은 `9999`입니다.
- **DEVICE**: 모델 추론에 사용할 장치입니다. `cpu`, `cuda`, `cuda:0` 등 알맞게 설정할 수 있습니다. 기본 값은 `cpu`입니다.
- **MODEL**: 사용할 모델을 설정합니다. 기본 값은 `melo`입니다. <span style="color:red">현재에는 Melo TTS만 지원합니다.</span>

환경 변수는 컨테이너를 생성할 때 다음과 같이 변경할 수 있습니다.
```
$ docker run -p 18765:8765/tcp -v ~/tts/logs:/logs --env PORT=8765 --name tts_tcp tts_tcp:melo
```

# 📝 Protocol

TTS 모델 서버와 통신하기 위한 프로토콜입니다.

```python
# INVALID: 잘못된 입력이 들어온 경우
# response
{
    "command": 0, # int
    "message": "'invalid command' is not a valid CMD" # str
}

# GET_NAME: 현재 적용중인 모델 이름 가져오기
# request
{
    "command": 1 # int
}
# response
{
    "command": 1, # int
    "message": "Melo TTS" # str
}

# TO_SPEECH: 해당 텍스트의 음성 데이터 생성하기
# request
{
    "command": 2, # int
    "text": "음성을 생성하고 싶은 텍스트", # str
    "speed": 1.0 # float
}
{
    "command": 2, # int
    "audio": "~~~~" # str (ndarr -> bytes -> base64 로 변환한 데이터)
    "sample_rate": 44100 # int
}
```

각 명령에 대한 ID는 다음과 같습니다.  
명령어의 ID는 요청 및 응답에서 `command`의 값이 됩니다.

| ID |     COMMAND     | DESCRIPTION |
|----|-----------------|-------------|
| 0  | INVALID         | 잘못된 요청에 대한 응답입니다.
| 1  | GET_NAME        | 현재 추론에 사용중인 모델에 대한 정보를 가져옵니다.
| 2  | TO_SPEECH       | 텍스트를 기반으로 음성 데이터를 생성합니다.

# 🤙🏻 Rule

해당 TCP 서버는 아래와 같은 폴더 구조를 가집니다.

```
|- model.py
|- server.py
|- tcp_server.py
|- utils.py
|- configs.json
|- README.md
|- melo_tts
|   |- Dockerfile
|   |- melo.py
|   |- requirements.txt
```
- 추가되는 모델은 `model.py` 의 Model 객체를 상속하도록 구성합니다.
- 추가되는 모델 서버 이미지 생성을 위한 `Dockerfile`과 의존성 `requirements.txt` 를 작성합니다.
- 위 생성된 파일들을 `[모델명]_tts` 폴더 안에 위치시킵니다.

# 🔄 Update

**24.06.09**

> 서버와 모델의 느슨한 종속성을 위해 TCP 통신으로 음성을 생성하도록 설계하였습니다.
이를 통해 추론 모델이 변경되어도 앞서 제시한 규칙을 지키면 쉽게 교체가 가능하도록 만들었습니다.

* 프로토콜과 규칙을 설정하였습니다.
* Melo TTS 모델을 추가하였습니다.
