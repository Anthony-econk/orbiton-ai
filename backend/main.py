# backend/main.py
# Orbiton.ai FastAPI 메인 서버 진입점 - Lifespan 기반 초기화, GeoIP 정책, 라우팅, 예외 처리 포함

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from backend.routes import slack, health
from backend.utils.logger import logger
from backend.utils.geoip_policy import is_country_blocked
import geoip2.database
import os

geoip_reader = None

# ✅ Lifespan 이벤트 핸들러로 초기화 및 종료 로직 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    global geoip_reader

    logger.info("🔄 Lifespan startup 시작 - Orbiton.ai API 서버 준비 중...")
    
    # GeoIP 초기화
    geoip_db_path = os.getenv("GEOIP_DB_PATH", "GeoLite2-Country.mmdb")
    try:
        geoip_reader = geoip2.database.Reader(geoip_db_path)
        logger.info(f"✅ GeoIP DB 로드 완료: {geoip_db_path}")
    except Exception as e:
        geoip_reader = None
        logger.warning(f"⚠️ GeoIP 데이터베이스 로드 실패: {e}")

    yield  # 앱 실행 시작

    logger.info("🛑 Lifespan shutdown 시작 - Orbiton.ai API 종료 중...")
    if geoip_reader:
        geoip_reader.close()
        logger.info("✅ GeoIP 리더 종료 완료")

# ✅ FastAPI 인스턴스 생성
app = FastAPI(
    title="Orbiton.ai API",
    version="1.0",
    lifespan=lifespan
)

# ✅ CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 라우터 등록
app.include_router(health.router, prefix="/api")
app.include_router(slack.router, prefix="/api")

# ✅ 지역 접근 제어 미들웨어
ALLOWED_COUNTRIES = os.getenv("ALLOWED_COUNTRIES", "KR,US,JP").split(',')

@app.middleware("http")
async def geoip_restriction(request: Request, call_next):
    if geoip_reader:
        client_ip = request.client.host
        try:
            response = geoip_reader.country(client_ip)
            country_code = response.country.iso_code
            if is_country_blocked(country_code):
                logger.warning(f"접근 차단 - IP: {client_ip}, 국가: {country_code}")
                return JSONResponse(status_code=403, content={"error": "해당 지역에서는 접근이 제한됩니다."})
        except Exception as e:
            logger.error(f"GeoIP 확인 실패: {e}")
    return await call_next(request)

# ✅ 글로벌 예외 핸들러
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"예기치 못한 오류 발생: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "서버 내부 오류가 발생했습니다. 관리자에게 문의하세요."}
    )