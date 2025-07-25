# backend/models/command_log.py
from sqlalchemy import Column, String, Text, DateTime
from backend.database.db_session import Base
from datetime import datetime

class CommandLog(Base):
    __tablename__ = "command_logs"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    command = Column(String, nullable=False)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
