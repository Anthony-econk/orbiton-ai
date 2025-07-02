# commands/tasklist.py
from fastapi.responses import PlainTextResponse
from services.clickup import get_task_list

# /orbiton.list 명령어 처리 핸들러
async def handle(text, user_name):
    try:
        # ✅ ClickUp에서 Task 목록 불러오기
        response = get_task_list()
        tasks = response.get("tasks", [])

        # ✅ Task가 없는 경우 안내
        if not tasks:
            return PlainTextResponse("📭 현재 등록된 작업이 없습니다.")

        # ✅ 최대 10개까지만 요약 출력
        summary = "\n".join([
            f"• {task['name']}" for task in tasks[:10]
        ])
        return PlainTextResponse(f"📝 현재 작업 목록 (최대 10개):\n{summary}")

    except Exception as e:
        return PlainTextResponse(f"⚠️ 작업 목록 불러오기 실패: {str(e)}")