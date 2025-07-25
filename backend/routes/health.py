# backend/routes/health.py
# 시스템 헬스체크, DB 연결 상태, 사용자 및 태스크 정보 조회, 환경변수/LLM/Slack/ClickUp 상태 점검 포함

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.db_session import get_db
from backend.database import models
from backend.database.schemas import UserMappingSchema, ClickUpTaskSchema
from typing import List
# DB 생성용 임시 코드 
from backend.database.init_db import init_db, insert_sample_data

import os
import requests

router = APIRouter()

# DB 생성용 임시 코드
@router.get("/health/init")
def initialize_database():
    init_db()
    insert_sample_data()
    return {"status": "ok", "message": "DB Initialized"}

# 1. 기본 Ping
@router.get("/health/ping")
async def ping():
    return {"status": "ok", "message": "Orbiton.ai API is running."}


# 2. DB 연결 상태
@router.get("/health/db")
async def db_healthcheck(db: Session = Depends(get_db)):
    try:
        user_count = db.query(models.UserMapping).count()
        task_count = db.query(models.ClickUpTask).count()
        return {
            "status": "ok",
            "users": user_count,
            "tasks": task_count
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


# 3. 사용자 목록
@router.get("/health/users", response_model=List[UserMappingSchema])
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.UserMapping).all()


# 4. 태스크 목록
@router.get("/health/tasks", response_model=List[ClickUpTaskSchema])
async def get_all_tasks(db: Session = Depends(get_db)):
    return db.query(models.ClickUpTask).all()


# 5. 환경변수 상태
@router.get("/health/env")
async def env_check():
    env_keys = [
        "LLM_MODEL", "LLM_API_URL", "SLACK_SIGNING_SECRET", "SLACK_VERIFICATION_TOKEN",
        "SLACK_BOT_TOKEN", "CLICKUP_API_KEY", "CLICKUP_LIST_ID", "DATABASE_URL"
    ]
    return {key: "✅" if os.getenv(key) else "❌" for key in env_keys}


# 6. LLM API 연동 상태
@router.get("/health/llm")
async def llm_status():
    try:
        api_url = os.getenv("LLM_API_URL", "http://localhost:11434/api/tags")
        response = requests.get(api_url, timeout=3)
        if response.status_code == 200:
            return {
                "status": "ok",
                "message": "LLM API 연결 정상",
                "response": response.json()
            }
        return {"status": "error", "message": "LLM 응답 오류", "code": response.status_code}
    except Exception as e:
        return {"status": "error", "message": f"LLM API 연결 실패: {str(e)}"}


# 7. 현재 사용 중인 LLM 모델 이름 반환
@router.get("/health/model")
async def llm_model():
    return {
        "model": os.getenv("LLM_MODEL", "알 수 없음"),
        "llm_api_url": os.getenv("LLM_API_URL", "미설정")
    }


# 8. Slack 연동 확인
@router.get("/health/slack")
async def slack_check():
    try:
        token = os.getenv("SLACK_BOT_TOKEN")
        if not token:
            return {"status": "error", "message": "SLACK_BOT_TOKEN 누락"}

        response = requests.post(
            "https://slack.com/api/auth.test",
            headers={"Authorization": f"Bearer {token}"},
            timeout=3
        )
        data = response.json()
        if data.get("ok"):
            return {"status": "ok", "team": data.get("team"), "user": data.get("user")}
        return {"status": "error", "message": data.get("error", "Unknown error")}
    except Exception as e:
        return {"status": "error", "message": f"Slack API 호출 실패: {str(e)}"}


# 9. ClickUp 연동 상태 확인
@router.get("/health/clickup")
async def clickup_check():
    try:
        token = os.getenv("CLICKUP_API_KEY")
        if not token:
            return {"status": "error", "message": "CLICKUP_API_KEY 누락"}

        response = requests.get(
            "https://api.clickup.com/api/v2/team",
            headers={"Authorization": token},
            timeout=3
        )
        data = response.json()
        if "teams" in data:
            return {"status": "ok", "team_count": len(data["teams"])}
        return {"status": "error", "message": data.get("err", "Unknown error")}
    except Exception as e:
        return {"status": "error", "message": f"ClickUp API 호출 실패: {str(e)}"}
