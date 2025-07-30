# orbiton.ai/frontend/Dockerfile

FROM node:20  
# Node.js 20 이미지

WORKDIR /frontend  
# 실제 폴더명 기준

COPY ./frontend/package*.json ./  
RUN npm install

COPY ./frontend .  
# 소스 전체 복사

CMD ["npm", "run", "dev", "--", "--host"]
