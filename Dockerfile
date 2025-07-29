# 파일 위치: orbiton-ai/Dockerfile

FROM python:3.13.5  
# Python 3.13.5 이미지 사용

WORKDIR /backend  
# backend 디렉토리를 작업 디렉토리로 설정

COPY ./backend /backend  
# backend 디렉토리만 복사

COPY requirements.txt .  
# 루트에 있는 requirements.txt만 복사

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY GeoLite2-Country.mmdb ./GeoLite2-Country.mmdb  
# GeoIP DB도 포함 (경로 유지 시)

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# FastAPI 앱 실행 (main.py는 backend 내에 위치하므로 WORKDIR 기준 OK)
