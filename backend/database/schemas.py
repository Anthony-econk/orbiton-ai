# app/database/schemas.py
# 데이터베이스 모델의 Pydantic 스키마 정의

from pydantic import BaseModel
from typing import Optional

# UserMapping 조회용 스키마
class UserMappingSchema(BaseModel):
    slack_user_id: str
    internal_user_id: str

    class Config:
        from_attributes = True

# ClickUpTask 조회용 스키마
class ClickUpTaskSchema(BaseModel):
    task_id: str
    name: str
    status: Optional[str]
    assignee: Optional[str]
    due_date: Optional[str]
    list_id: str

    class Config:
        from_attributes = True
