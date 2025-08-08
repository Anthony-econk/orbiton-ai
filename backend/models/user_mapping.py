# backend/models/user_mapping.py
from datetime import datetime
from sqlalchemy import Column, String, DateTime, PrimaryKeyConstraint, Index
from backend.database.db_session import Base  # 단일 Base 사용

# 향 후 확장 가능성을 고려한 설계, 기업별 대응
class UserMapping(Base):
    __tablename__ = "user_mappings" 

    platform = Column(String(32), nullable=False)    # ex: slack, kakao, line, web
    platform_user_id = Column(String(64), nullable=False)
    internal_user_id = Column(String(64), nullable=False)   # Orbiton.ai 내부 사용자 ID
    alias = Column(String(64), nullable=True)   # 사용자 별칭 또는 이름
    external_tool = Column(String(32), nullable=True)   # ex: clickup, jira
    external_user_id = Column(String(64), nullable=True)    # 외부 툴 사용자 ID
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("platform", "platform_user_id"),
        Index("ix_user_mappings_platform_user", "platform", "platform_user_id"),
        Index("ix_user_mappings_internal_user_id", "internal_user_id"),
    )

    def __repr__(self) -> str:
        return f"<UserMapping {self.platform}:{self.platform_user_id} -> {self.internal_user_id}>"
