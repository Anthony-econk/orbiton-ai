# 파일 위치: orbiton.ai/frontend/Dockerfile

FROM node:20  
# Node.js 20 LTS 사용 (보수적 안정 버전)

WORKDIR /frontend  
# 프론트엔드 작업 디렉토리

COPY ./frontend/package*.json .  

RUN npm install  

COPY . .  

CMD ["npm", "run", "dev", "--", "--host"]  
# 개발 서버 실행
