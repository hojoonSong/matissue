FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . /app

