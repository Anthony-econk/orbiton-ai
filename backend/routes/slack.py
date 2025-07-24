# backend/routes/slack.py
# Slack 명령어 라우터 - 보안, 검증, 로깅 강화

from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse
from backend.commands.slack import ask, summary, tasklist, mytask, assign, deadline, update, status, delete
from backend.utils.logger import logger
import os
import hmac
import hashlib
import time
import re

router = APIRouter()

# 환경변수 로딩 (점검을 위해 잠시 주석 처리 250724)
#SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
#SLACK_VERIFICATION_TOKEN = os.getenv("SLACK_VERIFICATION_TOKEN")

#if not SLACK_SIGNING_SECRET or not SLACK_VERIFICATION_TOKEN:
#    raise EnvironmentError("SLACK_SIGNING_SECRET 또는 SLACK_VERIFICATION_TOKEN 환경변수가 설정되지 않았습니다.")

# 오류를 찾기 위한 임시 테스트용 250724
def get_slack_secrets():
    signing_secret = os.getenv("SLACK_SIGNING_SECRET")
    verification_token = os.getenv("SLACK_VERIFICATION_TOKEN")
    if not signing_secret or not verification_token:
        raise EnvironmentError("SLACK 관련 환경변수가 설정되지 않았습니다.")
    return signing_secret, verification_token

SLACK_SIGNING_SECRET, SLACK_VERIFICATION_TOKEN = get_slack_secrets()




# Slack Signature 검증 함수
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

# 텍스트 정규화
def sanitize_input(text: str, max_length: int = 500) -> str:
    text = re.sub(r'[<>]', '', text)
    return text.strip()[:max_length]

# Slack 명령어 라우팅
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
        match command:
            case "/orbiton.ask":
                return await ask.handle_ask_command(text, user_name)
            case "/orbiton.summary":
                return await summary.handle_summary_command(list_id)
            case "/orbiton.tasklist":
                return await tasklist.handle_tasklist_command(list_id)
            case "/orbiton.mytask":
                return await mytask.handle_mytask_command(list_id, user_id)
            case "/orbiton.assign":
                return await assign.handle_assign_command(list_id, text, user_name)
            case "/orbiton.deadline":
                return await deadline.handle_deadline_command(list_id, text, user_name)
            case "/orbiton.update":
                return await update.handle_update_command(list_id, text, user_name)
            case "/orbiton.status":
                return await status.handle_status_command(list_id, text, user_name)
            case "/orbiton.delete":
                return await delete.handle_delete_command(list_id, text, user_name)
            case _:
                return JSONResponse(content={"text": "❌ 지원하지 않는 명령어입니다."})

    except Exception as e:
        logger.error(f"Slack command processing error: {e}")
        return JSONResponse(content={"text": f"❌ 명령어 처리 중 오류가 발생했습니다: {e}"})
