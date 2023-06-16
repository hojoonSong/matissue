<p align="center">
  <a href="https://fastapi.tiangolo.com/" target="blank"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="180" alt="FastAPI 로고" /></a>　
  <a href="https://www.mongodb.com/" target="blank"><img src="https://www.mongodb.com/assets/images/global/favicon.ico" width="60" alt="MongoDB 로고" /></a>　
  <a href="https://redis.io/" target="blank"><img src="https://velog.velcdn.com/images/sejinkim/post/c3f2148b-a8c2-4628-bb5a-eb5f47cab0c2/image.png" width="180" alt="Redis 로고" /></a>　
  <a href="https://motor.readthedocs.io/en/stable/" target="blank"><img src="https://motor.readthedocs.io/en/stable/_images/motor.png" width="180" alt="Motor 로고" /></a>　
  <a href="https://www.matissue.com/" target="blank"><img src="https://matissue.com/logo.svg" width="180" alt="맛이슈 로고" /></a>
</p>

<p align="center">
🚀 <b>맛이슈 서버는 표준 Python 타입 힌트를 기반으로 한 모던하고 고성능 웹 프레임워크인 FastAPI를 사용하여 API를 구축한 웹 프로젝트입니다.</b> 🚀
</p>

<p align="center">
<a href="https://pypi.org/project/fastapi/" target="_blank"><img src="https://img.shields.io/pypi/v/fastapi.svg" alt="패키지 버전" /></a>
<a href="https://pypi.org/project/fastapi/" target="_blank"><img src="https://img.shields.io/pypi/pyversions/fastapi.svg" alt="Python 버전" /></a>
<a href="https://github.com/tiangolo/fastapi" target="_blank"><img src="https://img.shields.io/github/stars/tiangolo/fastapi.svg?style=social&label=Star&maxAge=2592000" alt="GitHub Stars" /></a>
</p>

---

## 🌟 개요
💼 엘리스 SW트랙 4기 맛이슈의 백엔드 팀은 **FastAPI**, **MongoDB**, 그리고 **Motor**를 사용했습니다. 이 선택은 3주간의 짧은 기간 동안 유연한 프로젝트 설계를 위한 것으로, FastAPI는 뛰어난 성능과 효율성을 제공하여 빠른 개발과 처리를 가능하게 합니다. 또한, ASGI를 기반으로 한 비동기 처리와 타입 힌트를 통해 안정성을 높입니다. MongoDB는 데이터의 유연한 저장과 처리를 지원하여 프로젝트의 확장성을 높입니다. Motor는 비동기 MongoDB 드라이버로서 높은 성능과 함께 간편한 사용법을 제공합니다. 이를 통해 우리는 제한된 시간 내에 프로젝트를 유연하게 설계하고 개발할 수 있었습니다. 따라서, FastAPI, MongoDB, Motor를 사용함으로써 민첩한 개발과 유지보수를 지원하며, 사용자에게 우수한 경험을 제공하는 데 도움이 되었습니다.

## 🚀 기대사항
🎨 확장성 있는 웹 커뮤니티를 제작하고자 할 때, 해당 코드를 활용하여 다양한 기능을 확장하여 구현할 수 있습니다. 해당 프로젝트는 풍부한 사용자 경험을 제공하며, 웹소켓 및 이메일 인증과 같은 다양한 기능을 제공합니다. 이 프로젝트는 웹 개발을 시작하는 데 유용한 스켈레톤 코드로 활용할 수 있습니다. 또한, FastAPI의 빠르고 간편한 경험은 프로젝트 개발에 큰 도움이 될 것입니다.

## ⚙ 사전 요구사항
- 🐍 최신 버전의 Python (3.6 이상)과 pip가 설치되어 있어야 합니다. 이 프로젝트에서는 Redis, MongoDB를 부가적으로 사용합니다. 
- 📚 [FastAPI](https://fastapi.tiangolo.com/)와 [Motor](https://motor.readthedocs.io/en/stable/) 문서를 참고하세요.

## 🛠 설치하기
애플리케이션을 설치하려면 다음 단계를 따르세요:

```bash
# 저장소 복제하기
$ git clone https://kdt-gitlab.elice.io/sw_track/class_04/web_2_project/team10/dev-be

# 저장소 디렉토리로 이동하기
$ cd dev-be

# 의존성 설치하기
$ pip install -r requirements.txt

# env에는 다음과 같이 요구됩니다.
MONGO_DB_URL=
MONGO_DB_NAME=
REDIS_URL=
SMTP_SERVER=
SMTP_PORT=
SENDER_EMAIL=
SMTP_PASSWORD=

# 다음과 같이 서버를 실행합니다.
$ uvicorn main:app 
