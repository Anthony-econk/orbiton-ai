# 파일 위치: backend/Dockerfile

FROM python:3.13.5  
# Python 3.13.5 이미지 사용

WORKDIR /backend  
# 작업 디렉토리 설정

COPY requirements.txt ./requirements.txt  
# 의존성 파일 복사

COPY GeoLite2-Country.mmdb ./GeoLite2-Country.mmdb  
# GeoIP 데이터 파일 복사

RUN pip install --no-cache-dir -r requirements.txt  
# 의존성 설치

COPY . .  
# 나머지 소스 전체 복사

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]  
# FastAPI 실행
