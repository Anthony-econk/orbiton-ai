# commands/assign.py
from fastapi.responses import PlainTextResponse
from services.clickup import create_clickup_task

# /orbiton.assign 명령어 처리 핸들러
async def handle(text, user_name):
    task_name = f"{user_name}: {text}"
    result = create_clickup_task(task_name)

    if result.get("id"):
        return PlainTextResponse(f"✔ ClickUp Task 생성됨: {task_name}")
    else:
        return PlainTextResponse("⚠️ ClickUp Task 생성 실패")
