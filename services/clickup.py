# services/clickup.py
import os
import requests

# 환경변수로부터 ClickUp API 정보 가져오기
CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")

# ClickUp에 Task 생성 요청 함수
def create_clickup_task(task_name, due_date=None):
    url = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "name": task_name,
        "status": "to do"
    }

    if due_date:
        payload["due_date"] = due_date

    response = requests.post(url, headers=headers, json=payload)
    print(f"[ClickUp] Response {response.status_code}: {response.text}")
    return response.json()

# ✅ ClickUp 리스트에서 Task 목록 조회 함수
def get_task_list():
    url = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY
    }
    response = requests.get(url, headers=headers)
    print(f"[ClickUp] Task List Response {response.status_code}: {response.text}")
    return response.json()