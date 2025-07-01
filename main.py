from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import uvicorn
import os
import requests

# FastAPI 앱 생성
app = FastAPI()

# 환경변수 불러오기 (.env 또는 Render 설정에서 자동 반영됨)
CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")

# ClickUp에 Task를 생성하는 함수
def create_clickup_task(task_name):
    url = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "name": task_name,     # 생성할 작업 이름
        "status": "to do"      # 기본 상태 (필요시 변경 가능)
    }

    # POST 요청으로 ClickUp에 작업 생성
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Slack에서 들어오는 Slash Command 이벤트 처리 엔드포인트
@app.post("/slack/events")
async def slack_events(request: Request):
    # Slack 명령으로부터 전달된 Form 데이터 추출
    form_data = await request.form()
    command = form_data.get("command")       # 예: "/orbiton.assign"
    text = form_data.get("text")             # 예: "@techsoft 보고서 작성"
    user_name = form_data.get("user_name")   # 예: "techsoft"

    # 수신 로그 출력
    print(f"📩 Received: {command=} {text=} {user_name=}")

    # 명령어에 따라 분기 처리
    if command == "/orbiton.assign":
        # ClickUp에 Task 생성
        task_name = f"{user_name}: {text}"   # Task에 사용자 이름을 포함
        result = create_clickup_task(task_name)

        # 성공 여부에 따라 응답 메시지 반환
        if result.get("id"):
            return PlainTextResponse(f"✔ ClickUp Task 생성됨: {task_name}")
        else:
            return PlainTextResponse("⚠️ ClickUp Task 생성 실패")

    elif command == "/orbiton.deadline":
        return PlainTextResponse(f"📆 Deadline set: {text}")

    elif command == "/orbiton.list":
        return PlainTextResponse("📝 Here's your task list!")

    elif command == "/orbiton.delete":
        return PlainTextResponse(f"❌ Deleted task: {text}")

    elif command == "/orbiton.update":
        return PlainTextResponse(f"✏️ Update task description: {text}")

    elif command == "/orbiton.status":
        return PlainTextResponse(f"🔄 Change task status: {text}")

    elif command == "/orbiton.mytask":
        return PlainTextResponse(f"👤 View My Tasks for: {user_name}")

    # 처리되지 않은 명령어
    else:
        return PlainTextResponse(f"❓ Unknown command: {text}")

# 로컬 개발 환경에서 실행 시 (Render 배포에서는 자동 실행됨)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=3000)
