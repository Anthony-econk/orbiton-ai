# app/routes/health.py
# 시스템 헬스체크, DB 연결 테스트, 사용자 매핑 및 태스크 목록 조회 라우터

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.db_session import get_db
from backend.database import models
from backend.database.schemas import UserMappingSchema, ClickUpTaskSchema
from typing import List

router = APIRouter()

@router.get("/health/ping")
async def ping():
    return {"status": "ok", "message": "Orbiton.ai API is running."}

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

@router.get("/health/users", response_model=List[UserMappingSchema])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.UserMapping).all()
    return users

@router.get("/health/tasks", response_model=List[ClickUpTaskSchema])
async def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.ClickUpTask).all()
    return tasks