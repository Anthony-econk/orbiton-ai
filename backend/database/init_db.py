# backend/database/init_db.py
# 데이터베이스 초기화 및 샘플 데이터 삽입 (Codex 스타일 설계)

from backend.database.db_session import engine, Base, SessionLocal
from backend import models
from backend.utils.logger import logger
from sqlalchemy.exc import IntegrityError
import traceback

def init_db():
    logger.info("🚀 데이터베이스 테이블 생성 시작...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ 데이터베이스 테이블 생성 완료.")

def create_sample_users(db):
    user = models.UserMapping(
        slack_user_id="U12345678",
        internal_user_id="user_001"
    )
    db.merge(user)  # 중복 방지용 UPSERT

def create_sample_tasks(db):
    task = models.ClickUpTask(
        task_id="T001",
        name="Orbiton Slack 연동 개선",
        status="진행중",
        assignee="user_001",
        due_date="2025-08-01",
        list_id="L456"
    )
    db.merge(task)

def create_sample_logs(db):
    cmd_log = models.CommandLog(
        id="cmd_001",
        user_id="U12345678",
        command="/orbiton.assign",
        text="Slack 연동 기능 점검"
    )
    summary_log = models.SummaryLog(
        id="sum_001",
        prompt="태스크 목록 요약해줘",
        result="1. Slack 연동 진행 중\n2. ClickUp API 정상 동작",
        model_used="llama3-8b"
    )
    db.merge(cmd_log)
    db.merge(summary_log)

def insert_sample_data():
    db = SessionLocal()
    try:
        create_sample_users(db)
        create_sample_tasks(db)
        create_sample_logs(db)
        db.commit()
        logger.info("✅ 초기 샘플 데이터 삽입 완료.")
    except IntegrityError as ie:
        db.rollback()
        logger.error(f"❌ 중복 데이터 오류: {ie}")
    except Exception as e:
        db.rollback()
        logger.error(f"❌ 샘플 데이터 삽입 실패: {e}")
        logger.debug(traceback.format_exc())
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    insert_sample_data()
