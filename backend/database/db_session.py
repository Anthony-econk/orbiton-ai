# backend/database/db_session.py
# 데이터베이스 세션 및 엔진 초기화 모듈

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import os

# 환경 변수에서 DATABASE_URL 로딩
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL 환경변수가 설정되지 않았습니다. 예: postgresql://user:pass@host:port/dbname")

# PostgreSQL 연결 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    poolclass=NullPool,  # Render 배포환경에서 연결 풀 유지 방지
    connect_args={"sslmode": "require"} if "render.com" in DATABASE_URL else {}
)

# 세션 팩토리 정의
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ORM 모델 Base 클래스
Base = declarative_base()

# 의존성 주입용 세션 생성기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# DATABASE_URL 미설정 시 예외 발생
# Render 환경 자동 감지하여 sslmode=require 설정
# NullPool 사용으로 서버리스 환경에서 연결 문제 방지
# ORM 기반 확장 가능한 구조