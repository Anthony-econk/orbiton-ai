# backend/database/init_db.py
# 사용자 매핑 테이블 및 샘플 데이터 삽입 

from sqlalchemy.exc import IntegrityError
from backend.database.db_session import engine, Base, SessionLocal
from backend.models.user_mapping import UserMapping
from datetime import datetime
from backend.utils.logger import logger
import traceback

def init_db():
    try:
        logger.info("🚀 user_mapping 테이블 생성 시작...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ user_mapping 테이블 생성 완료.")
    except Exception as e:
        logger.error("❌ 테이블 생성 실패")
        logger.debug(traceback.format_exc())

def create_sample_user_mappings(db):
    try:
        logger.info("🚀 샘플 사용자 매핑 삽입 시작...")

        users = [
            UserMapping(
                platform="slack",
                platform_user_id="U12345678",
                internal_user_id="user_001",
                alias="기혁",
                external_tool="clickup",
                external_user_id="cu_98765",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            UserMapping(
                platform="kakao",
                platform_user_id="abc_56789",
                internal_user_id="user_001",
                alias="기혁",
                external_tool="clickup",
                external_user_id="cu_98765",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]

        for user in users:
            db.merge(user)

        logger.info("✅ 샘플 사용자 매핑 UPSERT 완료.")

    except Exception as e:
        logger.error("❌ 샘플 사용자 삽입 실패")
        logger.debug(traceback.format_exc())
        raise

def insert_sample_data():
    db = SessionLocal()
    try:
        create_sample_user_mappings(db)
        db.commit()
        logger.info("✅ 초기 샘플 데이터 커밋 완료.")
    except IntegrityError as ie:
        db.rollback()
        logger.error(f"❌ 중복 데이터 오류 발생: {ie}")
    except Exception as e:
        db.rollback()
        logger.error("❌ 데이터 삽입 실패, 롤백 수행")
        logger.debug(traceback.format_exc())
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    insert_sample_data()
