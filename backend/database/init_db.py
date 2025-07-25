# backend/database/init_db.py
from backend.database.db_session import engine, Base, SessionLocal
from backend import models

def init_db():
    print("🚀 데이터베이스 테이블 생성 시작...")
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블 생성 완료.")

def insert_sample_data():
    db = SessionLocal()
    try:
        # UserMapping 샘플
        user_mapping = models.UserMapping(
            slack_user_id="U12345678",
            internal_user_id="user_001"
        )
        db.add(user_mapping)

        # ClickUpTask 샘플
        clickup_task = models.ClickUpTask(
            task_id="T001",
            name="Orbiton Slack 연동 개선",
            status="진행중",
            assignee="user_001",
            due_date="2025-08-01",
            list_id="L456"
        )
        db.add(clickup_task)

        # CommandLog 샘플
        cmd = models.CommandLog(
            id="cmd_001",
            user_id="U12345678",
            command="/orbiton.assign",
            text="Slack 연동 기능 점검"
        )
        db.add(cmd)

        # SummaryLog 샘플
        summary = models.SummaryLog(
            id="sum_001",
            prompt="태스크 목록 요약해줘",
            result="1. Slack 연동 진행 중\n2. ClickUp API 정상 동작",
            model_used="llama3-8b"
        )
        db.add(summary)

        db.commit()
        print("✅ 초기 샘플 데이터 삽입 완료.")
    except Exception as e:
        db.rollback()
        print(f"❌ 샘플 데이터 삽입 실패: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    insert_sample_data()
