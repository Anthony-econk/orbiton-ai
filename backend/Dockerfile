# 파일 위치: orbiton.ai/backend/Dockerfile

FROM python:3.13.5  
# Python 3.13.5 이미지 사용

WORKDIR /backend  
# 백엔드 작업 디렉토리

COPY ./backend /backend  
COPY ./requirements.txt /backend/requirements.txt  
COPY ./GeoLite2-Country.mmdb /backend/GeoLite2-Country.mmdb  

RUN pip install --no-cache-dir -r requirements.txt  
# 의존성 설치

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
# FastAPI 실행
