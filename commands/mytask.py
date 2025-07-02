# commands/mytask.py
from fastapi.responses import PlainTextResponse
from services.clickup import get_task_list

# /orbiton.mytask 명령어 처리
async def handle(text, user_name):
    try:
        response = get_task_list()
        tasks = response.get("tasks", [])

        # ✅ 사용자 이름으로 시작하는 Task만 필터링
        user_tasks = [task for task in tasks if task["name"].startswith(f"{user_name}:")]

        if not user_tasks:
            return PlainTextResponse("📭 현재 내 작업이 없습니다.")

        summary = "\n".join([
            f"• {task['name']}" for task in user_tasks[:10]
        ])

        return PlainTextResponse(f"👤 내 작업 목록 (최대 10개):\n{summary}")

    except Exception as e:
        return PlainTextResponse(f"⚠️ 내 작업 조회 실패: {str(e)}")
