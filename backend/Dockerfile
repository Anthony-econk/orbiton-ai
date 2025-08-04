# backend/Dockerfile  
# Orbiton.ai - FastAPI 서버용 Dockerfile

FROM python:3.13.5  
# Python 3.13.5 이미지 사용

WORKDIR /backend  
# 작업 디렉토리 설정

COPY ./backend /backend  
# 애플리케이션 소스 복사

COPY ./requirements.txt ./requirements.txt  
# 의존성 복사 (루트 기준)

COPY ./GeoLite2-Country.mmdb /backend/GeoLite2-Country.mmdb  
# GeoIP DB 복사

RUN pip install --no-cache-dir -r requirements.txt  
# 의존성 설치

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# 앱 실행 명령
