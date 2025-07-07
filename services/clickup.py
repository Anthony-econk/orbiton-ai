# services/clickup.py
import os
import requests
from rapidfuzz import fuzz

# 동일소수 재반영을 위한 주석 추가
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

# 90% 이상 유사한 기존 작업 찾기
def find_similar_task(task_name, threshold=90):
    tasks = get_task_list().get("tasks", [])
    matches = []
    for task in tasks:
        # prefix 제거하고 비교
        clean_task_name = task["name"].split(":", 1)[-1].strip()
        score = fuzz.WRatio(task_name, clean_task_name)
        if score >= threshold:
            matches.append((task["id"], task["name"], score))
    return sorted(matches, key=lambda x: -x[2])




# ✅ ClickUp 리스트에서 Task 목록 조회 함수
def get_task_list():
    url = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY
    }
    response = requests.get(url, headers=headers)
    print(f"[ClickUp] Task List Response {response.status_code}: {response.text}")
    return response.json()

# ✅ 특정 Task 이름으로 ID 조회
def find_task_id_by_name(task_name):
    url = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY
    }
    res = requests.get(url, headers=headers)
    data = res.json()
    tasks = data.get("tasks", [])
    for task in tasks:
        if task["name"] == task_name:
            return task["id"]
    return None

# ✅ Task ID로 삭제
def delete_task_by_id(task_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {
        "Authorization": CLICKUP_API_KEY
    }
    res = requests.delete(url, headers=headers)
    print(f"[ClickUp] Delete Response {res.status_code}")
    return res.status_code == 200

# ✅ Task 설명 업데이트
def update_task_description(task_id, description):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "description": description
    }
    res = requests.put(url, headers=headers, json=payload)
    print(f"[ClickUp] Update Description Response {res.status_code}")
    return res.status_code == 200
