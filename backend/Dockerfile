FROM python:3.13.5
# Python 3.13.5 이미지 사용

WORKDIR /backend  
# main.py가 위치한 디렉토리로 설정

COPY ./backend /backend  
# 전체 backend 소스 복사

RUN pip install --no-cache-dir -r requirements.txt  
# 의존성 설치

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  
# FastAPI 앱 실행
