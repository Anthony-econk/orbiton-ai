# backend/models/clickup_task.py

from datetime import datetime
from sqlalchemy import Column, String, DateTime, Index
from backend.database.db_session import Base

class ClickUpTask(Base):
    __tablename__ = "clickup_tasks"

    task_id    = Column(String, primary_key=True, index=True)
    name       = Column(String, nullable=False)
    status     = Column(String, nullable=True)
    assignee   = Column(String, nullable=True)
    due_date   = Column(String, nullable=True)
    list_id    = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_clickup_tasks_list", "list_id"),
        Index("ix_clickup_tasks_status", "status"),
        Index("ix_clickup_tasks_assignee", "assignee"),
    )

    def __repr__(self) -> str:
        return f"<ClickUpTask {self.task_id} {self.name}>"

