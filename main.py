from fastapi import FastAPI, Request
import os
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.signature import SignatureVerifier

app = FastAPI()

slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
slack_client = AsyncWebClient(token=slack_bot_token)
verifier = SignatureVerifier(signing_secret=slack_signing_secret)

@app.post("/slack/events")
async def slack_events(request: Request):
    body = await request.body()
    if not verifier.is_valid_request(body, request.headers):
        return {"error": "invalid request"}

    payload = await request.json()
    # 여기에 명령어 처리 로직 추가 예정
    return {"ok": True}
