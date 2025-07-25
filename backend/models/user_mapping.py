# backend/models/user_mapping.py
from sqlalchemy import Column, String, DateTime
from backend.database.db_session import Base
from datetime import datetime

class UserMapping(Base):
    __tablename__ = "user_mappings"

    slack_user_id = Column(String, primary_key=True, index=True)
    internal_user_id = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
