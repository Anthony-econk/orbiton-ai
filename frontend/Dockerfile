# 파일 위치: orbiton-ai/frontend/Dockerfile

FROM node:20  
# Node 20 사용

WORKDIR /app  
# 작업 디렉토리

COPY package*.json ./  
# package.json 복사

RUN npm install  
# 패키지 설치

COPY . .  
# 모든 소스 복사

CMD ["npm", "run", "dev", "--", "--host"]
# 외부 접근 허용
