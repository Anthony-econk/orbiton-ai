# commands/mytask.py
from fastapi.responses import PlainTextResponse
from services.clickup import get_task_list

# /orbiton.mytask 명령어 핸들러
async def handle(text, user_name):
    try:
        all_tasks = get_task_list().get("tasks", [])
        my_tasks = [
            task["name"]
            for task in all_tasks
            if task["name"].startswith(f"{user_name}:")
        ]

        if not my_tasks:
            return PlainTextResponse("📭 할당된 작업이 없습니다.")

        task_list = "\n".join(f"• {task.split(':',1)[-1].strip()}" for task in my_tasks)
        return PlainTextResponse(f"📋 *{user_name}*님의 할당된 작업 목록:\n{task_list}")

    except Exception as e:
        return PlainTextResponse(f"❌ 오류 발생: {e}")
