# backend/routes/slack.py
# Slack 명령어 라우터 - 보안 검증 + 명령 처리 + 확장성 고려 통합버전

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from backend.commands.slack import ask, summary, tasklist, mytask, assign, deadline, update, status, delete
from backend.utils.logger import logger
from urllib.parse import urlencode  # ✅  오류 방지용. [선언문]
import os
import hmac
import hashlib
import time
import re

router = APIRouter()

# ✅ 환경변수 로딩 함수
def get_slack_secrets():
    signing_secret = os.getenv("SLACK_SIGNING_SECRET")
    verification_token = os.getenv("SLACK_VERIFICATION_TOKEN")
    if not signing_secret or not verification_token:
        raise EnvironmentError("SLACK 관련 환경변수가 설정되지 않았습니다.")
    return signing_secret, verification_token

# ✅ Slack Signature 검증 함수
def verify_slack_request(request: Request, body: str) -> bool:
    try:
        signing_secret, _ = get_slack_secrets()
    except Exception as e:
        logger.error(f"환경변수 로딩 실패: {e}")
        return False

    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    slack_signature = request.headers.get("X-Slack-Signature")

    if not timestamp or not slack_signature:
        logger.warning("Slack signature headers 누락")
        return False

    if abs(time.time() - int(timestamp)) > 60 * 5:
        logger.warning("Slack 요청 시간이 너무 지남")
        return False

    sig_basestring = f"v0:{timestamp}:{body}"
    my_signature = 'v0=' + hmac.new(
        signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(my_signature, slack_signature)

# ✅ 입력 정규화 함수
def sanitize_input(text: str, max_length: int = 500) -> str:
    return re.sub(r'[<>]', '', text).strip()[:max_length]

# ✅ Slack 명령어 라우터
@router.post("/slack/command")
async def handle_slack_command(request: Request):
    form = await request.form()

    token = form.get("token")
    command = form.get("command")
    text = form.get("text")
    user_name = form.get("user_name")
    user_id = form.get("user_id")
    channel_id = form.get("channel_id")

    body = urlencode(form)  # ✅ 정확한 Slack 서명 검증용 포맷

    if not verify_slack_request(request, body):
        logger.warning(f"Slack Signature 검증 실패 - 사용자: {user_id}")
        return JSONResponse(status_code=403, content={"error": "Invalid Slack signature"})

    try:
        _, verification_token = get_slack_secrets()
    except Exception as e:
        logger.error(f"환경변수 로딩 오류: {e}")
        return JSONResponse(status_code=500, content={"error": "서버 설정 오류"})

    if token != verification_token:
        logger.warning(f"Slack Token 불일치 - 사용자: {user_id}")
        return JSONResponse(status_code=403, content={"error": "Invalid Slack token"})

    list_id = os.getenv("CLICKUP_LIST_ID", "")
    clean_text = sanitize_input(text)

    try:
        match command:
            case "/orbiton.ask":
                return await ask.handle_ask_command(clean_text, user_name)
            case "/orbiton.summary":
                return await summary.handle_summary_command(list_id)
            case "/orbiton.tasklist":
                return await tasklist.handle_tasklist_command(list_id)
            case "/orbiton.mytask":
                return await mytask.handle_mytask_command(list_id, user_id)
            case "/orbiton.assign":
                return await assign.handle_assign_command(list_id, clean_text, user_name)
            case "/orbiton.deadline":
                return await deadline.handle_deadline_command(list_id, clean_text, user_name)
            case "/orbiton.update":
                return await update.handle_update_command(list_id, clean_text, user_name)
            case "/orbiton.status":
                return await status.handle_status_command(list_id, clean_text, user_name)
            case "/orbiton.delete":
                return await delete.handle_delete_command(list_id, clean_text, user_name)
            case _:
                logger.info(f"지원하지 않는 명령어 호출됨: {command}")
                return JSONResponse(content={"text": "❌ 지원하지 않는 명령어입니다."})
    except Exception as e:
        logger.error(f"Slack 명령어 처리 중 오류: {e}")
        return JSONResponse(content={"text": f"❌ 처리 중 오류 발생: {e}"})
