# app/services/slack_service.py
# Slack API 호출을 담당하는 서비스 모듈

import os
import httpx

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_API_URL = "https://slack.com/api/chat.postMessage"

if not SLACK_BOT_TOKEN:
    raise EnvironmentError("SLACK_BOT_TOKEN 환경변수가 설정되지 않았습니다.")

# Slack 채널에 메시지를 전송하는 함수
async def send_message(channel: str, text: str) -> bool:
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SLACK_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("ok", False)
        except httpx.RequestError:
            return False
        except httpx.HTTPStatusError:
            return False