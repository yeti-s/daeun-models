# 🔊 TTS TCP Server

프로젝트 [다은 서버](https://github.com/yeti-s/daeun-server)와 통신하기 위한 `TCP` 서버를 제작하였습니다.

# 🤔 How to use

### Build
아래 명령어를 사용하여 빌드할 수 있습니다.
```
$ docker build -tag {tag} .
```
이미 빌드된 이미지를 도커 허브에 올려두었으니, 이를 사용할 수도 있습니다.

### Run
직접 빌드한 이미지를 사용하는 경우
```
$ docker run -p {port}:80 -v {log_dir}:/logs --name {name} {image_name}
```
도커 허브에 올려진 이미지를 사용하는 경우
```
$ docker run -p {port}:80 -v {log_dir}:/logs --name {name} sel9371/daeun-tts:{model}
```

컨테이너 환경 변수는 다음과 같습니다.
- **MELO_DEVICE**: `melo` 모델 추론에 사용할 장치입니다. `cpu`, `cuda`, `cuda:0` 등 알맞게 설정할 수 있습니다. 기본 값은 `cpu`입니다.

# 📝 Protocol

TTS 모델 서버와 통신하기 위한 프로토콜입니다.

```python
# GET http://<host>:<port>/api/v1/tts
# JSON BODY
{
    "text": "송성근은 매우 똑똑하다.",
    "speaker": "melo",
    "speed": 1.0, # optional 
    "volume": 1.0 # optional
    "pitch": 1.0 # optional
    "fmt": "wav" # optional ["wav", "mp3"]
}
```

# 🤙🏻 Rule

해당 TCP 서버는 아래와 같은 폴더 구조를 가집니다.

```
|- app
|   |- models
|   |- routers
|   |- services
|   |- shared
|- main.py
|- configs.json
```
- `configs.json`에서 각 모델에 대한 기본 설정값을 가져옵니다.

# 🔄 Update

**24.12.13**
> 기존 TCP 통신 구조가 아닌 `HTTP` 통신을 사용하도록 업데이트되었습니다.

* `FastAPI` 기반 서버를 구성하여 `HTTP` 통신을 이용하도록 변경하였습니다.

**24.06.09**

> 서버와 모델의 느슨한 종속성을 위해 TCP 통신으로 음성을 생성하도록 설계하였습니다.
이를 통해 추론 모델이 변경되어도 앞서 제시한 규칙을 지키면 쉽게 교체가 가능하도록 만들었습니다.

* 프로토콜과 규칙을 설정하였습니다.
* Melo TTS 모델을 추가하였습니다.
