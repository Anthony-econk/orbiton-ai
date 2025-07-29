# orbiton-ai/frontend/Dockerfile

FROM node:20  
# Node.js 20 이미지 사용

WORKDIR /frontend  
# 작업 디렉토리를 /frontend로 설정

COPY ./frontend/package*.json ./  
# package.json 및 lock 파일 복사

RUN npm install  
# 의존성 설치

COPY ./frontend .  
# 소스 전체 복사

CMD ["npm", "run", "dev", "--", "--host"]
# 외부 접근 허용을 위한 dev 서버 실행
