# commands/tasklist.py
from fastapi.responses import PlainTextResponse
from services.clickup import get_task_list

# /orbiton.list 명령어 핸들러
async def handle(text, user_name):
    try:
        data = get_task_list()
        tasks = data.get("tasks", [])

        if not tasks:
            return PlainTextResponse("📭 등록된 작업이 없습니다.")

        # 생성일 기준 정렬 (최신순)
        sorted_tasks = sorted(tasks, key=lambda t: t["date_created"], reverse=True)

        formatted = "\n".join(
            f"• {task['name']}  [{task['status']['status']}]"
            for task in sorted_tasks
        )
        return PlainTextResponse(f"📋 전체 작업 목록:\n{formatted}")

    except Exception as e:
        return PlainTextResponse(f"❌ 작업 목록 조회 오류: {e}")
