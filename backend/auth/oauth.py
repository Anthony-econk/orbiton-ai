# app/auth/oauth.py
# Slack OAuth 및 인증 관련 유틸리티 모듈

import os
import httpx

SLACK_OAUTH_ACCESS_URL = "https://slack.com/api/oauth.v2.access"
SLACK_CLIENT_ID = os.getenv("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET")

if not SLACK_CLIENT_ID or not SLACK_CLIENT_SECRET:
    raise EnvironmentError("SLACK_CLIENT_ID 또는 SLACK_CLIENT_SECRET 환경변수가 설정되지 않았습니다.")

# Slack OAuth 인증 코드를 통해 액세스 토큰 획득
async def exchange_code_for_token(code: str, redirect_uri: str) -> dict:
    payload = {
        "client_id": SLACK_CLIENT_ID,
        "client_secret": SLACK_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SLACK_OAUTH_ACCESS_URL, data=payload)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            return {"ok": False, "error": f"Request error: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"ok": False, "error": f"HTTP error: {str(e)}"}