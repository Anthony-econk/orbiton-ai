# backend/services/clickup_service.py
# ClickUp API와 통신하여 태스크 목록 조회 및 관리 기능 제공

import os
import httpx
from typing import List, Dict
from backend.utils.logger import logger

# ✅ ClickUp API 기본 URL 설정
BASE_URL = "https://api.clickup.com/api/v2"

# ✅ 인증 헤더 생성 함수
def get_clickup_headers() -> Dict[str, str]:
    api_key = os.getenv("CLICKUP_API_KEY")
    if not api_key:
        raise EnvironmentError("CLICKUP_API_KEY 환경변수가 설정되지 않았습니다.")
    return {"Authorization": api_key, "Content-Type": "application/json"}

# ✅ 특정 담당자의 태스크 목록 조회 (assignee_id 기준)
async def get_my_tasks(list_id: str, assignee_id: str) -> Dict:
    url = f"{BASE_URL}/list/{list_id}/task?assignees[]={assignee_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=get_clickup_headers())
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"ClickUp 태스크 조회 실패: {e}")
        return {"error": str(e)}

# ✅ 태스크 목록에서 제목(title)만 추출
async def extract_task_titles(tasks: List[Dict]) -> List[str]:
    return [task.get("name", "(제목 없음)") for task in tasks]

# ✅ 태스크 설명(description) 업데이트
async def update_task_description(task_id: str, description: str) -> bool:
    url = f"{BASE_URL}/task/{task_id}"
    payload = {"description": description}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=get_clickup_headers(), json=payload)
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"설명 업데이트 실패 (task_id={task_id}): {e}")
        return False

# ✅ 태스크 상태(status) 업데이트
async def update_task_status(task_id: str, status: str) -> bool:
    url = f"{BASE_URL}/task/{task_id}"
    payload = {"status": status}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url, headers=get_clickup_headers(), json=payload)
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"상태 업데이트 실패 (task_id={task_id}): {e}")
        return False

# ✅ 태스크에 댓글(comment) 추가
async def add_task_comment(task_id: str, comment_text: str) -> bool:
    url = f"{BASE_URL}/task/{task_id}/comment"
    payload = {"comment_text": comment_text}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=get_clickup_headers(), json=payload)
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"댓글 추가 실패 (task_id={task_id}): {e}")
        return False

# ✅ 태스크 삭제
async def delete_task(task_id: str) -> bool:
    url = f"{BASE_URL}/task/{task_id}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.delete(url, headers=get_clickup_headers())
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"태스크 삭제 실패 (task_id={task_id}): {e}")
        return False
