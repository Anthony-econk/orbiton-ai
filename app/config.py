# app/config.py
# 환경변수 및 설정값 로딩 모듈

import os

# Slack 관련 설정
SLACK_VERIFICATION_TOKEN = os.getenv("SLACK_VERIFICATION_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

# LLaMA API 설정
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# ClickUp API 설정
CLICKUP_API_URL = os.getenv("CLICKUP_API_URL", "https://api.clickup.com/api/v2")
CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")

# 필수 환경변수 체크 함수
def validate_env():
    required_vars = {
        "SLACK_VERIFICATION_TOKEN": SLACK_VERIFICATION_TOKEN,
        "SLACK_BOT_TOKEN": SLACK_BOT_TOKEN,
        "OLLAMA_API_URL": OLLAMA_API_URL,
        "OLLAMA_MODEL": OLLAMA_MODEL,
        "CLICKUP_API_KEY": CLICKUP_API_KEY,
        "CLICKUP_LIST_ID": CLICKUP_LIST_ID
    }
    for var_name, value in required_vars.items():
        if not value:
            raise EnvironmentError(f"환경변수 {var_name} 가 설정되지 않았습니다.")

# 모듈 로드 시 환경변수 검증
validate_env()
