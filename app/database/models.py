# app/database/models.py
# 데이터베이스 모델 정의 - 운영 제품용 완성형

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from app.database.db_session import Base

# Slack 사용자와 내부 사용자 매핑 모델
class UserMapping(Base):
    __tablename__ = 'user_mapping'

    id = Column(Integer, primary_key=True, autoincrement=True)
    slack_user_id = Column(String, unique=True, nullable=False)
    internal_user_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ClickUp 태스크 저장 모델 (완성형)
class ClickUpTask(Base):
    __tablename__ = 'clickup_tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    assignee = Column(String, nullable=True)
    due_date = Column(String, nullable=True)
    list_id = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
