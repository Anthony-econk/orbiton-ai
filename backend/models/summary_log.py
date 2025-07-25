# backend/models/summary_log.py
from sqlalchemy import Column, String, Text, DateTime
from backend.database.db_session import Base
from datetime import datetime

class SummaryLog(Base):
    __tablename__ = "summary_logs"

    id = Column(String, primary_key=True)
    prompt = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    model_used = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
