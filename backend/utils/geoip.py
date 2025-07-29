# backend/routes/health.py

from fastapi import APIRouter
from backend.utils.geoip_policy import ALLOW_ALL_COUNTRIES, ALLOWED_COUNTRIES, is_country_blocked
import geoip2.database
import os

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/ping")
def ping():
    return {"status": "ok"}

@router.get("/geoip")
def geoip_status():
    GEOIP_DB_PATH = os.getenv("GEOIP_DB_PATH", "GeoLite2-Country.mmdb")
    status = {}
    try:
        reader = geoip2.database.Reader(GEOIP_DB_PATH)
        test_ip = "8.8.8.8"  # Google DNS (미국)
        response = reader.country(test_ip)
        country_code = response.country.iso_code
        blocked = is_country_blocked(country_code)
        status["geoip_db_loaded"] = True
        status["test_ip"] = test_ip
        status["country_code"] = country_code
        status["is_blocked"] = blocked
    except Exception as e:
        status["geoip_db_loaded"] = False
        status["error"] = str(e)

    # 접근 정책 정보 반환
    status["policy"] = {
        "ALLOW_ALL_COUNTRIES": ALLOW_ALL_COUNTRIES,
        "ALLOWED_COUNTRIES": ALLOWED_COUNTRIES
    }
    return status
