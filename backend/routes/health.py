# backend/routes/health.py
# 시스템 상태 모니터링 API - 안정화 리팩토링 (Render/로컬 호환 강화)

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Dict
import os
import requests
import geoip2.database

from backend.database.db_session import get_db
# 모델 import 경로를 명시적으로 분리(환경간 차이 최소화)
try:
    from backend.models.user_mapping import UserMapping
    from backend.models.clickup_task import ClickUpTask
except Exception:
    # 기존 통합 import 경로도 시도 (프로젝트 구조 차이 대응)
    from backend.models import UserMapping, ClickUpTask  # type: ignore

from backend.database.schemas import UserMappingSchema, ClickUpTaskSchema
from backend.utils.logger import logger
from backend.utils.geoip_policy import ALLOW_ALL_COUNTRIES, ALLOWED_COUNTRIES, is_country_blocked

router = APIRouter(prefix="/health", tags=["Health"])

# 1) 핑
@router.get("/ping", summary="기본 헬스 체크")
def ping():
    return {"status": "ok", "message": "Orbiton.ai API is running."}

# 2) DB 연결/카운트
@router.get("/db", summary="DB 연결 확인")
def db_healthcheck(db: Session = Depends(get_db)):
    try:
        return {
            "status": "ok",
            "users": db.query(UserMapping).count(),
            "tasks": db.query(ClickUpTask).count()
        }
    except Exception as e:
        logger.error(f"DB 오류: {e}")
        return {"status": "error", "message": str(e)}

# 3) 사용자 리스트
@router.get("/users", response_model=List[UserMappingSchema], summary="전체 사용자 조회")
def get_all_users(db: Session = Depends(get_db)):
    try:
        return db.query(UserMapping).all()
    except Exception as e:
        logger.error(f"/users 조회 실패: {e}")
        return []

# 4) 태스크 리스트
@router.get("/tasks", response_model=List[ClickUpTaskSchema], summary="전체 태스크 조회")
def get_all_tasks(db: Session = Depends(get_db)):
    try:
        return db.query(ClickUpTask).all()
    except Exception as e:
        logger.error(f"/tasks 조회 실패: {e}")
        return []

# 5) 환경 변수 상태
@router.get("/env", summary="환경 변수 설정 상태 점검")
def env_check() -> Dict[str, str]:
    keys = [
        "LLM_MODEL", "LLM_API_URL", "SLACK_SIGNING_SECRET",
        "SLACK_VERIFICATION_TOKEN", "SLACK_BOT_TOKEN",
        "CLICKUP_API_KEY", "CLICKUP_LIST_ID", "DATABASE_URL",
        "GEOIP_DB_PATH"  # ✅ 추가
    ]
    out: Dict[str, str] = {}
    for k in keys:
        v = os.getenv(k)
        out[k] = f"✅ ({v})" if v else "❌"
    return out

# 6) LLM API 상태
@router.get("/llm", summary="LLM API 상태 확인")
def llm_status():
    url = os.getenv("LLM_API_URL", "").strip()
    if not url:
        return {"status": "error", "message": "LLM_API_URL 미설정"}

    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            return {"status": "ok", "response": res.json()}
        return {"status": "error", "code": res.status_code, "url": url}
    except Exception as e:
        return {"status": "error", "message": f"LLM API 연결 실패: {e}", "url": url}

# 7) 사용 중인 모델
@router.get("/model", summary="LLM 모델 정보")
def llm_model():
    return {
        "model": os.getenv("LLM_MODEL", "미설정"),
        "llm_api_url": os.getenv("LLM_API_URL", "미설정")
    }

# 8) Slack
@router.get("/slack", summary="Slack 연동 확인")
def slack_check():
    try:
        token = os.getenv("SLACK_BOT_TOKEN")
        if not token:
            return {"status": "error", "message": "SLACK_BOT_TOKEN 누락"}

        res = requests.post(
            "https://slack.com/api/auth.test",
            headers={"Authorization": f"Bearer {token}"},
            timeout=3
        )
        data = res.json()
        if data.get("ok"):
            return {"status": "ok", "team": data.get("team"), "user": data.get("user")}
        return {"status": "error", "message": data.get("error", "Slack 오류")}
    except Exception as e:
        return {"status": "error", "message": f"Slack API 오류: {e}"}

# 9) ClickUp
@router.get("/clickup", summary="ClickUp 연동 상태")
def clickup_check():
    try:
        token = os.getenv("CLICKUP_API_KEY")
        if not token:
            return {"status": "error", "message": "CLICKUP_API_KEY 누락"}

        res = requests.get(
            "https://api.clickup.com/api/v2/team",
            headers={"Authorization": token},
            timeout=3
        )
        data = res.json()
        if "teams" in data:
            return {"status": "ok", "team_count": len(data["teams"])}
        return {"status": "error", "message": data.get("err", "ClickUp 오류")}
    except Exception as e:
        return {"status": "error", "message": f"ClickUp API 오류: {e}"}

# 10) GeoIP 상태
@router.get("/geoip", summary="GeoIP 상태 및 정책 확인")
def geoip_status():
    path = os.getenv("GEOIP_DB_PATH", "").strip()  # ✅ 기본값 제거(환경 의존)
    status: Dict[str, object] = {"GEOIP_DB_PATH": path or "미설정"}

    if not path:
        status["geoip_db_loaded"] = False
        status["error"] = "GEOIP_DB_PATH 미설정"
        status["policy"] = {
            "ALLOW_ALL_COUNTRIES": ALLOW_ALL_COUNTRIES,
            "ALLOWED_COUNTRIES": ALLOWED_COUNTRIES
        }
        return status

    if not os.path.exists(path):
        status["geoip_db_loaded"] = False
        status["error"] = f"파일 없음: {path}"
        status["policy"] = {
            "ALLOW_ALL_COUNTRIES": ALLOW_ALL_COUNTRIES,
            "ALLOWED_COUNTRIES": ALLOWED_COUNTRIES
        }
        return status

    reader = None
    try:
        reader = geoip2.database.Reader(path)
        test_ip = "8.8.8.8"
        response = reader.country(test_ip)
        country_code = response.country.iso_code
        blocked = is_country_blocked(country_code)
        status.update({
            "geoip_db_loaded": True,
            "test_ip": test_ip,
            "country_code": country_code,
            "is_blocked": blocked,
        })
    except Exception as e:
        status["geoip_db_loaded"] = False
        status["error"] = str(e)
    finally:
        if reader:
            reader.close()

    status["policy"] = {
        "ALLOW_ALL_COUNTRIES": ALLOW_ALL_COUNTRIES,
        "ALLOWED_COUNTRIES": ALLOWED_COUNTRIES
    }
    return status
