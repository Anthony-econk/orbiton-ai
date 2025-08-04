# frontend/Dockerfile  
# Orbiton.ai - Vite 기반 프론트엔드 Dockerfile

FROM node:20  
# Node.js 20 LTS 이미지 사용

WORKDIR /frontend  
# 프론트엔드 작업 디렉토리 설정

COPY ./frontend/package*.json ./  
# 루트의 frontend/package.json 파일 복사

RUN npm install  
# 프론트엔드 패키지 설치

COPY ./frontend ./  
# 전체 frontend 소스 복사

CMD ["npm", "run", "dev", "--", "--host"]  
# Vite 개발 서버 실행
