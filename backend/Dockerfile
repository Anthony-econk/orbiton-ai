# backend/Dockerfile

FROM python:3.13.5  
# Python 3.13.5 이미지 사용

WORKDIR /backend  
# 작업 디렉토리 설정

COPY ./backend ./  
# backend 폴더 전체 복사 (루트 기준)

COPY ./requirements.txt ./requirements.txt  
# 루트의 requirements.txt 명확히 복사

COPY ./GeoLite2-Country.mmdb ./GeoLite2-Country.mmdb  
# 루트의 GeoIP DB 복사

RUN pip install --no-cache-dir -r requirements.txt  
# 의존성 설치

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]