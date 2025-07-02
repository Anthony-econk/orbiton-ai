# commands/delete.py
from fastapi.responses import PlainTextResponse
from services.clickup import find_task_id_by_name, delete_task_by_id

# /orbiton.delete 명령어 처리
async def handle(text, user_name):
    task_name = f"{user_name}: {text}".strip()

    # Step 1: Task ID 조회
    task_id = find_task_id_by_name(task_name)
    if not task_id:
        return PlainTextResponse(f"❗ 삭제할 작업을 찾을 수 없습니다: {task_name}")

    # Step 2: Task 삭제 요청
    success = delete_task_by_id(task_id)
    if success:
        return PlainTextResponse(f"🗑 작업 삭제 완료: {task_name}")
    else:
        return PlainTextResponse(f"⚠️ 작업 삭제 실패: {task_name}")
