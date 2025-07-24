# app/services/clickup_service.py
# ClickUp API와 통신하여 태스크 목록 조회 및 관리 기능 제공

import os
import httpx
from typing import List, Dict

CLICKUP_API_URL = os.getenv("CLICKUP_API_URL", "https://api.clickup.com/api/v2")
CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")

if not CLICKUP_API_KEY:
    raise EnvironmentError("CLICKUP_API_KEY 환경변수가 설정되지 않았습니다.")

# ClickUp 리스트 ID를 기반으로 태스크 목록 조회
async def get_tasks_from_list(list_id: str) -> List[Dict]:
    url = f"{CLICKUP_API_URL}/list/{list_id}/task"
    headers = {"Authorization": CLICKUP_API_KEY}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data.get("tasks", [])
        except Exception:
            return []

# 태스크 목록에서 제목(title)만 추출
async def extract_task_titles(tasks: List[Dict]) -> List[str]:
    return [task.get("name", "(제목 없음)") for task in tasks]

# 태스크 설명 업데이트
async def update_task_description(task_id: str, description: str) -> bool:
    url = f"{CLICKUP_API_URL}/task/{task_id}"
    headers = {"Authorization": CLICKUP_API_KEY, "Content-Type": "application/json"}
    payload = {"description": description}

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=payload)
        return response.status_code == 200

# 태스크 상태 업데이트
async def update_task_status(task_id: str, status: str) -> bool:
    url = f"{CLICKUP_API_URL}/task/{task_id}"
    headers = {"Authorization": CLICKUP_API_KEY, "Content-Type": "application/json"}
    payload = {"status": status}

    async with httpx.AsyncClient() as client:
        response = await client.put(url, headers=headers, json=payload)
        return response.status_code == 200

# 태스크 댓글 추가
async def add_task_comment(task_id: str, comment_text: str) -> bool:
    url = f"{CLICKUP_API_URL}/task/{task_id}/comment"
    headers = {"Authorization": CLICKUP_API_KEY, "Content-Type": "application/json"}
    payload = {"comment_text": comment_text}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        return response.status_code == 200

# 태스크 삭제
async def delete_task(task_id: str) -> bool:
    url = f"{CLICKUP_API_URL}/task/{task_id}"
    headers = {"Authorization": CLICKUP_API_KEY}

    async with httpx.AsyncClient() as client:
        response = await client.delete(url, headers=headers)
        return response.status_code == 200