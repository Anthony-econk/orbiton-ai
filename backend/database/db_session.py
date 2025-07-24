# app/database/db_session.py
# PostgreSQL 데이터베이스 세션 및 엔진 설정

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# PostgreSQL DATABASE_URL 환경변수 예시:
# postgresql://user:password@localhost:5432/orbiton_db
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL 환경변수가 설정되지 않았습니다. 예: postgresql://user:pass@host:port/dbname")

# SQLAlchemy 엔진 및 세션 설정
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# DB 세션 생성 유틸리티 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
