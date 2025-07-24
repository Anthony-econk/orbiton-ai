# 파일 위치: orbiton-ai/Dockerfile

FROM python:3.13.5  
# Python 3.13.5 이미지 사용

WORKDIR /app  
# 작업 디렉토리

COPY requirements.txt .  
# requirements.txt 복사

RUN pip install --no-cache-dir -r requirements.txt  
# 의존성 설치

COPY . .  
# app 소스 복사

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 
# FastAPI 실행

