# app/routes/slack_command.py
# 설명: Slack 명령어를 받아 LLaMA (Ollama API)와 연동하여 응답하는 FastAPI 라우트

from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

# 환경 변수로 설정된 Ollama API Endpoint (필수)
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL")
if not OLLAMA_API_URL:
    raise EnvironmentError("OLLAMA_API_URL 환경변수가 설정되지 않았습니다.")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
if not OLLAMA_MODEL:
    raise EnvironmentError("OLLAMA_MODEL 환경변수가 설정되지 않았습니다.")

# Slack Verification Token (필수)
SLACK_VERIFICATION_TOKEN = os.getenv("SLACK_VERIFICATION_TOKEN")
if not SLACK_VERIFICATION_TOKEN:
    raise EnvironmentError("SLACK_VERIFICATION_TOKEN 환경변수가 설정되지 않았습니다.")

@backend.post("/slack/command")
async def slack_command(
    request: Request,
    token: str = Form(...),
    command: str = Form(...),
    text: str = Form(...),
    user_name: str = Form(...)
):
    """Slack에서 들어온 명령어를 처리하는 메인 핸들러"""

    if token != SLACK_VERIFICATION_TOKEN:
        return JSONResponse(status_code=403, content={"error": "Invalid Slack token"})

    if command == "/orbiton.ask":
        llama_response = await query_llama(text)
        return JSONResponse(content={
            "response_type": "in_channel",
            "text": f"*{user_name}님의 질문:* {text}\n*LLaMA 응답:* {llama_response}"
        })

    return JSONResponse(content={"text": "알 수 없는 명령어입니다."})

async def query_llama(prompt: str) -> str:
    """LLaMA API (Ollama) 호출 함수"""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(OLLAMA_API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "응답이 없습니다.")
            else:
                return "LLaMA API 호출 실패."
        except Exception as e:
            return f"LLaMA API 호출 중 예외 발생: {str(e)}"

# 실행 명령: uvicorn main:app --reload