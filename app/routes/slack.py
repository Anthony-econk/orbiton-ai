# app/routes/slack.py
# Slack 명령어 라우터 - 보안, 검증, 로깅 강화

from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse
from app.commands.slack import ask, summary, tasklist, mytask, assign, deadline, update, status, delete
from app.utils.logger import logger
import os
import hmac
import hashlib
import time
import re

router = APIRouter()

SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_VERIFICATION_TOKEN = os.getenv("SLACK_VERIFICATION_TOKEN")

if not SLACK_SIGNING_SECRET or not SLACK_VERIFICATION_TOKEN:
    raise EnvironmentError("SLACK_SIGNING_SECRET 또는 SLACK_VERIFICATION_TOKEN 환경변수가 설정되지 않았습니다.")

# Slack 요청 Signature 검증
def verify_slack_request(request: Request, body: bytes) -> bool:
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    slack_signature = request.headers.get("X-Slack-Signature")

    if not timestamp or not slack_signature:
        logger.warning("Slack signature headers missing.")
        return False

    if abs(time.time() - int(timestamp)) > 60 * 5:
        logger.warning("Slack request timestamp too old.")
        return False

    sig_basestring = f"v0:{timestamp}:{body.decode('utf-8')}"
    my_signature = 'v0=' + hmac.new(
        SLACK_SIGNING_SECRET.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(my_signature, slack_signature)

# 입력값 정규화 및 길이 제한
def sanitize_input(text: str, max_length: int = 500) -> str:
    text = re.sub(r'[<>]', '', text)
    return text.strip()[:max_length]

@router.post("/slack/command")
async def handle_slack_command(
    request: Request,
    token: str = Form(...),
    command: str = Form(...),
    text: str = Form(...),
    user_name: str = Form(...),
    user_id: str = Form(...),
    channel_id: str = Form(...)
):
    body = await request.body()
    if not verify_slack_request(request, body):
        logger.warning(f"Invalid Slack signature from user: {user_id}")
        return JSONResponse(status_code=403, content={"error": "Invalid Slack signature"})

    if token != SLACK_VERIFICATION_TOKEN:
        logger.warning(f"Invalid Slack token attempt by user: {user_id}")
        return JSONResponse(status_code=403, content={"error": "Invalid Slack token"})

    list_id = os.getenv("CLICKUP_LIST_ID")
    text = sanitize_input(text)

    try:
        if command == "/orbiton.ask":
            return await ask.handle_ask_command(text, user_name)

        elif command == "/orbiton.summary":
            return await summary.handle_summary_command(list_id)

        elif command == "/orbiton.tasklist":
            return await tasklist.handle_tasklist_command(list_id)

        elif command == "/orbiton.mytask":
            return await mytask.handle_mytask_command(list_id, user_id)

        elif command == "/orbiton.assign":
            return await assign.handle_assign_command(list_id, text, user_name)

        elif command == "/orbiton.deadline":
            return await deadline.handle_deadline_command(list_id, text, user_name)

        elif command == "/orbiton.update":
            return await update.handle_update_command(list_id, text, user_name)

        elif command == "/orbiton.status":
            return await status.handle_status_command(list_id, text, user_name)

        elif command == "/orbiton.delete":
            return await delete.handle_delete_command(list_id, text, user_name)

        return JSONResponse(content={"text": "❌ 지원하지 않는 명령어입니다."})

    except Exception as e:
        logger.error(f"Slack command processing error: {e}")
        return JSONResponse(content={"text": f"❌ 명령어 처리 중 오류가 발생했습니다: {e}"})