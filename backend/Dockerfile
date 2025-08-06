# backend/Dockerfile

FROM python:3.13.5  
# Python 3.13.5 이미지 사용

WORKDIR /backend  
# 작업 디렉토리 설정

COPY ./backend ./
COPY ./requirements.txt ./requirements.txt
COPY ./GeoLite2-Country.mmdb ./GeoLite2-Country.mmdb

RUN ls -la /backend
RUN pip install --no-cache-dir -r requirements.txt  


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]