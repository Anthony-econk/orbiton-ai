# backend/Dockerfile

FROM python:3.13.5  
# Python 3.13.5 이미지 사용

WORKDIR /backend  
# 작업 디렉토리 설정

COPY ./backend ./
COPY ./requirements.txt ./requirements.txt
COPY ./backend/GeoLite2-Country.mmdb ./backend/GeoLite2-Country.mmdb

# GeoIP DB 환경 변수 활용을 위한 선언
ENV GEOIP_DB_PATH=/backend/GeoLite2-Country.mmdb
# 디버깅용 파일 목록 확인
RUN echo "📁 백엔드 디렉토리 리스트:" && ls -al /backend
RUN echo "📁 루트 디렉토리 리스트:" && ls -al /

RUN pip install --no-cache-dir -r requirements.txt  


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]