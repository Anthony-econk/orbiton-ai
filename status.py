# commands/status.py
from fastapi.responses import PlainTextResponse
from services.clickup import find_task_id_by_name, update_task_status

# /orbiton.status 명령어 처리
async def handle(text, user_name):
    try:
        parts = text.strip().split(maxsplit=1)
        if len(parts) != 2:
            return PlainTextResponse("⚠️ 형식: 작업명 상태 (예: 업무정리 in progress)")

        task_name, new_status = parts
        full_task_name = f"{user_name}: {task_name}"

        task_id = find_task_id_by_name(full_task_name)
        if not task_id:
            return PlainTextResponse(f"❗ 작업을 찾을 수 없습니다: {task_name}")

        success = update_task_status(task_id, new_status)
        if success:
            return PlainTextResponse(f"🔄 작업 상태가 변경되었습니다: {task_name} → {new_status}")
        else:
            return PlainTextResponse(f"⚠️ 작업 상태 변경 실패: {task_name}")
    except Exception as e:
        return PlainTextResponse(f"❌ 오류 발생: {str(e)}")
