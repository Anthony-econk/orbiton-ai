# backend/services/clickup_service.py

import os
import httpx
from typing import List, Dict
from backend.utils.logger import logger

BASE_URL = "https://api.clickup.com/api/v2"

def get_clickup_headers() -> Dict[str, str]:
    api_key = os.getenv("CLICKUP_API_KEY")
    if not api_key:
        raise EnvironmentError("CLICKUP_API_KEY 환경변수가 설정되지 않았습니다.")
    return {"Authorization": api_key, "Content-Type": "application/json"}

async def get_tasks_from_list(list_id: str) -> List[Dict]:
    url = f"{BASE_URL}/list/{list_id}/task"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=get_clickup_headers())
            response.raise_for_status()
            data = response.json()
            return data.get("tasks", [])
    except Exception as e:
        logger.error(f"태스크 목록 조회 실패: {e}")
        return []

async def extract_task_titles(tasks: List[Dict]) -> List[str]:
    return [task.get("name", "(제목 없음)") for task in tasks]

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
