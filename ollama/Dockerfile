# orbiton-ai/ollama/Dockerfile

FROM ollama/ollama:latest  
# Ollama 공식 이미지 기반

WORKDIR /ollama  
# 명시적 작업 디렉토리 설정 (필수는 아니지만 구조화 목적)

# 모델 다운로드는 컨테이너 실행 후 수동 실행해야 함 (빌드 시 불가능)
# RUN ollama pull llama3

EXPOSE 11434  
# Ollama 기본 포트 노출

CMD ["serve"]  
# Ollama 서버 실행
