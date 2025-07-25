# backend/models/clickup_task.py
from sqlalchemy import Column, String, DateTime
from backend.database.db_session import Base
from datetime import datetime

class ClickUpTask(Base):
    __tablename__ = "clickup_tasks"

    task_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    assignee = Column(String, nullable=False)
    due_date = Column(String)
    list_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
