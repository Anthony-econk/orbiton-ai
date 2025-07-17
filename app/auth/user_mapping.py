# app/auth/user_mapping.py
# Slack 사용자와 내부 시스템 사용자 매핑 (DB 기반)

from typing import Optional
from app.database.db_session import SessionLocal
from app.database.models import UserMapping

# Slack 사용자 ID를 내부 시스템 사용자 ID로 DB에서 조회
def map_slack_to_internal_user(slack_user_id: str) -> Optional[str]:
    session = SessionLocal()
    try:
        user_mapping = session.query(UserMapping).filter_by(slack_user_id=slack_user_id).first()
        if user_mapping:
            return user_mapping.internal_user_id
        return None
    finally:
        session.close()
