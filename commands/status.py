# commands/status.py
from fastapi.responses import PlainTextResponse
from services.clickup import update_task_status, find_similar_task

# /orbiton.status 명령어 처리 핸들러
# 예시: /orbiton.status 보고서작성 done
async def handle(text, user_name):
    try:
        task_raw, new_status = text.strip().rsplit(" ", 1)
        full_name = f"{user_name}: {task_raw.strip()}"

        # 유사도 높은 기존 작업 찾기
        similar = find_similar_task(full_name)
        if not similar:
            return PlainTextResponse(f"❗ 작업을 찾을 수 없습니다: {task_raw}")

        task_id, task_name, score = similar[0]

        success = update_task_status(task_id, new_status.strip())
        if success:
            return PlainTextResponse(f"✅ 작업 상태가 변경되었습니다: {task_name} → *{new_status}*")
        else:
            return PlainTextResponse("⚠️ 상태 변경 실패")

    except Exception as e:
        return PlainTextResponse(f"❌ 입력 오류 또는 형식을 확인해주세요: {e}")