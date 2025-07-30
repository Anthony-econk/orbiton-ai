# orbiton.ai/backend/Dockerfile

FROM python:3.13.5  
# Python 3.13.5 이미지 사용

WORKDIR /backend  
# 실제 디렉토리명 기준 작업 디렉토리

COPY ./backend /backend  
# 소스 복사

COPY ./requirements.txt /backend/requirements.txt  
COPY ./GeoLite2-Country.mmdb /backend/GeoLite2-Country.mmdb

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
