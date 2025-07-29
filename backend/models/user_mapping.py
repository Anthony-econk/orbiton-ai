# 파일 위치: backend/models/user_mapping.py

from sqlalchemy import Column, String, DateTime, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class UserMapping(Base):
    __tablename__ = "user_mapping"

    # 향 후 확장 가능성을 고려한 설계, 기업별 대응
    platform = Column(String(32), nullable=False)  # ex: slack, kakao, line, web
    platform_user_id = Column(String(64), nullable=False)  # ex: U123456, abcdef
    internal_user_id = Column(String(64), nullable=False)  # Orbiton.ai 내부 사용자 ID
    alias = Column(String(64), nullable=True)  # 사용자 별칭 또는 이름
    external_tool = Column(String(32), nullable=True)  # ex: clickup, jira
    external_user_id = Column(String(64), nullable=True)  # 외부 툴 사용자 ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        PrimaryKeyConstraint('platform', 'platform_user_id'),
    )
