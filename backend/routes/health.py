# backend/routes/health.py
# 시스템 상태 모니터링 API - 고급 구조 기반 리팩토링

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Dict
import os
import requests

from backend.database.db_session import get_db
from backend.models import UserMapping, ClickUpTask
from backend.database.schemas import UserMappingSchema, ClickUpTaskSchema
from backend.utils.logger import logger
from backend.database.init_db import init_db, insert_sample_data

router = APIRouter(prefix="/health", tags=["Health"])

# ✅ 0. DB 초기화용 엔드포인트 (운영 배포 시 제거 권장)
# DB 초기화 후 주석처리 * Render shell을 사용하려면 월 정기구매 해야 해서 
# 간접 방법으로 DB Table 초기생성작업 250725
# @router.get("/init", summary="DB 초기화")
# def initialize_database():
#     try:
#         init_db()
#         insert_sample_data()
#         return {"status": "ok", "message": "DB Initialized"}
#     except Exception as e:
#         logger.error(f"DB 초기화 실패: {e}")
#         return {"status": "error", "message": str(e)}

# ✅ 1. 기본 핑 테스트
@router.get("/ping", summary="기본 헬스 체크")
def ping():
    return {"status": "ok", "message": "Orbiton.ai API is running."}

# ✅ 2. DB 연결 및 레코드 수 체크
@router.get("/db", summary="DB 연결 확인")
def db_healthcheck(db: Session = Depends(get_db)):
    try:
        return {
            "status": "ok",
            "users": db.query(UserMapping).count(),
            "tasks": db.query(ClickUpTask).count()
        }
    except Exception as e:
        logger.error(f"DB 오류: {e}")
        return {"status": "error", "message": str(e)}

# ✅ 3. 전체 사용자 조회
@router.get("/users", response_model=List[UserMappingSchema], summary="전체 사용자 조회")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(UserMapping).all()

# ✅ 4. 전체 태스크 조회
@router.get("/tasks", response_model=List[ClickUpTaskSchema], summary="전체 태스크 조회")
def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(ClickUpTask).all()

# ✅ 5. 환경 변수 상태 확인
@router.get("/env", summary="환경 변수 설정 상태 점검")
def env_check() -> Dict[str, str]:
    keys = [
        "LLM_MODEL", "LLM_API_URL", "SLACK_SIGNING_SECRET",
        "SLACK_VERIFICATION_TOKEN", "SLACK_BOT_TOKEN",
        "CLICKUP_API_KEY", "CLICKUP_LIST_ID", "DATABASE_URL"
    ]
    return {k: "✅" if os.getenv(k) else "❌" for k in keys}

# ✅ 6. LLM API 응답 확인
@router.get("/llm", summary="LLM API 상태 확인")
def llm_status():
    try:
        url = os.getenv("LLM_API_URL", "http://localhost:11434/api/tags")
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            return {"status": "ok", "response": res.json()}
        return {"status": "error", "code": res.status_code}
    except Exception as e:
        return {"status": "error", "message": f"LLM API 연결 실패: {e}"}

# ✅ 7. 사용 중인 LLM 모델 정보
@router.get("/model", summary="LLM 모델 정보")
def llm_model():
    return {
        "model": os.getenv("LLM_MODEL", "미설정"),
        "llm_api_url": os.getenv("LLM_API_URL", "미설정")
    }

# ✅ 8. Slack API 연동 상태
@router.get("/slack", summary="Slack 연동 확인")
def slack_check():
    try:
        token = os.getenv("SLACK_BOT_TOKEN")
        if not token:
            return {"status": "error", "message": "SLACK_BOT_TOKEN 누락"}

        res = requests.post(
            "https://slack.com/api/auth.test",
            headers={"Authorization": f"Bearer {token}"},
            timeout=3
        )
        data = res.json()
        if data.get("ok"):
            return {"status": "ok", "team": data.get("team"), "user": data.get("user")}
        return {"status": "error", "message": data.get("error", "Slack 오류")}
    except Exception as e:
        return {"status": "error", "message": f"Slack API 오류: {e}"}

# ✅ 9. ClickUp 연동 상태
@router.get("/clickup", summary="ClickUp 연동 상태")
def clickup_check():
    try:
        token = os.getenv("CLICKUP_API_KEY")
        if not token:
            return {"status": "error", "message": "CLICKUP_API_KEY 누락"}

        res = requests.get(
            "https://api.clickup.com/api/v2/team",
            headers={"Authorization": token},
            timeout=3
        )
        data = res.json()
        if "teams" in data:
            return {"status": "ok", "team_count": len(data["teams"])}
        return {"status": "error", "message": data.get("err", "ClickUp 오류")}
    except Exception as e:
        return {"status": "error", "message": f"ClickUp API 오류: {e}"}
