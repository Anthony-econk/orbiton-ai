import os
import json
import requests
from rapidfuzz import fuzz

# 환경변수
CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")
CLICKUP_TEAM_ID = os.getenv("CLICKUP_TEAM_ID")

# 사용자 매핑 JSON 로딩
def load_user_mapping():
    with open("services/user_map.json", "r", encoding="utf-8") as f:
        return json.load(f)

# ClickUp에 Task 생성
def create_clickup_task(task_name, due_date=None, assignee_email=None):
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

    # 이메일이 있으면 assignee 지정
    if assignee_email:
        user_id = find_clickup_user_id(assignee_email)
        if user_id:
            payload["assignees"] = [user_id]

    res = requests.post(url, headers=headers, json=payload)
    print(f"[ClickUp] Create Response: {res.status_code} - {res.text}")
    return res.json()

# ClickUp 사용자 ID 조회
def find_clickup_user_id(email):
    url = f"https://api.clickup.com/api/v2/team/{CLICKUP_TEAM_ID}/user"
    headers = {
        "Authorization": CLICKUP_API_KEY
    }
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return None

    data = res.json()
    for member in data.get("users", []):
        if member["user"]["email"] == email:
            return member["user"]["id"]
    return None

# 기존 작업 유사도 검색
def find_similar_task(task_name, threshold=80):
    tasks = get_task_list().get("tasks", [])
    matches = []
    for task in tasks:
        raw = task["name"]
        clean = raw.split(":", 1)[-1].strip()

        if task_name.strip() in clean:
            matches.append((task["id"], raw, 100))
            continue

        score = fuzz.WRatio(task_name.strip(), clean)
        if score >= threshold:
            matches.append((task["id"], raw, score))

    return sorted(matches, key=lambda x: -x[2])

def get_task_list():
    url = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY
    }
    res = requests.get(url, headers=headers)
    print(f"[ClickUp] List Response: {res.status_code}")
    return res.json()

def find_task_id_by_name(task_name):
    for task in get_task_list().get("tasks", []):
        if task["name"] == task_name:
            return task["id"]
    return None

def delete_task_by_id(task_id):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {
        "Authorization": CLICKUP_API_KEY
    }
    res = requests.delete(url, headers=headers)
    print(f"[ClickUp] Delete Response: {res.status_code}")
    return res.status_code == 200

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
    return res.status_code == 200

def update_task_status(task_id, status):
    url = f"https://api.clickup.com/api/v2/task/{task_id}"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "status": status
    }
    res = requests.put(url, headers=headers, json=payload)
    return res.status_code == 200

def add_task_comment(task_id, comment_text):
    url = f"https://api.clickup.com/api/v2/task/{task_id}/comment"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "comment_text": comment_text
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.status_code == 200
