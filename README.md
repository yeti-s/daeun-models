# 📱 Inference Module for Daeun

서버와 추론 모델 사이 느슨한 종속성을 위해 `TCP` 혹은 `Websocket` 서버를 구성하여 모델에게 간접적으로 접근하도록 설계하였습니다.
이를 통해 추론 모델이 변경되어도 통신 규칙만을 지킨다면 서버에서 추가적인 변경 없이 사용할 수 있도록 만들었습니다.

현재는 `TTS`, `Embedder`, `Generator` 세 가지 모델로 구상하였습니다.
각 모델에 대한 서버는 브랜치를 통해 접근할 수 있습니다.

# 🔄 Update

**24.06.09**

- TTS 모델에 대한 `TCP` 서버를 생성하였습니다.
- Melo TTS 모델 기반 서버를 이미지로 만들어 [REPO](https://hub.docker.com/repository/docker/sel9371/daeun-tts)에 배포하였습니다.