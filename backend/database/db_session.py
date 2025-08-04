# backend/database/db_session.py
# Orbiton.ai - PostgreSQL 세션 및 ORM 엔진 초기화

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# ✅ 환경 변수에서 DATABASE_URL 불러오기
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL 환경변수가 설정되지 않았습니다. 예: postgresql://user:pass@host:port/dbname")

# ✅ Render 환경 감지 시 SSL 설정 적용
ssl_args = {"sslmode": "require"} if "render.com" in DATABASE_URL else {}

# ✅ SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    poolclass=NullPool,  # 서버리스 환경에서 연결 유지 방지
    connect_args=ssl_args
)

# ✅ 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ ORM Base 클래스 (모든 모델에서 상속)
Base = declarative_base()

# ✅ FastAPI 의존성 주입용 DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()