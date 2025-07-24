# app/commands/slack/ask.py
# Slack 명령어 /orbiton.ask 처리 - LLaMA에 질문하고 응답 반환

from fastapi.responses import PlainTextResponse
from backend.services import llama_service

# /orbiton.ask 명령어를 처리하여 LLaMA 응답 반환
async def handle_ask_command(question: str, user_name: str) -> PlainTextResponse:
    try:
        if not question.strip():
            return PlainTextResponse("❌ 질문 내용을 입력해주세요.")

        response = await llama_service.query_llama(question)

        return PlainTextResponse(
            f"💬 *{user_name}님의 질문:* {question}\n"
            f"🤖 *LLaMA 응답:* {response}"
        )

    except Exception as e:
        return PlainTextResponse(f"❌ 질문 처리 중 오류 발생: {e}")