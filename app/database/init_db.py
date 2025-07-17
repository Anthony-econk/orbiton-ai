# app/database/init_db.py
# PostgreSQL 데이터베이스 테이블 생성 및 초기 샘플 데이터 삽입 스크립트

from app.database.db_session import engine, Base, SessionLocal
from app.database import models

# 모든 테이블 생성
def init_db():
    print("🚀 데이터베이스 테이블 생성 시작...")
    Base.metadata.create_all(bind=engine)
    print("✅ 데이터베이스 테이블 생성 완료.")

# 초기 샘플 데이터 삽입
def insert_sample_data():
    db = SessionLocal()
    try:
        # 샘플 UserMapping 데이터
        user_mapping = models.UserMapping(
            slack_user_id="U12345678",
            internal_user_id="internal_user_1"
        )
        db.add(user_mapping)

        # 샘플 ClickUpTask 데이터
        clickup_task = models.ClickUpTask(
            task_id="T123",
            name="Sample Task",
            status="진행중",
            assignee="internal_user_1",
            due_date="2025-08-01",
            list_id="L123"
        )
        db.add(clickup_task)

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