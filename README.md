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
  
[![FastAPI 패키지 버전](https://img.shields.io/pypi/v/fastapi.svg)](https://pypi.org/project/fastapi/)
[![FastAPI Python 버전](https://img.shields.io/pypi/pyversions/fastapi.svg)](https://pypi.org/project/fastapi/)
[![FastAPI GitHub Stars](https://img.shields.io/github/stars/tiangolo/fastapi.svg?style=social&label=Star&maxAge=2592000)](https://github.com/tiangolo/fastapi)

[![Redis 릴리스 버전](https://img.shields.io/github/v/release/redis/redis.svg)](https://redis.io)
[![Redis 지원 플랫폼](https://img.shields.io/badge/supported%20platforms-linux%20%7C%20osx-brightgreen)](https://redis.io)
[![Redis GitHub Stars](https://img.shields.io/github/stars/redis/redis.svg?style=social&label=Star&maxAge=2592000)](https://github.com/redis/redis)

[![PyMongo](https://img.shields.io/badge/PyMongo-MongoDB-green)](https://www.mongodb.com/drivers/pymongo)
[![PyMongo GitHub Stars](https://img.shields.io/github/stars/mongodb/mongo-python-driver.svg?style=social&label=Star&maxAge=2592000)](https://github.com/mongodb/mongo-python-driver)

[![Motor](https://img.shields.io/badge/Motor-Async%20MongoDB%20Driver-blue)](https://motor.readthedocs.io)
[![Motor GitHub Stars](https://img.shields.io/github/stars/mongodb/motor.svg?style=social&label=Star&maxAge=2592000)](https://github.com/mongodb/motor)

</p>


---
　
　
　

## 🌟 개요

💼 엘리스 SW트랙 4기 맛이슈의 백엔드 팀은 **FastAPI**, **MongoDB**, 그리고 **Motor**를 사용했습니다. 이 선택은 3주간의 짧은 기간 동안 유연한 프로젝트 설계를 위한 것으로, FastAPI는 뛰어난 성능과 효율성을 제공하여 빠른 개발과 처리를 가능하게 합니다. 또한, ASGI를 기반으로 한 비동기 처리와 타입 힌트를 통해 안정성을 높입니다. MongoDB는 데이터의 유연한 저장과 처리를 지원하여 프로젝트의 확장성을 높입니다. Motor는 비동기 MongoDB 드라이버로서 높은 성능과 함께 간편한 사용법을 제공합니다. 이를 통해 우리는 제한된 시간 내에 프로젝트를 유연하게 설계하고 개발할 수 있었습니다. 따라서, FastAPI, MongoDB, Motor를 사용함으로써 민첩한 개발과 유지보수를 지원하며, 사용자에게 우수한 경험을 제공하는 데 도움이 되었습니다.

　

## 🚀 기대사항

🎨 확장성 있는 웹 커뮤니티를 제작하고자 할 때, 해당 코드를 활용하여 다양한 기능을 확장하여 구현할 수 있습니다. 해당 프로젝트는 풍부한 사용자 경험을 제공하며, 웹소켓 및 이메일 인증과 같은 다양한 기능을 제공합니다. 이 프로젝트는 웹 개발을 시작하는 데 유용한 스켈레톤 코드로 활용할 수 있습니다. 또한, FastAPI의 빠르고 간편한 경험은 프로젝트 개발에 큰 도움이 될 것입니다.

　

## ⚙ 사전 요구사항

- 🐍 최신 버전의 Python (3.6 이상)과 pip가 설치되어 있어야 합니다. 이 프로젝트에서는 Redis, MongoDB를 부가적으로 사용합니다. 
- 📚 [FastAPI](https://fastapi.tiangolo.com/)와 [Motor](https://motor.readthedocs.io/en/stable/) 문서를 참고하세요.

　

## 🌈 최고의 웹 서비스를 만들어가는 여정에 맛이슈 백엔드팀이 이뤄냈습니다. 🚀
이 프로젝트를 통해 최고 수준의 웹 서비스를 구축하는 데 필요한 기술과 지식을 얻을 수 있습니다. 맛이슈의 백엔드 팀과 함께 이 여정에서 함께 배우고 성장하며, 혁신적인 웹 서비스를 만들어가는 데 기여하세요!

　
　
　

## 📝 기능 설명


#### 사용자 인증

- 사용자 등록과 로그인을 위한 인메모리 데이터베이스 레디스 세션 기반 인증을 사용합니다.
- 이메일 인증을 통해 사용자가 제공한 이메일 주소의 유효성을 검증합니다.

#### 웹소켓 통신

- 웹소켓을 이용하여 실시간으로 알림 기능을 구현합니다.

#### 레시피 관리

- 사용자는 레시피를 작성, 수정, 삭제할 수 있습니다.
- 다른 사용자가 작성한 레시피에 대해 댓글을 남기거나 좋아요를 표시할 수 있습니다.

#### 댓글 및 알림

- 사용자는 레시피에 댓글을 남길 수 있으며, 댓글이 달리면 해당 레시피 작성자에게 알림이 전송됩니다.
- 구독을 받은 사용자는 알림을 받습니다!

　

## 📁 폴더 구조
```bash
.
├── API
│   ├── controllers
│   │   ├── recipe_controller.py
│   │   ├── user_controller.py
│   │   ├── verify_controller.py
│   │   └── websocket_controller.py
│   └── routes
│       ├── api_routes.py
│       ├── recipe_routes.py
│       ├── user_routes.py
│       ├── verify_routes.py
│       └── websocket_routes.py
├── README.md
├── constants.py
├── dao
│   ├── recipe_dao.py
│   └── user_dao.py
├── main.py
├── models
│   ├── recipe_models.py
│   ├── response_models.py
│   └── user_models.py
├── output.txt
├── requirements.txt
├── services
│   ├── recipe_service.py
│   └── user_service.py
├── templates
│   ├── email_verification_code.html
│   ├── forgot_id_email.html
│   ├── forgot_password.html
│   └── verification_email.html
└── utils
    ├── config.py
    ├── db_manager.py
    ├── email_manager.py
    ├── hash_manager.py
    ├── notification_manager.py
    ├── permission_manager.py
    ├── response_manager.py
    ├── session_manager.py
    └── websocket_manager.py

```
　
## 포지션
- :lemon: 백엔드 팀장 송호준 : USERS, Email 인증, Websocket 구현 담당
-  :green_apple:  맛이슈 팀장 신유빈 : RECIPIES, COMMENT, 배포 담당


　

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


