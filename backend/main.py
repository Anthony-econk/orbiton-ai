# app/main.py
# Orbiton.ai FastAPI 메인 서버 진입점 - 라우터, CORS, 로깅, 예외 핸들러, 지역 접근 제어 설계 포함

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.routes import slack, health
from backend.utils.logger import logger
import geoip2.database
import os

app = FastAPI(title="Orbiton.ai API", version="1.0")

# CORS 설정 (모든 출처 허용)
backend.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
backend.include_router(health.router, prefix="/api")
backend.include_router(slack.router, prefix="/api")

# 지역 접근 제어 (GeoIP 데이터베이스 필요)
GEOIP_DB_PATH = os.getenv("GEOIP_DB_PATH", "GeoLite2-Country.mmdb")
ALLOWED_COUNTRIES = os.getenv("ALLOWED_COUNTRIES", "KR,US,JP").split(',')

try:
    geoip_reader = geoip2.database.Reader(GEOIP_DB_PATH)
except Exception as e:
    geoip_reader = None
    logger.warning(f"GeoIP 데이터베이스 로드 실패: {e}")

@backend.middleware("http")
async def geoip_restriction(request: Request, call_next):
    if geoip_reader:
        client_ip = request.client.host
        try:
            response = geoip_reader.country(client_ip)
            country_code = response.country.iso_code
            if country_code not in ALLOWED_COUNTRIES:
                logger.warning(f"접근 차단 - IP: {client_ip}, 국가: {country_code}")
                return JSONResponse(status_code=403, content={"error": "해당 지역에서는 접근이 제한됩니다."})
        except Exception as e:
            logger.error(f"GeoIP 확인 실패: {e}")

    return await call_next(request)

# 글로벌 예외 핸들러
@backend.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"예기치 못한 오류 발생: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "서버 내부 오류가 발생했습니다. 관리자에게 문의하세요."}
    )

@backend.on_event("startup")
async def startup_event():
    logger.info("🚀 Orbiton.ai API 서버가 시작되었습니다.")

@backend.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Orbiton.ai API 서버가 종료되었습니다.")